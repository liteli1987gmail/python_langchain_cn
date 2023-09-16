# CSV 代理

这个笔记本展示了如何使用代理与 csv 进行交互。主要优化了问答功能。

**注意**: 这个代理在内部调用了 Pandas DataFrame 代理，而 Pandas DataFrame 代理又调用了 Python 代理，后者执行 LLM 生成的 Python 代码 - 如果 LLM 生成的 Python 代码有害的话，这可能会造成问题。请谨慎使用。

```python
from langchain.agents import create_csv_agent
```

```python
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
```

## 使用 ZERO_SHOT_REACT_DESCRIPTION

这展示了如何使用 ZERO_SHOT_REACT_DESCRIPTION 代理类型初始化代理。请注意，这是上述方法的另一种选择。

```python
agent = create_csv_agent(
    OpenAI(temperature=0),
    "titanic.csv",
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)
```

## 使用 OpenAI 函数

这展示了如何使用 OPENAI_FUNCTIONS 代理类型初始化代理。请注意，这是上述方法的另一种选择。

```python
agent = create_csv_agent(
    ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613"),
    "titanic.csv",
    verbose=True,
    agent_type=AgentType.OPENAI_FUNCTIONS,
)
```

```python
agent.run("有多少行数据？")
```

    Error in on_chain_start callback: 'name'
    

    [32;1m[1;3m
    调用: `python_repl_ast`，使用 `df.shape[0]`
    
    
    [0m[36;1m[1;3m891[0m[32;1m[1;3m数据框中有 891 行数据。[0m
    
    [1m> 完成链。[0m
    



    '数据框中有 891 行数据。'



```python
agent.run("how many people have more than 3 siblings")
```

    Error in on_chain_start callback: 'name'
    

    [32;1m[1;3m
    Invoking: `python_repl_ast` with `df[df['SibSp'] > 3]['PassengerId'].count()`
    
    
    [0m[36;1m[1;3m30[0m[32;1m[1;3mThere are 30 people in the dataframe who have more than 3 siblings.[0m
    
    [1m> Finished chain.[0m
    



    '数据框中有 30 人有超过 3 个兄弟姐妹。'



```python
agent.run("平均年龄的平方根是多少？")
```

    在 on_chain_start 回调中出现错误: 'name'
    

    [32;1m[1;3m
    Invoking: `python_repl_ast` with `import pandas as pd
    import math
    
    # Create a dataframe
    data = {'Age': [22, 38, 26, 35, 35]}
    df = pd.DataFrame(data)
    
    # 计算平均年龄
    average_age = df['Age'].mean()
    
    # 计算平均年龄的平方根
    square_root = math.sqrt(average_age)
    
    square_root`
    
    
    [0m[36;1m[1;3m5.585696017507576[0m[32;1m[1;3m平均年龄的平方根约为 5.59。[0m
    
    [1m> Finished chain.[0m
    




    'The square root of the average age is approximately 5.59.'



### Multi CSV Example

接下来的部分展示了代理程序如何与作为列表传递的多个CSV文件进行交互。

```python
agent = create_csv_agent(
    ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613"),
    ["titanic.csv", "titanic_age_fillna.csv"],
    verbose=True,
    agent_type=AgentType.OPENAI_FUNCTIONS,
)
agent.run("how many rows in the age column are different between the two dfs?")
```

    Error in on_chain_start callback: 'name'
    
    
    [32;1m[1;3m
    Invoking: `python_repl_ast` with `df1['Age'].nunique() - df2['Age'].nunique()`
    
    
    [0m[36;1m[1;3m-1[0m[32;1m[1;3mThere is 1 row in the age column that is different between the two dataframes.[0m
    
    [1m> Finished chain.[0m
    



    'There is 1 row in the age column that is different between the two dataframes.'



```python

```