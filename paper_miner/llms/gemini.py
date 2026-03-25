
import os
import time
import random
import re

from google import genai
from google.genai import types

from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

from typing import Tuple

from rich.console import Console
from rich.panel import Panel


# not used as of now
# logger = logging.getLogger('rich')

console = Console()


class Gemini:
    """A client for interacting with Google's Gemini API with rate limiting and error handling."""
    
    def __init__(self, model: str = "gemini-2.0-flash", rpm: int = 2000, debug: bool = False, save: bool = True):
        """
        Initialize the Gemini client.
        
        Args:
            model: The Gemini model to use
            rpm: Requests per minute rate limit
            debug: Whether to enable debug output
        """
        load_dotenv()
        
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found in environment variables. "
                "Create a .env file with GEMINI_API_KEY=..."
            )
        
        self.client = genai.Client(
            api_key=api_key,
            http_options=types.HttpOptions(api_version='v1alpha'),
        )

        # self.model = genai.GenerativeModel(model_name)
        self.model = model

        self.rpm = rpm
        self.debug = debug
        self.save = save
        if self.save:
            self.save_dir = Path('./logs/gemini/')
            self.save_dir.mkdir(parents=True, exist_ok=True)
        
        # Usage counters
        self.n_calls = 0
        self.n_in_chars = 0
        self.n_out_chars = 0
    
    def __call__(self, prompt: str, depth: int = 1) -> str:
        """
        Generate content using the Gemini model with automatic retry on errors.
        
        Args:
            prompt: The input prompt
            depth: Current retry depth (for internal use)
            
        Returns:
            Generated text response
        """
        timeout = self._calculate_timeout()
        indent = " " * (depth - 1)        

        # logger.debug(f"#{self.n_calls}")
        print(f"{indent}Call #{self.n_calls}")
        
        # if self.debug and depth == 1:
        #     debug_panel(logger, "Prompt", prompt)
        console.print(Panel(f"{prompt}", title="[bold yellow]Gemini Prompt", expand=False, style="yellow"), markup=False)
        
        try:
            # Split timeout around the API call for rate limiting
            time.sleep(timeout / 2 + 0.5)
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )
            time.sleep(timeout / 2 + 0.5)
            
            if not response.candidates:
                print("{indent}WARNING: no candidates")
                result = ""
            if not response.text:
                print("{indent}WARNING: empty response text")
                result = ""
            else:
                result = response.text
            
            # Update counters
            self.n_calls += 1
            self.n_in_chars += len(prompt)
            self.n_out_chars += len(result)

            if self.save:
                ts = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
                (self.save_dir / f"{ts}-in.md").write_text(prompt)
                (self.save_dir / f"{ts}-out.md").write_text(result)

            # if self.debug and depth == 1:
                # debug_panel(logger, "Response", result)
            console.print(Panel(f"{result}", title=f"[bold red]Gemini Response", expand=False, style="red"), markup=False)
            
            return result
            
        except Exception as e:
            if isinstance(e, TimeoutError):
                raise
            return self._handle_error(e, prompt, depth, timeout)
    
    def _calculate_timeout(self) -> float:
        """Calculate the base timeout for rate limiting."""
        return 61 / self.rpm
    
    def _handle_error(self, error: Exception, prompt: str, depth: int, timeout: float) -> str:
        """Handle API errors with appropriate retry logic."""
        err_msg = str(error)
        indent = " " * (depth - 1)
        
        print(f"{indent}ERROR: {err_msg.replace('\n', '   ')}")
        
        # Calculate sleep time based on error type
        if "429" in err_msg:  # Rate limit error
            sleep_time = self._extract_retry_after(err_msg) or round(timeout * depth, 2)
        else:
            sleep_time = round(timeout * depth, 2)
        
        print(f"{indent}sleeping for {sleep_time} seconds")
        time.sleep(sleep_time)
        
        return self.__call__(prompt, depth=depth + 1)
    
    def _extract_retry_after(self, error_message: str) -> int | None:
        """Extract retry-after time from error message."""
        match = re.search(r'seconds:\s*(\d+)', error_message)
        return int(match.group(1)) + 1 if match else None
    
    @property
    def counters(self) -> Tuple[int, int, int]:
        """
        Get usage statistics.
        
        Returns:
            Tuple of (calls, input_chars, output_chars)
        """
        return (self.n_calls, self.n_in_chars, self.n_out_chars)


# TODO? a generic Gemini ensemble class
# TODO methods to compute counters, and API usage

class DualGemini:
    def __init__(self, llm_flash: Gemini, llm_pro: Gemini):
        self.llm_flash = llm_flash
        self.llm_pro = llm_pro
    
    def __call__(self, *args, pro: bool = False, **kwargs) -> str:
        if pro:
            return self.llm_pro(*args, **kwargs)
        else:
            return self.llm_flash(*args, **kwargs)