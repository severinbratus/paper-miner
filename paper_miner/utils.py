from pathlib import Path
import pickle

from datetime import datetime


def begin_end(label: str, content: str) -> str:
    """Wrap content with BEGIN and END markers."""
    return f"""
--- BEGIN {label} ---

{content}

--- END {label} ---
""".strip()


def x_join(sep: str, *args: str) -> str:
    """Join strings with a separator, ignoring empty strings."""
    return sep.join(str(arg).strip() for arg in args if str(arg).strip())


def nn_join(*args: str) -> str:
    """Join strings with two newlines, ignoring empty strings."""
    return x_join("\n\n", *args)


def n_join(*args: str) -> str:
    """Join strings with a single newline, ignoring empty strings."""
    return x_join("\n", *args)


def glue(paper: str, prompt: str) -> str:
    "Glue paper and prompt into a single input for an LLM"
    begin_end_paper = begin_end("PAPER", paper)
    begin_end_prompt = begin_end("QUESTION", prompt)
    return nn_join(begin_end_paper, begin_end_prompt)


def h(level: int, text: str, ) -> str:
    """Create a header for Markdown with specified level."""
    return f"{'#' * level} {text.strip()}"


def bold(text: str) -> str:
    """Create a bold text for Markdown."""
    return f"**{text.strip()}**"


def save_pkl(obj, filepath):
    """Save an object to a pickle file."""
    with open(filepath, 'wb') as f:
        pickle.dump(obj, f)


def load_pkl(filepath):
    """Load an object from a pickle file."""
    with open(filepath, 'rb') as f:
        return pickle.load(f)


def get_citekey(dir: Path) -> str:
    key_file = next(dir.glob("*.key"), None)
    if key_file is None:
        raise FileNotFoundError(f"No .key file found in {dir}")
    return key_file.stem


def find_result_file(subdir: Path, ext: str = 'md') -> Path | None:
    """Find the first result file in the given subdirectory."""
    for file in subdir.glob(f"result-*.{ext}"):
        return file
    return None


def get_ts() -> str:
    """Get the current timestamp in a specific format."""
    return datetime.now().strftime("%d-%H%M%S-%f")  # day-hour-minute-second-microsecond
