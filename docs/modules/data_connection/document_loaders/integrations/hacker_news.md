# Hacker News

>[Hacker News](https://en.wikipedia.org/wiki/Hacker_News) (sometimes abbreviated as `HN`) is a social news website focusing on computer science and entrepreneurship. It is run by the investment fund and startup incubator `Y Combinator`. In general, content that can be submitted is defined as "anything that gratifies one's intellectual curiosity."

This notebook covers how to pull page data and comments from [Hacker News](https://news.ycombinator.com/)


```python
from langchain.document_loaders import HNLoader
```


```python
loader = HNLoader("https://news.ycombinator.com/item?id=34817881")
```


```python
data = loader.load()
```


```python
data[0].page_content[:300]
```




    "delta_p_delta_x 73 days ago  \n             | next [–] \n\nAstrophysical and cosmological simulations are often insightful. They're also very cross-disciplinary; besides the obvious astrophysics, there's networking and sysadmin, parallel computing and algorithm theory (so that the simulation programs a"




```python
data[0].metadata
```




    {'source': 'https://news.ycombinator.com/item?id=34817881',
     'title': 'What Lights the Universe’s Standard Candles?'}


