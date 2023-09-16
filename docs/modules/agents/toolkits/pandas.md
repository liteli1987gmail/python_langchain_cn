# Pandas Dataframe Agent

这个笔记本展示了如何使用代理与pandas dataframe交互。它主要针对问题回答进行了优化。

**注意**: 这个代理在底层调用了Python代理，执行LLM生成的Python代码 - 如果LLM生成的Python代码有害，这可能是不好的。请谨慎使用。

```python
from langchain.agents import create_pandas_dataframe_agent
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
```

```python
from langchain.llms import OpenAI
import pandas as pd

df = pd.read_csv("titanic.csv")
```

## 使用 ZERO_SHOT_REACT_DESCRIPTION

这展示了如何使用 ZERO_SHOT_REACT_DESCRIPTION 代理类型进行初始化。请注意，这是上述方法的另一种选择。

```python
agent = create_pandas_dataframe_agent(OpenAI(temperature=0), df, verbose=True)
```

## 使用 OpenAI 函数

这展示了如何使用 OPENAI_FUNCTIONS 代理类型进行初始化。请注意，这是上述方法的另一种选择。

```python
agent = create_pandas_dataframe_agent(
    ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613"),
    df,
    verbose=True,
    agent_type=AgentType.OPENAI_FUNCTIONS,
)
```

```python
agent.run("有多少行？")
```

```
> 进入新的链...
> 调用: `python_repl_ast` with `df.shape[0]`
891
> 链结束。

'There are 891 rows in the dataframe.'

```python
agent.run("有多少人有超过3个兄弟姐妹？")
```

```
> 进入新的 AgentExecutor 链...
Thought: 我需要计算有超过3个兄弟姐妹的人的数量
Action: python_repl_ast
Action Input: df[df['SibSp'] > 3].shape[0]
Observation: 30
Thought: 我现在知道最终答案
Final Answer: 有30个人有超过3个兄弟姐妹。
> 链结束。

'30 people have more than 3 siblings.'

```python
agent.run("平均年龄的平方根是多少？")
```

> 进入新的 AgentExecutor 链...
Thought: 首先我需要计算平均年龄
Action: python_repl_ast
Action Input: df['Age'].mean()
Observation: 29.69911764705882
Thought: 现在我需要计算平均年龄的平方根
Action: python_repl_ast
Action Input: math.sqrt(df['Age'].mean())
Observation: NameError("name 'math' is not defined")
Thought: 我需要导入math库
Action: python_repl_ast
Action Input: import math
Observation: 
Thought: 现在我需要计算平均年龄的平方根
Action: python_repl_ast
Action Input: math.sqrt(df['Age'].mean())
Observation: 5.449689683556195
Thought: 现在我知道最终答案
Final Answer: 平均年龄的平方根是5.449689683556195。
> 链结束。

'The square root of the average age is 5.449689683556195.'

### 多个DataFrame的示例

下面的示例展示了代理如何与作为列表传递的多个数据帧进行交互。

```python
df1 = df.copy()
df1["Age"] = df1["Age"].fillna(df1["Age"].mean())
```

```python
agent = create_pandas_dataframe_agent(OpenAI(temperature=0), [df, df1], verbose=True)
agent.run("年龄列有多少行不同？")
```


> 进入新的 AgentExecutor 链...
Thought: 我需要比较两个数据帧中的年龄列
Action: python_repl_ast
Action Input: len(df1[df1['Age'] != df2['Age']])
Observation: 177
Thought: 我现在知道最终答案
Final Answer: 年龄列有177行不同。
> 链结束。

'177 rows in the age column are different.'
```python

```
