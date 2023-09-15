# URL

This covers how to load HTML documents from a list of URLs into a document format that we can use downstream.


```python
from langchain.document_loaders import UnstructuredURLLoader
```


```python
urls = [
    "https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment-february-8-2023",
    "https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment-february-9-2023",
]
```

Pass in ssl_verify=False with headers=headers to get past ssl_verification error.


```python
loader = UnstructuredURLLoader(urls=urls)
```


```python
data = loader.load()
```

# Selenium URL Loader

This covers how to load HTML documents from a list of URLs using the `SeleniumURLLoader`.

Using selenium allows us to load pages that require JavaScript to render.

## Setup

To use the `SeleniumURLLoader`, you will need to install `selenium` and `unstructured`.



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

This covers how to load HTML documents from a list of URLs using the `PlaywrightURLLoader`.

As in the Selenium case, Playwright allows us to load pages that need JavaScript to render.

## Setup

To use the `PlaywrightURLLoader`, you will need to install `playwright` and `unstructured`. Additionally, you will need to install the Playwright Chromium browser:


```python
# Install playwright
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
