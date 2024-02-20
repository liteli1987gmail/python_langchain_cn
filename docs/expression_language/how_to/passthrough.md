---
sidebar_position: 1
title: "RunnablePassthrough: 通过传递数据"
keywords: [RunnablePassthrough, RunnableParallel, LCEL]
---

# 通过传递数据

RunnablePassthrough允许传递输入数据，可以保持不变或添加额外的键。通常与RunnableParallel一起使用，将数据分配给映射中的新键。

RunnablePassthrough() 单独调用时，将简单地接收输入并传递。

使用assign参数调用RunnablePassthrough (`RunnablePassthrough.assign(...)`)，将接收输入，并添加传递给assign函数的额外参数。

请参考下面的示例：

```python
%pip install --upgrade --quiet  langchain langchain-openai
```

```python
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

runnable = RunnableParallel(
    passed=RunnablePassthrough(),
    extra=RunnablePassthrough.assign(mult=lambda x: x["num"] * 3),
    modified=lambda x: x["num"] + 1,
)

runnable.invoke({"num": 1})
```

如上所示，`passed` 键使用 `RunnablePassthrough()` 调用，因此它只是传递了 `{'num': 1}`。

在第二行中，我们使用了带有将数值乘以3的lambda的 `RunnablePastshrough.assign`。在这种情况下，`extra` 被设置为 `{'num': 1, 'mult': 3}`，即原始值加上 `mult` 键。

最后，我们还使用lambda在映射中设置了第三个键 `modified`，将num加1，结果为 `modified` 键的值为 `2`。

## 检索示例

在下面的示例中，我们看到了使用RunnablePassthrough和RunnableMap的用例。

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

在这里，prompt的输入预期是一个带有 "context" 和 "question" 键的映射。用户输入只是问题。因此，我们需要使用我们的retriever获取上下文，并将用户输入传递到 "question" 键下。在这种情况下，RunnablePassthrough允许我们将用户的问题传递给prompt和model。

=======