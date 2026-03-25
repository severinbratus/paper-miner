from pathlib import Path
from sys import argv

from paper_miner.utils import find_result_file, nn_join


def main(in_dir: Path, out_path: Path):
    """Merge all result .md files in the subdirectories of in_dir into a single .md file at out_path."""
    subdirs = [d for d in in_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]
    subdirs.sort(key=lambda x: x.name)

    texts = []
    for subdir in subdirs:
        citekey = subdir.stem
        result_md = find_result_file(subdir)
        assert result_md is not None, f'No result file found in {subdir}'
        texts.append(result_md.read_text(encoding='utf-8'))
    
    full_text = nn_join(*texts)
    out_path.write_text(full_text)
    

# usage:
# python paper_miner/cases/arc_review/merge.py
if __name__ == '__main__':
    _, in_dir, out_path = argv
    main(Path(in_dir), Path(out_path))