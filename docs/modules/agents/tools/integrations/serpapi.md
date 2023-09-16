# SerpAPI

本笔记本介绍如何使用SerpAPI组件进行网络搜索。

```python
from langchain.utilities import SerpAPIWrapper
```

```python
search = SerpAPIWrapper()
```

```python
search.run("奥巴马的名字是什么？")
```


    '巴拉克·侯赛因·奥巴马二世'



## 自定义参数
您还可以使用任意参数自定义SerpAPI包装器。例如，在下面的示例中，我们将使用'bing'而不是'google'。

```python
params = {
    "engine": "bing",
    "gl": "us",
    "hl": "en",
}
search = SerpAPIWrapper(params=params)
```

```python
search.run("奥巴马的名字是什么？")
```


    '巴拉克·侯赛因·奥巴马二世是美国的政治家，曾担任2009年至2017年的第44任美国总统。奥巴马是美国历史上第一位非裔美国总统。在2005年至2008年担任伊利诺伊州的美国参议员，以及1997年至2004年担任伊利诺伊州的州参议员之前，奥巴马曾是一名民权律师，并在进入政界之前从事过民权律师工作。Wikipedia
barackobama.com'


```python
from langchain.agents import Tool

# 您可以创建一个工具并将其传递给代理
repl_tool = Tool(
    name="python_repl",
    description="一个Python Shell。使用它执行Python命令。输入应为有效的Python命令。如果要查看值的输出，应使用`print(...)`打印出来。",
    func=search.run,
)
```
