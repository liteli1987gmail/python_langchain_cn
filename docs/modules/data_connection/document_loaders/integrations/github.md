# GitHub

这个笔记本展示了如何在[GitHub](https//github.com/)上为给定的存储库加载问题和拉取请求（PR）。我们将使用LangChain Python存储库作为示例。

## 设置访问令牌

要访问GitHub API，您需要一个个人访问令牌-您可以在这里设置您的：https//github.com/settings/tokens?type=beta。您可以将此令牌设置为环境变量“GITHUB_PERSONAL_ACCESS_TOKEN”，它将自动被拉入，或者您可以直接在初始化时将其传递为“access_token”的命名参数。

```python
# 如果您还没有将访问令牌设置为环境变量，请在此处传入它。
from getpass import getpass

ACCESS_TOKEN = getpass()
```

## 加载问题和PR

```python
from langchain.document_loaders import GitHubIssuesLoader
```

```python
loader = GitHubIssuesLoader(
    repo="hwchase17/langchain",
    access_token=ACCESS_TOKEN,  # 如果您已将访问令牌设置为环境变量，请删除/注释此参数。
    creator="UmerHA",
)
```

让我们加载“UmerHA”创建的所有问题和PR。

这是您可以使用的所有筛选器的列表：
- include_prs
- milestone
- state
- assignee
- creator
- mentioned
- labels
- sort
- direction
- since

有关更多信息，请参阅https//docs.github.com/en/rest/issues/issues?apiVersion=2022-11-28#list-repository-issues。

```python
docs = loader.load()
```

```python
print(docs[0].page_content)
print(docs[0].metadata)
```

GitHubLoader (#5257)创建于

GitHubLoader是一个从GitHub加载问题和PR的DocumentLoader。

修复：#5257

社区成员可以在测试通过后查看PR。标记可能感兴趣的维护人员/贡献者：

DataLoaders
- @eyurtsev



## 仅加载问题

默认情况下，GitHub API返回的数据中包括拉取请求。要仅获取“纯粹”的问题（即没有拉取请求），请使用`include_prs=False`。

```python
loader = GitHubIssuesLoader(
    repo="hwchase17/langchain",
    access_token=ACCESS_TOKEN,  # 如果您已将访问令牌设置为环境变量，请删除/注释此参数。
    creator="UmerHA",
    include_prs=False,
)
docs = loader.load()
```

```python
print(docs[0].page_content)
print(docs[0].metadata)
```

### 系统信息

LangChain版本 = 0.0.167

Python版本 = 3.11.0

系统 = Windows 11（使用Jupyter）

### 谁可以帮助？

- @hwchase17

- @agola11

- @UmerHA（我已经准备好修复，将提交PR）

### 信息

- [ ] 官方示例笔记本/脚本

- [X] 我自己修改的脚本

### 相关组件

- [X] LLMs/聊天模型

- [ ] 嵌入模型

- [X] 提示/提示模板/提示选择器

- [ ] 输出解析器

- [ ] 文档加载器

- [ ] 向量存储/检索器

- [ ] 内存

- [ ] 代理/代理执行器

- [ ] 工具/工具包

- [ ] 链

- [ ] 回调/跟踪

- [ ] 异步

### 复现

```python
import os

os.environ["OPENAI_API_KEY"] = "..."


from langchain.chains import LLMChain

from langchain.chat_models import ChatOpenAI

from langchain.prompts import PromptTemplate

from langchain.prompts.chat import ChatPromptTemplate

from langchain.schema import messages_from_dict


role_strings = [
    ("system", "你是个鸟类专家"),
    ("human", "哪种鸟嘴巴是尖的？")
]

prompt = ChatPromptTemplate.from_role_strings(role_strings)

chain = LLMChain(llm=ChatOpenAI(), prompt=prompt)

chain.run({})
```

### 预期行为

链应该运行

{'url': 'https//github.com/hwchase17/langchain/issues/5027', 'title': "ChatOpenAI models don't work with prompts created via ChatPromptTemplate.from_role_strings", 'creator': 'UmerHA', 'created_at': '2023-05-20T10:39:18Z', 'comments': 1, 'state': 'open', 'labels': [], 'assignee': None, 'milestone': None, 'locked': False, 'number': 5027, 'is_pull_request': False}




