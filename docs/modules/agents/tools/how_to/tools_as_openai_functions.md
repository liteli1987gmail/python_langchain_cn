# Tools as OpenAI Functions

本笔记本介绍了如何将LangChain工具用作OpenAI函数。


```python
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
```


```python
model = ChatOpenAI(model="gpt-3.5-turbo-0613")
```


```python
from langchain.tools import MoveFileTool, format_tool_to_openai_function
```


```python
tools = [MoveFileTool()]
functions = [format_tool_to_openai_function(t) for t in tools]
```


```python
message = model.predict_messages(
    [HumanMessage(content="move file foo to bar")], functions=functions
)
```


```python
message
```




    AIMessage(content='', additional_kwargs={'function_call': {'name': 'move_file', 'arguments': '{\n  "source_path": "foo",\n  "destination_path": "bar"\n}'}}, example=False)




```python
message.additional_kwargs["function_call"]
```




    {'name': 'move_file',
     'arguments': '{\n  "source_path": "foo",\n  "destination_path": "bar"\n}'}




```python

```
