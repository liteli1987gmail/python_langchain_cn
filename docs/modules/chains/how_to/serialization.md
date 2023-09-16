# 序列化
本笔记本介绍了如何将链条序列化到磁盘并从磁盘中反序列化。我们使用的序列化格式是 JSON 或 YAML。目前，只有一些链条支持这种类型的序列化。随着时间的推移，我们将增加支持的链条数量。

## 将链条保存到磁盘
首先，让我们了解如何将链条保存到磁盘。可以使用 `.save` 方法来实现，需要指定一个具有 JSON 或 YAML 扩展名的文件路径。


```python
from langchain import PromptTemplate, OpenAI, LLMChain

template = """Question: {question}

Answer: Let's think step by step."""
prompt = PromptTemplate(template=template, input_variables=["question"])
llm_chain = LLMChain(prompt=prompt, llm=OpenAI(temperature=0), verbose=True)
```


```python
llm_chain.save("llm_chain.json")
```

Let's now take a look at what's inside this saved file


```python
!cat llm_chain.json
```

    {

        "memory": null,

        "verbose": true,

        "prompt": {

            "input_variables": [

                "question"

            ],

            "output_parser": null,

            "template": "Question: {question}\n\nAnswer: Let's think step by step.",

            "template_format": "f-string"

        },

        "llm": {

            "model_name": "text-davinci-003",

            "temperature": 0.0,

            "max_tokens": 256,

            "top_p": 1,

            "frequency_penalty": 0,

            "presence_penalty": 0,

            "n": 1,

            "best_of": 1,

            "request_timeout": null,

            "logit_bias": {},

            "_type": "openai"

        },

        "output_key": "text",

        "_type": "llm_chain"

    }

## Loading a chain from disk
We can load a chain from disk by using the `load_chain` method.


```python
from langchain.chains import load_chain
```


```python
chain = load_chain("llm_chain.json")
```


```python
chain.run("whats 2 + 2")
```

    
    
    [1m> Entering new LLMChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mQuestion: whats 2 + 2
    
    Answer: Let's think step by step.[0m
    
    [1m> Finished chain.[0m
    




    ' 2 + 2 = 4'



## Saving components separately
In the above example, we can see that the prompt and llm configuration information is saved in the same json as the overall chain. Alternatively, we can split them up and save them separately. This is often useful to make the saved components more modular. In order to do this, we just need to specify `llm_path` instead of the `llm` component, and `prompt_path` instead of the `prompt` component.


```python
llm_chain.prompt.save("prompt.json")
```


```python
!cat prompt.json
```

    {

        "input_variables": [

            "question"

        ],

        "output_parser": null,

        "template": "Question: {question}\n\nAnswer: Let's think step by step.",

        "template_format": "f-string"

    }


```python
llm_chain.llm.save("llm.json")
```


```python
!cat llm.json
```

    {

        "model_name": "text-davinci-003",

        "temperature": 0.0,

        "max_tokens": 256,

        "top_p": 1,

        "frequency_penalty": 0,

        "presence_penalty": 0,

        "n": 1,

        "best_of": 1,

        "request_timeout": null,

        "logit_bias": {},

        "_type": "openai"

    }


```python
config = {
    "memory": None,
    "verbose": True,
    "prompt_path": "prompt.json",
    "llm_path": "llm.json",
    "output_key": "text",
    "_type": "llm_chain",
}
import json

with open("llm_chain_separate.json", "w") as f:
    json.dump(config, f, indent=2)
```


```python
!cat llm_chain_separate.json
```

    {

      "memory": null,

      "verbose": true,

      "prompt_path": "prompt.json",

      "llm_path": "llm.json",

      "output_key": "text",

      "_type": "llm_chain"

    }

We can then load it in the same way


```python
chain = load_chain("llm_chain_separate.json")
```


```python
chain.run("whats 2 + 2")
```

    
    
    [1m> Entering new LLMChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mQuestion: whats 2 + 2
    
    Answer: Let's think step by step.[0m
    
    [1m> Finished chain.[0m
    




    ' 2 + 2 = 4'




```python

```
