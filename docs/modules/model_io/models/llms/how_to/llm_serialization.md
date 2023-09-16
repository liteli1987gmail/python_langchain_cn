# Serialization

本笔记本将介绍如何将LLM配置写入磁盘并从磁盘读取。如果您想保存给定LLM的配置（例如提供商、温度等），这将非常有用。

```python
from langchain.llms import OpenAI
from langchain.llms.loading import load_llm
```

## 加载
首先，让我们了解如何从磁盘加载LLM。LLM可以以两种格式保存在磁盘上：json或yaml。无论扩展名如何，加载的方式都是相同的。


```python
!cat llm.json
```

    {

        "model_name": "text-davinci-003",

        "temperature": 0.7,

        "max_tokens": 256,

        "top_p": 1.0,

        "frequency_penalty": 0.0,

        "presence_penalty": 0.0,

        "n": 1,

        "best_of": 1,

        "request_timeout": null,

        "_type": "openai"

    }


```python
llm = load_llm("llm.json")
```


```python
!cat llm.yaml
```

    _type: openai

    best_of: 1

    frequency_penalty: 0.0

    max_tokens: 256

    model_name: text-davinci-003

    n: 1

    presence_penalty: 0.0

    request_timeout: null

    temperature: 0.7

    top_p: 1.0




```python
llm = load_llm("llm.yaml")
```

## Saving
If you want to go from an LLM in memory to a serialized version of it, you can do so easily by calling the `.save` method. Again, this supports both json and yaml.


```python
llm.save("llm.json")
```


```python
llm.save("llm.yaml")
```


```python

```
