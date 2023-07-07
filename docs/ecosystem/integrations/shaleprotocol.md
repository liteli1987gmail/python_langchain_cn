# Shale Protocol

[Shale Protocol](https://shaleprotocol.com) 提供了开放的 LLM 生产级推理 API。它是一个即插即用的 API，托管在高度可扩展的 GPU 云基础设施上。

我们的免费套餐支持每个密钥每天最多 1K 个请求，因为我们希望消除任何人开始使用 LLM 构建 genAI 应用的障碍。

使用 Shale Protocol，开发人员/研究人员可以免费创建应用程序并探索开放 LLM 的能力。

本页面介绍了如何将 Shale-Serve API 与 LangChain 集成。

截至 2023 年 6 月，默认情况下，API 支持 Vicuna-13B。我们将在未来的版本中支持更多的 LLM，如 Falcon-40B。


## 如何操作

### 1. 在 https://shaleprotocol.com 上找到我们的 Discord 链接。通过我们的 Discord 上的 "Shale Bot" 生成 API 密钥。无需信用卡，也没有免费试用。这是一个每个 API 密钥每天 1K 限制的永久免费套餐。

### 2. 使用 https://shale.live/v1 作为 OpenAI API 的替代

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
