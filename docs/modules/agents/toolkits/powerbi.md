# PowerBI Dataset Agent

这个笔记本展示了一个与Power BI数据集交互的代理。代理旨在回答关于数据集的更一般的问题，并从错误中恢复。

请注意，由于这个代理处于积极开发中，所有的回答可能不正确。它运行在[executequery端点](https://learn.microsoft.com/en-us/rest/api/power-bi/datasets/execute-queries)上，该端点不允许删除操作。

### 一些注意事项
- 它依赖于azure.identity包进行身份验证，可以使用`pip install azure-identity`安装。或者，您可以在不提供凭据的情况下，使用一个字符串作为令牌创建powerbi数据集。
- 您还可以提供一个用户名来模拟启用了RLS的数据集的使用。
- 该工具包使用LLM从问题创建查询，代理使用LLM进行整体执行。
- 测试主要使用`text-davinci-003`模型进行，codex模型似乎表现不佳。

## 初始化

```python
from langchain.agents.agent_toolkits import create_pbi_agent
from langchain.agents.agent_toolkits import PowerBIToolkit
from langchain.utilities.powerbi import PowerBIDataset
from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentExecutor
from azure.identity import DefaultAzureCredential
```


```python
fast_llm = ChatOpenAI(
    temperature=0.5, max_tokens=1000, model_name="gpt-3.5-turbo", verbose=True
)
smart_llm = ChatOpenAI(temperature=0, max_tokens=100, model_name="gpt-4", verbose=True)

toolkit = PowerBIToolkit(
    powerbi=PowerBIDataset(
        dataset_id="<dataset_id>",
        table_names=["table1", "table2"],
        credential=DefaultAzureCredential(),
    ),
    llm=smart_llm,
)

agent_executor = create_pbi_agent(
    llm=fast_llm,
    toolkit=toolkit,
    verbose=True,
)
```

## 示例: 描述一个表

```python
agent_executor.run("Describe table1")
```

## 示例: 在表上运行简单查询
在这个例子中，代理实际上找出了获取表的行数的正确查询。

```python
agent_executor.run("How many records are in table1?")
```

## 示例: 运行查询

```python
agent_executor.run("How many records are there by dimension1 in table2?")
```

```python
agent_executor.run("What unique values are there for dimensions2 in table2")
```

## 示例: 添加自己的few-shot提示

```python
# 虚构的例子
few_shots = """
Question: How many rows are in the table revenue?
DAX: EVALUATE ROW("Number of rows", COUNTROWS(revenue_details))
----
Question: How many rows are in the table revenue where year is not empty?
DAX: EVALUATE ROW("Number of rows", COUNTROWS(FILTER(revenue_details, revenue_details[year] <> "")))
----
Question: What was the average of value in revenue in dollars?
DAX: EVALUATE ROW("Average", AVERAGE(revenue_details[dollar_value]))
----
"""

toolkit = PowerBIToolkit(
    powerbi=PowerBIDataset(
        dataset_id="<dataset_id>",
        table_names=["table1", "table2"],
        credential=DefaultAzureCredential(),
    ),
    llm=smart_llm,
    examples=few_shots,
)

agent_executor = create_pbi_agent(
    llm=fast_llm,
    toolkit=toolkit,
    verbose=True,
)
```


```python
agent_executor.run("What was the maximum of value in revenue in dollars in 2022?")
```
