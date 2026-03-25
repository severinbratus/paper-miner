## paper-miner

You have some papers with PDFs in Zotero you want to summarize / analyze / otherwise process with LLMs.


### Workflow

0. Collect your PDFs from Zotero into one directory
  - Install ZotMoov
  - Configure attachment names as shown here https://github.com/wileyyugioh/zotmoov/issues/47
  - "Copy Selected to Custom Directory"
1. Install [marker-pdf](https://github.com/datalab-to/marker). Run on the directory.
2. Copy and adapt `paper_miner/cases/arc_review/main.py` to your needs.
3. Arrange the results as you wish from a Jupyter notebook


### Supported LLM APIs:

- OpenAI
- Gemini


### Project status: Discontinued.