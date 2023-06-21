# Shale Protocol

[Shale Protocol](https://shaleprotocol.com) 提供了开放的LLM生产级推理API。它是一个即插即用的API，托管在高度可扩展的GPU云基础设施上。

我们的免费套餐支持每个密钥每天最多1K个请求，因为我们希望消除任何人开始使用LLM构建genAI应用的障碍。

使用Shale Protocol，开发人员/研究人员可以免费创建应用程序并探索开放LLM的能力。

本页面介绍了如何将Shale-Serve API与LangChain集成。

截至2023年6月，默认情况下，API支持Vicuna-13B。我们将在未来的版本中支持更多的LLM，如Falcon-40B。


## 如何操作

### 1. 在https://shaleprotocol.com上找到我们的Discord链接。通过我们的Discord上的"Shale Bot"生成API密钥。无需信用卡，也没有免费试用。这是一个每个API密钥每天1K限制的永久免费套餐。

### 2. 使用https://shale.live/v1作为OpenAI API的替代

例如
```python
from langchain.llms import OpenAI
from langchain import PromptTemplate, LLMChain

import os
os.environ['OPENAI_API_BASE'] = "https://shale.live/v1"
os.environ['OPENAI_API_KEY'] = "ENTER YOUR API KEY"

llm = OpenAI()

template = """Question: {question}

# Answer: Let's think step by step."""

prompt = PromptTemplate(template=template, input_variables=["question"])

llm_chain = LLMChain(prompt=prompt, llm=llm)

question = "What NFL team won the Super Bowl in the year Justin Beiber was born?"

llm_chain.run(question)

```
