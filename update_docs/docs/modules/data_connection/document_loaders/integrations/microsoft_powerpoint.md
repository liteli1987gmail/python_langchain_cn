# Microsoft PowerPoint
>[Microsoft PowerPoint](https://en.wikipedia.org/wiki/Microsoft_PowerPoint)是Microsoft的演示程序。

本文介绍了如何将`Microsoft PowerPoint`文档加载到我们可以在下游使用的文档格式中。

```python
from langchain.document_loaders import UnstructuredPowerPointLoader
```

```python
loader = UnstructuredPowerPointLoader("example_data/fake-power-point.pptx")
```

```python
data = loader.load()
```

```python
data
```




    [Document(page_content='Adding a Bullet Slide\n\nFind the bullet slide layout\n\nUse _TextFrame.text for first bullet\n\nUse _TextFrame.add_paragraph() for subsequent bullets\n\nHere is a lot of text!\n\nHere is some text in a text box!', metadata={'source': 'example_data/fake-power-point.pptx'})]



## Retain Elements

Under the hood, `Unstructured` creates different "elements" for different chunks of text. By default we combine those together, but you can easily keep that separation by specifying `mode="elements"`.


```python
loader = UnstructuredPowerPointLoader(
    "example_data/fake-power-point.pptx", mode="elements"
)
```


```python
data = loader.load()
```


```python
data[0]
```




    Document(page_content='Adding a Bullet Slide', lookup_str='', metadata={'source': 'example_data/fake-power-point.pptx'}, lookup_index=0)




```python

```
