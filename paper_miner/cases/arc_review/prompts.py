sys_prompt = '''
You are a helpful scientific assistant in a literature review on "Methods applied to Abstraction and Reasoning Corpus (ARC) 2019--2025".

Here is some background information on ARC:

The Abstraction and Reasoning Corpus (Chollet 2019) is also known as ARC or ARC-AGI-1.
ARC-AGI-1 consists of 4 sets totalling 1,000 tasks:
- Training Set (400 tasks, sometimes called ARC-Easy)
- Public Eval Set (400 tasks, sometimes called ARC-Hard)
- Semiprivate Eval Set (100 tasks, for testing closed-source models)
- Private Eval Set (100 tasks)

ARC has multiple derivative corpora, e.g. 1D-ARC or ConceptARC.

Each task contains a few examples of input-output pairs, and a few test inputs.

---

You will be provided with a research paper related to ARC, and prompted with a question.
Please read the provided research paper and answer the user question based on the paper content.
Keep your answers concise, accurate, and relevant to the question asked.
Keep your style formal and academic.
'''

original_spec = '''
RQ0. Method summary
RQ1. Typology: hashtags (with explanations), classes
RQ2. Extract accuracy score (and the context: data, evaluation procedure, etc.)
RQ3. N/A. see RQ1 (#ns)
RQ4. (If a method is applied), is there a discussion of computational efficiency?
- a) at training time
- b) at inference time
RQ5. How are human priors represented in the method?
'''

comments = '''
RQ1 may take the the answer to RQ0 as input.
RQ5 as well.
'''



question_0 = {
    'title': 'RQ 0. Method Summary',
    'prompt': '''
Question: What method is being applied (or proposed) to ARC (or its derivative) and discussed in the paper?

For this question please look at the Methods section (or similar) and search for the following information:
- What is the method? Describe in a couple of words.
- How is the method trained? (if applicable)
- How does the method perform inference?
- How is the method evaluated?

Please answer in a concise and precise manner in the following format:

- Name/Description: ...
- Training: ...
- Inference: ...
- Evaluation: ...
- Brief Summary: ...

If no method is applied, answer in the following format:

- [No method applied]
- Brief Summary: ...
'''
}


question_1 = {
    'title': 'RQ 1. Method Typology',
    'prompt': '''
Question: How can the method be classified?

Here is a brief summary of the paper/method:

{answer_0}

---

Classify the method (or the paper) using relevant tags. Use the following tags:

By methodology:
  - neural networks `#nn`
    - transformers `#tf`
        - language models `#lm`
        - vision language models `#vlm`
  - symbolic `#symbolic`
    - inductive logic programming `#ilp`
  - neuro-symbolic (neural networks + symbolic reasoning methods) `#ns`
  - program synthesis `#psynth`
  - reinforcement learning `#rl`
  - graph-based `#graph`
  - object-based representations `#obj`

By contribution:
  - method proposed for ARC but not applied `#prop`
  - emphasis on analytical insights `#analysis`
  - helper corpus introduced `#corpus`
  - helper tools introduced `#tools`
  - human performance measured or analysed `#human`
  - method applied to a derivative corpus `#1darc` `#mcarc` `#larc` etc

You may include additional relevant tags as needed.
Please return the tags as a bullet list, with very brief explanations per tag, if needed / not obvious.
'''
}

question_2 = {
    'title': 'RQ 2. Method Accuracy',
    'prompt': '''
Question: What is the accuracy of the method on ARC (or its derivative)?

Here is a brief summary of the paper/method:

{answer_0}

---

Please extract or compute the performance of the method on ARC (or its derivative) as a percentage.
Please answer briefly and accurately in the following format:

- Accuracy: ...
- Data: ...
- Evaluation Procedure: ...

If not applicable, then answer in the following format:

- [Not applicable]
- Explanation: ...
'''
}

question_4 = {
    'title': 'RQ 4. Computational Efficiency',
    'prompt': '''
Question: Is computational efficiency (compute costs) of the method discussed?

Here is a brief summary of the paper/method:

{answer_0}

---

Please look at the Discussion section (or similar) and search for the following information:
- Is the computational efficiency (or compute costs) of the method discussed?
- If yes, is it discussed for training time, inference time, or both?

Please answer in the following format.
Summarize your findings very briefly, or give `[Not discussed]` if no discussion is present.

- Training Efficiency: ...
- Inference Efficiency: ...
'''
}

question_5 = {
  'title': 'RQ 5. Core Knowldge Priors',
  'prompt': '''
Question: How are Core Knowledge priors represented in the method?

Core Knowledge priors are a subset of human priors necessary for efficient solving of ARC tasks.
Core Knowledge priors include: Objectness, Goal-directedness, Numeric and Counting, Basic Geometry & Topology priors.

Here is a brief summary of the paper/method:

{answer_0}

---

Please answer briefly and accurately as a bullet point list of one or more bullets.

If not applicable, then answer in the following format:

- [Not applicable]
- Explanation: ...
'''
}

questions = {
    '0': question_0,
    '1': question_1,
    '2': question_2,
    '4': question_4,
    '5': question_5,
}


citekey_comment_template = '''
When needed, use \\citet{{{citekey}}} or \\citep{{{citekey}}} to refer to the paper authors.
'''
