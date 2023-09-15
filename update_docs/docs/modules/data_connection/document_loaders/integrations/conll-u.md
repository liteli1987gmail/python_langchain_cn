# CoNLL-U

>[CoNLL-U](https://universaldependencies.org/format.html) is revised version of the CoNLL-X format. Annotations are encoded in plain text files (UTF-8, normalized to NFC, using only the LF character as line break, including an LF character at the end of file) with three types of lines:
>- Word lines containing the annotation of a word/token in 10 fields separated by single tab characters; see below.
>- Blank lines marking sentence boundaries.
>- Comment lines starting with hash (#).

This is an example of how to load a file in [CoNLL-U](https://universaldependencies.org/format.html) format. The whole file is treated as one document. The example data (`conllu.conllu`) is based on one of the standard UD/CoNLL-U examples.


```python
from langchain.document_loaders import CoNLLULoader
```


```python
loader = CoNLLULoader("example_data/conllu.conllu")
```


```python
document = loader.load()
```


```python
document
```




    [Document(page_content='They buy and sell books.', metadata={'source': 'example_data/conllu.conllu'})]


