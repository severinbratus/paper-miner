from pathlib import Path
from paper_miner.utils import get_ts
from rich.console import Console
from rich.panel import Panel

from dotenv import load_dotenv

from openai import OpenAI
import tiktoken

MODEL = "gpt-4.1"
# MODEL = "gpt-3.5-turbo"

INPUT_COST = 2.00 / 1_000_000
OUTPUT_COST = 8.00 / 1_000_000

n_output_tokens = 0
n_input_tokens = 0


load_dotenv()

client = OpenAI()

encoding = tiktoken.encoding_for_model("gpt-4")

console = Console()


def gpt(prompt: str, sys_prompt: str = "You are a helpful assistant.") -> str | None:
    global n_input_tokens, n_output_tokens
    console.print(Panel(f"{prompt}", title="[bold yellow] GPT-4.1 Prompt", expand=False, style="yellow"), markup=False)
    ts = get_ts()
    log_prompt(prompt, ts)

    n_input_tokens += num_tokens(sys_prompt) + num_tokens(prompt)
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": prompt}
        ],
        n=1,
    )
    result = completion.choices[0].message.content
    n_output_tokens += num_tokens(result)
    console.print(Panel(f"{result}", title=f"[bold red]GPT-4.1 Response {ts}", expand=False, style="red"), markup=False)
    console.print(f"Input  tokens: {n_input_tokens} ({get_input_cost():.6f}$)")
    console.print(f"Output tokens: {n_output_tokens} ({get_output_cost():.6f}$)")
    console.print(f"Total cost: ${get_cost():.6f}")
    console.print()
    return result


def num_tokens(text: str) -> int:
    return len(encoding.encode(text))


def get_input_cost() -> float:
    return n_input_tokens * INPUT_COST


def get_output_cost() -> float:
    return n_output_tokens * OUTPUT_COST


def get_cost() -> float:
    return get_input_cost() + get_output_cost()


def log_prompt(prompt: str, ts: str) -> None:
    log_dir = Path('logs/gpt')
    log_dir.mkdir(parents=True, exist_ok=True)
    (log_dir / f"{ts}.txt").write_text(prompt, encoding='utf-8')
