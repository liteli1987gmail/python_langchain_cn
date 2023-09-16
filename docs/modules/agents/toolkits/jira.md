# Jira

本笔记本说明如何使用 Jira 工具。
Jira 工具允许代理与给定的 Jira 实例进行交互，执行搜索问题和创建问题等操作，该工具封装了 atlassian-python-api 库，更多信息请参阅：https://atlassian-python-api.readthedocs.io/jira.html

要使用此工具，您首先必须将以下内容设置为环境变量：
    JIRA_API_TOKEN
    JIRA_USERNAME
    JIRA_INSTANCE_URL


```python
%pip install atlassian-python-api
```


```python
import os
from langchain.agents import AgentType
from langchain.agents import initialize_agent
from langchain.agents.agent_toolkits.jira.toolkit import JiraToolkit
from langchain.llms import OpenAI
from langchain.utilities.jira import JiraAPIWrapper
```


```python
os.environ["JIRA_API_TOKEN"] = "abc"
os.environ["JIRA_USERNAME"] = "123"
os.environ["JIRA_INSTANCE_URL"] = "https://jira.atlassian.com"
os.environ["OPENAI_API_KEY"] = "xyz"
```


```python
llm = OpenAI(temperature=0)
jira = JiraAPIWrapper()
toolkit = JiraToolkit.from_jira_api_wrapper(jira)
agent = initialize_agent(
    toolkit.get_tools(), llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)
```


```python
agent.run("make a new issue in project PW to remind me to make more fried rice")
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3m I need to create an issue in project PW
    Action: Create Issue
    Action Input: {"summary": "Make more fried rice", "description": "Reminder to make more fried rice", "issuetype": {"name": "Task"}, "priority": {"name": "Low"}, "project": {"key": "PW"}}[0m
    Observation: [38;5;200m[1;3mNone[0m
    Thought:[32;1m[1;3m I now know the final answer
    Final Answer: A new issue has been created in project PW with the summary "Make more fried rice" and description "Reminder to make more fried rice".[0m
    
    [1m> Finished chain.[0m
    




    'A new issue has been created in project PW with the summary "Make more fried rice" and description "Reminder to make more fried rice".'


