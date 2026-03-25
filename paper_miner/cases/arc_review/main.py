from datetime import datetime
from pathlib import Path
import shutil
import pickle
import time

from paper_miner.llms.openai import gpt
from paper_miner.cases.arc_review.prompts import (
    sys_prompt,
    questions,
    citekey_comment_template,
)

from paper_miner.utils import (
    find_result_file,
    save_pkl, load_pkl,
    glue,
    n_join, nn_join,
    h, bold
)

from rich.console import Console
console = Console()


from sys import argv


LIMIT_CONTENT_SIZE = 1024 * 1024  # characters

def main(SRC_PATH: str, DEST_PATH: str):
    """Process all .md files in SRC_PATH, generate results using LLM, and save results in DEST_PATH."""
    print('main()')
    src_dir = Path(SRC_PATH)
    dst_dir = Path(DEST_PATH)

    dst_dir.mkdir(exist_ok=True)
    shutil.copytree(src_dir, dst_dir, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns('*.jpeg', '*.json'))

    md_files = list(src_dir.rglob("*.md"))
    assert md_files
    for md_file in md_files:
        subdir = dst_dir / md_file.stem
        citekey = md_file.stem
        print("Processing:", citekey)

        if find_result_file(subdir):
            print(f"Skipping, results already exist: {subdir.name}")
            continue
        
        with md_file.open("r", encoding="utf-8") as file:
            md_content = file.read()

        if not len(md_content) < LIMIT_CONTENT_SIZE:
            print(f"Skipping, file too large: {md_file.name}")
            continue

        result = lmp(md_content, citekey)

        ts = datetime.now().strftime("%d-%H%M%S-%f")

        result_pkl = subdir / f"result-{ts}.pkl"
        save_pkl(result, result_pkl)

        result_md = subdir / f"result-{ts}.md"
        header = h(2, citekey)

        subtitles = [question['title'] for question in questions.values()]
        answers = result.values()
        fmat_answer = lambda subtitle, answer: nn_join(h(3, subtitle), answer)
        content = nn_join(*(fmat_answer(subtitle, answer) for subtitle, answer in zip(subtitles, answers)))

        text = nn_join(header, content)
        result_md.write_text(text, encoding="utf-8")



def lmp(paper: str, citekey: str) -> dict[str, str | None]:
    def gpt_helper(prompt):
        prompt_w_key = n_join(prompt, citekey_comment_template.format(citekey=citekey))
        return gpt(glue(paper, prompt_w_key), sys_prompt=sys_prompt)

    answers = {}

    for key, question in questions.items():
        console.print(f'[bold]{question["title"]}[/bold]')
        prompt = question['prompt'].format_map(answers)
        answer = gpt_helper(prompt)
        answer_key = f"answer_{key}"
        answers[answer_key] = answer
        # console.print(answers)

    return answers


USAGE = "Usage: python -m paper_miner.cases.arc_review.main [src_path] [dest_path]"

if __name__ == "__main__":
    assert len(argv) <= 3, USAGE
    SRC_PATH = argv[1]  # e.g. 'data/arc_review/pdfs.markdown/'
    DEST_PATH = argv[2] # e.g. 'data/arc_review/pdfs.markdown.results/'
    main(SRC_PATH, DEST_PATH)