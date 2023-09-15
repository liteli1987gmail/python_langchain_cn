# Gutenberg

>[Project Gutenberg](https://www.gutenberg.org/about/) is an online library of free eBooks.

This notebook covers how to load links to `Gutenberg` e-books into a document format that we can use downstream.


```python
from langchain.document_loaders import GutenbergLoader
```


```python
loader = GutenbergLoader("https://www.gutenberg.org/cache/epub/69972/pg69972.txt")
```


```python
data = loader.load()
```


```python
data[0].page_content[:300]
```




    'The Project Gutenberg eBook of The changed brides, by Emma Dorothy\r\n\n\nEliza Nevitte Southworth\r\n\n\n\r\n\n\nThis eBook is for the use of anyone anywhere in the United States and\r\n\n\nmost other parts of the world at no cost and with almost no restrictions\r\n\n\nwhatsoever. You may copy it, give it away or re-u'




```python
data[0].metadata
```




    {'source': 'https://www.gutenberg.org/cache/epub/69972/pg69972.txt'}


