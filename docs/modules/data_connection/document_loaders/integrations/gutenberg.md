# Gutenberg

>[Project Gutenberg](https://www.gutenberg.org/about/)是一个提供免费电子书的在线图书馆。

本文档介绍了如何将`Gutenberg`电子书的链接加载到我们可以在下游使用的文档格式中。

```python
from langchain.document_loaders import GutenbergLoader
```

```python
loader = GutenbergLoader("https://www.gutenberg.org/cache/epub/69972/pg69972.txt")
```

```python
ndata = loader.load()
```

```python
ndata[0].page_content[:300]
```


    'The Project Gutenberg eBook of The changed brides, by Emma Dorothy\r\n\n\nEliza Nevitte Southworth\r\n\n\n\r\n\n\nThis eBook is for the use of anyone anywhere in the United States and\r\n\n\nmost other parts of the world at no cost and with almost no restrictions\r\n\n\nwhatsoever. You may copy it, give it away or re-u'

```python
data[0].metadata
```


    {'source': 'https://www.gutenberg.org/cache/epub/69972/pg69972.txt'}
