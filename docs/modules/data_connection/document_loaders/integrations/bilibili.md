# BiliBili
[Bilibili](https://www.bilibili.tv/) 是中国最受欢迎的长视频网站之一。
此加载器利用[bilibili-api](https://github.com/MoyuScript/bilibili-api)从 `Bilibili` 获取文本转录。
通过这个 BiliBiliLoader，用户可以轻松获取所需视频内容的转录。
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