# 操纵输入和输出

RunnableParallel可以用于操纵一个Runnable的输出，以匹配序列中下一个Runnable的输入格式。

在这里，prompt的输入应该是一个带有"context"和"question"键的映射。用户输入只是问题。所以我们需要使用我们的检索器获取上下文，并将用户输入通过"question"键传递。

```python
%pip install --upgrade --quiet  langchain langchain-openai
```

```python
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

vectorstore = FAISS.from_texts(
    ["harrison worked at kensho"], embedding=OpenAIEmbeddings()
)
retriever = vectorstore.as_retriever()
template = """Answer the question based only on the following context:
{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)
model = ChatOpenAI()

retrieval_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

retrieval_chain.invoke("where did harrison work?")
```

::: {.callout-tip}
请注意，当将RunnableParallel与另一个Runnable组合时，我们甚至不需要将字典包装在RunnableParallel类中 - 类型转换会为我们处理。在链的上下文中，这些是等效的：
:::

```
{"context": retriever, "question": RunnablePassthrough()}
```

```
RunnableParallel({"context": retriever, "question": RunnablePassthrough()})
```

```
RunnableParallel(context=retriever, question=RunnablePassthrough())
```

## 使用itemgetter作为简写

请注意，您可以使用Python的`itemgetter`作为简写，从映射中提取数据，与`RunnableParallel`结合使用。有关itemgetter的更多信息，请参阅[Python文档](https://docs.python.org/3/library/operator.html#operator.itemgetter)。

在下面的示例中，我们使用itemgetter从映射中提取特定的键：

```python
from operator import itemgetter

from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

vectorstore = FAISS.from_texts(
    ["harrison worked at kensho"], embedding=OpenAIEmbeddings()
)
retriever = vectorstore.as_retriever()

template = """Answer the question based only on the following context:
{context}

Question: {question}

Answer in the following language: {language}
"""
prompt = ChatPromptTemplate.from_template(template)

chain = (
    {
        "context": itemgetter("question") | retriever,
        "question": itemgetter("question"),
        "language": itemgetter("language"),
    }
    | prompt
    | model
    | StrOutputParser()
)

chain.invoke({"question": "where did harrison work", "language": "italian"})
```

## 并行化步骤

RunnableParallel（又名RunnableMap）可以轻松地并行执行多个Runnables，并将这些Runnables的输出作为映射返回。

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel
from langchain_openai import ChatOpenAI

model = ChatOpenAI()
joke_chain = ChatPromptTemplate.from_template("tell me a joke about {topic}") | model
poem_chain = (
    ChatPromptTemplate.from_template("write a 2-line poem about {topic}") | model
)

map_chain = RunnableParallel(joke=joke_chain, poem=poem_chain)

map_chain.invoke({"topic": "bear"})
```

## 并行性

RunnableParallel还可用于并行运行独立的进程，因为映射中的每个Runnable都是并行执行的。例如，我们可以看到我们之前的`joke_chain`，`poem_chain`和`map_chain`的运行时间大致相同，即使`map_chain`执行了这两个Runnable。

```python
%%timeit

joke_chain.invoke({"topic": "bear"})
```

```python
%%timeit

poem_chain.invoke({"topic": "bear"})
```

```python
%%timeit

map_chain.invoke({"topic": "bear"})
```
