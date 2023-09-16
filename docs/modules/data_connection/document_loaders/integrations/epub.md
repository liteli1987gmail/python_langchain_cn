# EPub
>[EPUB](https://en.wikipedia.org/wiki/EPUB)是一种使用".epub"扩展名的电子书文件格式。该术语是数字出版的缩写，有时被称为ePub。EPUB受到许多电子阅读器的支持，大多数智能手机、平板电脑和计算机都有兼容软件。

本文介绍了如何将`.epub`文档加载到我们可以在下游使用的文档格式中。您需要安装[`pandoc`](https://pandoc.org/installing.html)软件包才能使用此加载器。
```python
#!pip install pandoc
```

```python
from langchain.document_loaders import UnstructuredEPubLoader
```

```python
loader = UnstructuredEPubLoader("winter-sports.epub")
```

```python
ndata = loader.load()
```

## 保留元素
底层，Unstructured为不同的文本块创建不同的"元素"。默认情况下，我们将它们合并在一起，但您可以通过指定`mode="elements"`来轻松保留该分隔。
```python
loader = UnstructuredEPubLoader("winter-sports.epub", mode="elements")
```

```python
ndata = loader.load()
```

```python
ndata[0]
```



Document(page_content='The Project Gutenberg eBook of Winter Sports in\nSwitzerland, by E. F. Benson', lookup_str='', metadata={'source': 'winter-sports.epub', 'page_number': 1, 'category': 'Title'}, lookup_index=0)



```python

```