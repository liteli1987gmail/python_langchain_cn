# Arxiv
[arXiv](https://arxiv.org/)是一个开放获取的存档，存储了约200万篇物理学、数学、计算机科学、定量生物学、定量金融、统计学、电气工程与系统科学以及经济学方面的学术文章。

本笔记本展示了如何从`Arxiv.org`中加载科学文章，并将其转换为我们可以在下游使用的文档格式。

## 安装
首先，您需要安装`arxiv` Python包。
```python
!pip install arxiv
```

其次，您需要安装`PyMuPDF` Python包，将从`arxiv.org`网站下载的PDF文件转换为文本格式。
```python
!pip install pymupdf
```

## 示例
`ArxivLoader`具有以下参数：
- `query`：用于在Arxiv中查找文档的自由文本
- 可选的`load_max_docs`：默认值为100。使用它来限制下载文档的数量。如果下载所需100个文档需要时间，请使用较小的数字。
- 可选的`load_all_available_meta`：默认为False。默认情况下，仅下载最重要的字段：`Published`（文档发布/最后更新日期）、`Title`、`Authors`、`Summary`。如果为True，则还会下载其他字段。
```python
from langchain.document_loaders import ArxivLoader
```

```python



docs = ArxivLoader(query="1605.08386", load_max_docs=2).load()
len(docs)
```

```python

docs[0].metadata  # Document的元数据
```



    {'Published': '2016-05-26',
     'Title': 'Heat-bath random walks with Markov bases',
     'Authors': 'Caprice Stanley, Tobias Windisch',
     'Summary': 'Graphs on lattice points are studied whose edges come from a finite set of
allowed moves of arbitrary length. We show that the diameter of these graphs on
fibers of a fixed integer matrix can be bounded from above by a constant. We
then study the mixing behaviour of heat-bath random walks on these graphs. We
also state explicit conditions on the set of moves so that the heat-bath random
walk, a generalization of the Glauber dynamics, is an expander in fixed
dimension.'}



```python

docs[0].page_content[:400]  # Document内容的所有页面
```



    'arXiv:1605.08386v1  [math.CO]  26 May 2016
HEAT-BATH RANDOM WALKS WITH MARKOV BASES
CAPRICE STANLEY AND TOBIAS WINDISCH
Abstract. Graphs on lattice points are studied whose edges come from a finite set of
allowed moves of arbitrary length. We show that the diameter of these graphs on fibers of a
fixed integer matrix can be bounded from above by a constant. We then study the mixing
behaviour of heat-bath random walks on these graphs. We
also state explicit conditions on the set of moves so that the heat-bath random
walk, a generalization of the Glauber dynamics, is an expander in fixed
dimension.'


