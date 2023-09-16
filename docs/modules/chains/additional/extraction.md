# 抽取

抽取链使用OpenAI的"functions"参数来指定从文档中抽取实体的模式。这样可以确保模型输出我们想要的实体和属性模式，并具有适当的类型。

当我们希望从同一段落中抽取多个实体及其属性时（例如：在这段文字中提到了哪些人？），可以使用抽取链。


```python
from langchain.chat_models import ChatOpenAI
from langchain.chains import create_extraction_chain, create_extraction_chain_pydantic
from langchain.prompts import ChatPromptTemplate
```

    /Users/harrisonchase/.pyenv/versions/3.9.1/envs/langchain/lib/python3.9/site-packages/deeplake/util/check_latest_version.py:32: UserWarning: deeplake有一个更新版本(3.6.4)可用。建议使用`pip install -U deeplake`来更新到最新版本。
      warnings.warn(
    


```python
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
```

## 抽取实体

要抽取实体，我们需要创建一个如下所示的模式，其中指定了我们要查找的所有属性及其期望的类型。我们还可以指定这些属性中哪些是必需的，哪些是可选的。


```python
schema = {
    "properties": {
        "person_name": {"type": "string"},
        "person_height": {"type": "integer"},
        "person_hair_color": {"type": "string"},
        "dog_name": {"type": "string"},
        "dog_breed": {"type": "string"},
    },
    "required": ["person_name", "person_height"],
}
```


```python
inp = """
Alex is 5 feet tall. Claudia is 1 feet taller Alex and jumps higher than him. Claudia is a brunette and Alex is blonde.
Alex's dog Frosty is a labrador and likes to play hide and seek.
        """
```


```python
chain = create_extraction_chain(schema, llm)
```

如我们所见，我们以所需的格式提取了必需的实体及其属性:


```python
chain.run(inp)
```




    [{'person_name': 'Alex',
      'person_height': 5,
      'person_hair_color': 'blonde',
      'dog_name': 'Frosty',
      'dog_breed': 'labrador'},
     {'person_name': 'Claudia',
      'person_height': 6,
      'person_hair_color': 'brunette'}]



## Pydantic示例

我们还可以使用Pydantic模式选择所需的属性和类型，并将那些不是严格要求的属性设置为“可选”。

通过使用`create_extraction_chain_pydantic`函数，我们可以将Pydantic模式作为输入发送，并且输出将是一个符合我们所需模式的实例化对象。

这样，我们可以以与在Python中创建新类或函数相同的方式指定模式-纯粹使用Python类型。


```python
from typing import Optional, List
from pydantic import BaseModel, Field
```


```python
class Properties(BaseModel):
    person_name: str
    person_height: int
    person_hair_color: str
    dog_breed: Optional[str]
    dog_name: Optional[str]
```


```python
chain = create_extraction_chain_pydantic(pydantic_schema=Properties, llm=llm)
```


```python
inp = """
Alex is 5 feet tall. Claudia is 1 feet taller Alex and jumps higher than him. Claudia is a brunette and Alex is blonde.
Alex's dog Frosty is a labrador and likes to play hide and seek.
        """
```

如我们所见，我们以所需的格式提取了必需的实体及其属性:


```python
chain.run(inp)
```




    [Properties(person_name='Alex', person_height=5, person_hair_color='blonde', dog_breed='labrador', dog_name='Frosty'),
     Properties(person_name='Claudia', person_height=6, person_hair_color='brunette', dog_breed=None, dog_name=None)]




```python

```
