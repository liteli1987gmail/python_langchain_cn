# 笔记本 NotebookLoader

![LangChain](https://pica.zhimg.com/50/v2-56e8bbb52aa271012541c1fe1ceb11a2_r.gif 'LangChain中文网')


本笔记本介绍了如何将.ipynb笔记本中的数据加载到适合LangChain的格式中。

<!-- 警告：此文件是自动生成的！请勿编辑！而是用包含此文件位置和名称的笔记本进行编辑。 -->


```python
from langchain.document_loaders import NotebookLoader
```


```python
loader = NotebookLoader("example_data/notebook.ipynb")
```

`NotebookLoader.load（）`将`.ipynb`笔记本文件加载到`Document`对象中。

**参数**：

* `include_outputs`（bool）：是否在生成的文档中包含单元格输出（默认为False）。
* `max_output_length`（int）：从每个单元格输出中包含的最大字符数（默认为10）。
* `remove_newline`（bool）：是否从单元格源和输出中删除换行符（默认为False）。
* `traceback`（bool）：是否包含完整的回溯（默认为False）。


```python
loader.load(include_outputs=True, max_output_length=20, remove_newline=True)
```
