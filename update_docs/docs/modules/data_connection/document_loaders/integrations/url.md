# URL

这涵盖了如何从URL列表中加载HTML文档到我们可以在下游使用的文档格式。

```python
from langchain.document_loaders import UnstructuredURLLoader
```

```python
urls = [
    "https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment-february-8-2023",
    "https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment-february-9-2023",
]
```

使用headers=headers并传入ssl_verify=False以解决ssl_verification错误。

```python
loader = UnstructuredURLLoader(urls=urls)
```

```python
data = loader.load()
```

# Selenium URL Loader

这涵盖了如何使用`SeleniumURLLoader`从URL列表中加载HTML文档。

使用selenium允许我们加载需要JavaScript渲染的页面。

## 设置

要使用`SeleniumURLLoader`，您需要安装`selenium`和`unstructured`。

```python
from langchain.document_loaders import SeleniumURLLoader
```

```python
urls = [
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "https://goo.gl/maps/NDSHwePEyaHMFGwh8",
]
```

```python
loader = SeleniumURLLoader(urls=urls)
```

```python
data = loader.load()
```

# Playwright URL Loader

这涵盖了如何使用`PlaywrightURLLoader`从URL列表中加载HTML文档。

与Selenium情况类似，Playwright允许我们加载需要JavaScript渲染的页面。

## 设置

要使用`PlaywrightURLLoader`，您需要安装`playwright`和`unstructured`。此外，您还需要安装Playwright Chromium浏览器:$

```python
# 安装playwright
!pip install "playwright"
!pip install "unstructured"
!playwright install
```

```python
from langchain.document_loaders import PlaywrightURLLoader
```

```python
urls = [
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "https://goo.gl/maps/NDSHwePEyaHMFGwh8",
]
```

```python
loader = PlaywrightURLLoader(urls=urls, remove_selectors=["header", "footer"])
```

```python
data = loader.load()
```
