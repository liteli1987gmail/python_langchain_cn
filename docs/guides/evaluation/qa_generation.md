# QA生成
本笔记本展示了如何使用`QAGenerationChain`来生成特定文档的问题-答案对。
这很重要，因为通常情况下，您可能没有数据来评估您的问答系统，所以这是一种廉价且轻量级的生成方法！


```python
from langchain.document_loaders import TextLoader
```


```python
loader = TextLoader("../../modules/state_of_the_union.txt")
```


```python
doc = loader.load()[0]
```


```python
from langchain.chat_models import ChatOpenAI
from langchain.chains import QAGenerationChain

chain = QAGenerationChain.from_llm(ChatOpenAI(temperature=0))
```


```python
qa = chain.run(doc.page_content)
```


```python
qa[1]
```




    {'question': '美国司法部正在采取什么行动来打击俄罗斯寡头的犯罪行为？',
     'answer': '美国司法部正在组建一个专门的工作组来打击俄罗斯寡头的犯罪行为。'}




```python

```
