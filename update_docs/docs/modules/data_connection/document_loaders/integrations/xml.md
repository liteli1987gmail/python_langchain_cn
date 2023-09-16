# XML

`UnstructuredXMLLoader` 用于加载 `XML` 文件。该加载器适用于 `.xml` 文件。页面内容将是从 XML 标签中提取的文本。

```python
from langchain.document_loaders import UnstructuredXMLLoader
```

```python
loader = UnstructuredXMLLoader(
    "example_data/factbook.xml",
)
docs = loader.load()
docs[0]
```




    Document(page_content='United States

Washington, DC

Joe Biden

Baseball

Canada

Ottawa

Justin Trudeau

Hockey

France

Paris

Emmanuel Macron

Soccer

Trinidad & Tobado

Port of Spain

Keith Rowley

Track & Field', metadata={'source': 'example_data/factbook.xml'})




```python

```