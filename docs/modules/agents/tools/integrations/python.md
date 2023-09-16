# Python REPL
有时候，对于复杂的计算，与其让LLM直接生成答案，不如让LLM生成计算答案的代码，然后运行该代码来获得答案。为了方便这样做，我们提供了一个简单的Python REPL来执行命令。

这个接口只会返回打印出来的内容 - 因此，如果您想使用它来计算答案，请确保它打印出答案。

```python
from langchain.agents import Tool
from langchain.utilities import PythonREPL
```

```python
python_repl = PythonREPL()
```

```python
python_repl.run("print(1+1)")
```


    '2\n'


```python
# 您可以创建一个工具来传递给一个代理
repl_tool = Tool(
    name="python_repl",
    description="一个Python shell。使用它来执行python命令。输入应该是一个有效的python命令。如果你想看到一个值的输出，你应该用`print(...)`打印出来。",
    func=python_repl.run,
)
```