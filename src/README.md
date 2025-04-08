This directory contains Jupyter notebooks used to prototype and test PDF summarization and question-answering features that are integrated into the Discord bot.

### summarize.ipynb

> Purpose: Prototype and test different summarization methods for PDF documents.

#### Key Components:

- Load PDF using `ReadFile.load_pdf()`
- Test full summarization using `FullSummarize.full_summarize()`
- Test range-based summarization with `UserRangeSummarize.range_summarize()`
- Evaluate summary length, clarity, and language handling

---

### retrieve.ipynb

> Purpose: Experiment with retrieval-based question answering from PDFs.

#### Key Components:

- Load document into a retrieval pipeline with `Retriever.retrieve()`
- Ask questions and evaluate responses using `Questions_and_Answers.qa_chain()`
- Analyze context windows, relevance, and accuracy
- Test multiple documents merged into a single knowledge base

---
