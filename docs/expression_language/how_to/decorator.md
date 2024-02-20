# 使用`@chain`装饰器创建可运行对象

您还可以通过添加`@chain`装饰器将任意函数转换为链式函数。这在功能上等同于在[`RunnableLambda`](./functions)中进行包装。

这将通过正确跟踪您的链式函数来改善可观察性。在此函数内部对可运行对象的任何调用都将被跟踪为嵌套子项。

它还允许您像使用其他可运行对象一样使用它，将其组合在链式函数中等等。

让我们看看它的实际应用！

```python
%pip install --upgrade --quiet  langchain langchain-openai
```

```python
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import chain
from langchain_openai import ChatOpenAI
```

```python
prompt1 = ChatPromptTemplate.from_template("Tell me a joke about {topic}")
prompt2 = ChatPromptTemplate.from_template("What is the subject of this joke: {joke}")
```

```python
@chain
def custom_chain(text):
    prompt_val1 = prompt1.invoke({"topic": text})
    output1 = ChatOpenAI().invoke(prompt_val1)
    parsed_output1 = StrOutputParser().invoke(output1)
    chain2 = prompt2 | ChatOpenAI() | StrOutputParser()
    return chain2.invoke({"joke": parsed_output1})
```

`custom_chain`现在是一个可运行对象，这意味着您需要使用`invoke`来调用它。

```python
custom_chain.invoke("bears")
```

您应该在LangSmith跟踪中看到一个`custom_chain`跟踪项，其中包含对OpenAI的调用。

