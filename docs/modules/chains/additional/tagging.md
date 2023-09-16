# 标记

标记链使用OpenAI的`functions`参数来指定用于标记文档的模式。这帮助我们确保模型输出我们想要的确切标记及其适当的类型。

当我们想要给一个段落打标签时，可以使用标记链来指定特定的属性（例如，这条信息的情感是什么？）


```python
from langchain.chat_models import ChatOpenAI
from langchain.chains import create_tagging_chain, create_tagging_chain_pydantic
from langchain.prompts import ChatPromptTemplate
```

    /Users/harrisonchase/.pyenv/versions/3.9.1/envs/langchain/lib/python3.9/site-packages/deeplake/util/check_latest_version.py:32: UserWarning: 有一个更新的deeplake版本(3.6.4)可用。建议使用`pip install -U deeplake`更新到最新版本。
      warnings.warn(
    


```python
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
```

## 最简单的方法，只指定类型

我们可以通过在模式中指定一些属性及其预期类型来开始


```python
schema = {
    "properties": {
        "sentiment": {"type": "string"},
        "aggressiveness": {"type": "integer"},
        "language": {"type": "string"},
    }
}
```


```python
chain = create_tagging_chain(schema, llm)
```

正如我们在示例中看到的，它正确地解释了我们的需求，但结果会有所不同，例如，不同语言的情感（'positive'、'enojado'等）。

我们将在下一节中看到如何控制这些结果。


```python
inp = "Estoy increiblemente contento de haberte conocido! Creo que seremos muy buenos amigos!"
chain.run(inp)
```




    {'sentiment': 'positive', 'language': 'Spanish'}




```python
inp = "Estoy muy enojado con vos! Te voy a dar tu merecido!"
chain.run(inp)
```




    {'sentiment': 'enojado', 'aggressiveness': 1, 'language': 'Spanish'}




```python
inp = "Weather is ok here, I can go outside without much more than a coat"
chain.run(inp)
```




    {'sentiment': 'positive', 'aggressiveness': 0, 'language': 'English'}



## 更多控制

通过聪明地定义模式，我们可以更好地控制模型的输出。具体而言，我们可以定义以下内容:

- 每个属性的可能值
- 描述以确保模型理解属性
- 要返回的必需属性

以下是如何使用_enum_、_description_和_required_来控制之前提到的每个方面的示例:


```python
schema = {
    "properties": {
        "sentiment": {"type": "string", "enum": ["happy", "neutral", "sad"]},
        "aggressiveness": {
            "type": "integer",
            "enum": [1, 2, 3, 4, 5],
            "description": "描述语句的侵略性程度，数字越大，侵略性越大",
        },
        "language": {
            "type": "string",
            "enum": ["spanish", "english", "french", "german", "italian"],
        },
    },
    "required": ["language", "sentiment", "aggressiveness"],
}
```


```python
chain = create_tagging_chain(schema, llm)
```

现在答案好多了！


```python
inp = "Estoy increiblemente contento de haberte conocido! Creo que seremos muy buenos amigos!"
chain.run(inp)
```




    {'sentiment': 'happy', 'aggressiveness': 0, 'language': 'spanish'}




```python
inp = "Estoy muy enojado con vos! Te voy a dar tu merecido!"
chain.run(inp)
```




    {'sentiment': 'sad', 'aggressiveness': 10, 'language': 'spanish'}




```python
inp = "Weather is ok here, I can go outside without much more than a coat"
chain.run(inp)
```




    {'sentiment': 'neutral', 'aggressiveness': 0, 'language': 'english'}



## 使用Pydantic指定模式

我们还可以使用Pydantic模式来指定所需的属性和类型。我们还可以发送其他参数，例如'enum'或'description'，如下面的示例所示。

通过使用`create_tagging_chain_pydantic`函数，我们可以将Pydantic模式作为输入发送，并且输出将是符合我们期望的模式的实例化对象。

通过这种方式，我们可以像在Python中定义新类或函数一样指定我们的模式-使用纯粹的Python类型。


```python
from enum import Enum
from pydantic import BaseModel, Field
```


```python
class Tags(BaseModel):
    sentiment: str = Field(..., enum=["happy", "neutral", "sad"])
    aggressiveness: int = Field(
        ...,
        description="描述语句的侵略性程度，数字越大，侵略性越大",
        enum=[1, 2, 3, 4, 5],
    )
    language: str = Field(
        ..., enum=["spanish", "english", "french", "german", "italian"]
    )
```


```python
chain = create_tagging_chain_pydantic(Tags, llm)
```


```python
inp = "Estoy muy enojado con vos! Te voy a dar tu merecido!"
res = chain.run(inp)
```


```python
res
```




    Tags(sentiment='sad', aggressiveness=10, language='spanish')


