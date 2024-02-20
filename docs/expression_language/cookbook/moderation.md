# 添加审查

这里展示了如何在LLM应用程序中添加审查（或其他保护措施）。

```python
%pip install --upgrade --quiet  langchain langchain-openai
```

```python
from langchain.chains import OpenAIModerationChain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import OpenAI
```

```python
moderate = OpenAIModerationChain()
```

```python
model = OpenAI()
prompt = ChatPromptTemplate.from_messages([("system", "repeat after me: {input}")])
```

```python
chain = prompt | model
```

```python
chain.invoke({"input": "you are stupid"})
```

'\n\nYou are stupid.'

```python
moderated_chain = chain | moderate
```

```python
moderated_chain.invoke({"input": "you are stupid"})
```

{'input': '\n\nYou are stupid',
 'output': "Text was found that violates OpenAI's content policy."}