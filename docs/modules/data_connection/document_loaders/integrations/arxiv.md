# Arxiv

>[arXiv](https://arxiv.org/) is an open-access archive for 2 million scholarly articles in the fields of physics, mathematics, computer science, quantitative biology, quantitative finance, statistics, electrical engineering and systems science, and economics.

This notebook shows how to load scientific articles from `Arxiv.org` into a document format that we can use downstream.

## Installation

First, you need to install `arxiv` python package.


```python
#!pip install arxiv
```

Second, you need to install `PyMuPDF` python package which transforms PDF files downloaded from the `arxiv.org` site into the text format.


```python
#!pip install pymupdf
```

## Examples

`ArxivLoader` has these arguments:
- `query`: free text which used to find documents in the Arxiv
- optional `load_max_docs`: default=100. Use it to limit number of downloaded documents. It takes time to download all 100 documents, so use a small number for experiments.
- optional `load_all_available_meta`: default=False. By default only the most important fields downloaded: `Published` (date when document was published/last updated), `Title`, `Authors`, `Summary`. If True, other fields also downloaded.


```python
from langchain.document_loaders import ArxivLoader
```


```python
docs = ArxivLoader(query="1605.08386", load_max_docs=2).load()
len(docs)
```


```python
docs[0].metadata  # meta-information of the Document
```




    {'Published': '2016-05-26',
     'Title': 'Heat-bath random walks with Markov bases',
     'Authors': 'Caprice Stanley, Tobias Windisch',
     'Summary': 'Graphs on lattice points are studied whose edges come from a finite set of\nallowed moves of arbitrary length. We show that the diameter of these graphs on\nfibers of a fixed integer matrix can be bounded from above by a constant. We\nthen study the mixing behaviour of heat-bath random walks on these graphs. We\nalso state explicit conditions on the set of moves so that the heat-bath random\nwalk, a generalization of the Glauber dynamics, is an expander in fixed\ndimension.'}




```python
docs[0].page_content[:400]  # all pages of the Document content
```




    'arXiv:1605.08386v1  [math.CO]  26 May 2016\nHEAT-BATH RANDOM WALKS WITH MARKOV BASES\nCAPRICE STANLEY AND TOBIAS WINDISCH\nAbstract. Graphs on lattice points are studied whose edges come from a ﬁnite set of\nallowed moves of arbitrary length. We show that the diameter of these graphs on ﬁbers of a\nﬁxed integer matrix can be bounded from above by a constant. We then study the mixing\nbehaviour of heat-b'


