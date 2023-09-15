# BiliBili

>[Bilibili](https://www.bilibili.tv/) is one of the most beloved long-form video sites in China.

This loader utilizes the [bilibili-api](https://github.com/MoyuScript/bilibili-api) to fetch the text transcript from `Bilibili`.

With this BiliBiliLoader, users can easily obtain the transcript of their desired video content on the platform.


```python
#!pip install bilibili-api-python
```


```python
from langchain.document_loaders import BiliBiliLoader
```


```python
loader = BiliBiliLoader(["https://www.bilibili.com/video/BV1xt411o7Xu/"])
```


```python
loader.load()
```
