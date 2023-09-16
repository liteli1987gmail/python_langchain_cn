# Hacker News

[Hacker News](https://en.wikipedia.org/wiki/Hacker_News)（有时缩写为HN）是一个专注于计算机科学和创业的社交新闻网站。它由投资基金和初创企业孵化器Y Combinator运营。一般来说，可以提交的内容被定义为“满足人们知识好奇心的任何东西”。

本文档介绍了如何从[Hacker News](https://news.ycombinator.com/)上获取页面数据和评论。

```python
from langchain.document_loaders import HNLoader
```

```python
loader = HNLoader("https://news.ycombinator.com/item?id=34817881")
```

```python
ndata = loader.load()
```

```python
ndata[0].page_content[:300]
```


    "delta_p_delta_x 73 days ago  
             | next [–] 

Astrophysical and cosmological simulations are often insightful. They're also very cross-disciplinary; besides the obvious astrophysics, there's networking and sysadmin, parallel computing and algorithm theory (so that the simulation programs a"



```python
ndata[0].metadata
```


    {'source': 'https://news.ycombinator.com/item?id=34817881',
     'title': 'What Lights the Universe’s Standard Candles?'}

