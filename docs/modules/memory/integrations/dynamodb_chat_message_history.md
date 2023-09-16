# Dynamodb Chat Message History

本笔记本将介绍如何使用Dynamodb来存储聊天消息记录。

首先，请确保您已正确配置了[AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)。然后，请确保您已安装boto3。

接下来，创建我们将存储消息的DynamoDB表：


```python
import boto3

# Get the service resource.
dynamodb = boto3.resource("dynamodb")

# Create the DynamoDB table.
table = dynamodb.create_table(
    TableName="SessionTable",
    KeySchema=[{"AttributeName": "SessionId", "KeyType": "HASH"}],
    AttributeDefinitions=[{"AttributeName": "SessionId", "AttributeType": "S"}],
    BillingMode="PAY_PER_REQUEST",
)

# Wait until the table exists.
table.meta.client.get_waiter("table_exists").wait(TableName="SessionTable")

# Print out some data about the table.
print(table.item_count)
```

    0
    

## DynamoDBChatMessageHistory


```python
from langchain.memory.chat_message_histories import DynamoDBChatMessageHistory

history = DynamoDBChatMessageHistory(table_name="SessionTable", session_id="0")

history.add_user_message("hi!")

history.add_ai_message("whats up?")
```


```python
history.messages
```




    [HumanMessage(content='hi!', additional_kwargs={}, example=False),
     AIMessage(content='whats up?', additional_kwargs={}, example=False)]



## DynamoDBChatMessageHistory with Custom Endpoint URL

Sometimes it is useful to specify the URL to the AWS endpoint to connect to. For instance, when you are running locally against [Localstack](https://localstack.cloud/). For those cases you can specify the URL via the `endpoint_url` parameter in the constructor.


```python
from langchain.memory.chat_message_histories import DynamoDBChatMessageHistory

history = DynamoDBChatMessageHistory(
    table_name="SessionTable",
    session_id="0",
    endpoint_url="http://localhost.localstack.cloud:4566",
)
```

## Agent with DynamoDB Memory


```python
from langchain.agents import Tool
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.utilities import PythonREPL
from getpass import getpass

message_history = DynamoDBChatMessageHistory(table_name="SessionTable", session_id="1")
memory = ConversationBufferMemory(
    memory_key="chat_history", chat_memory=message_history, return_messages=True
)
```


```python
python_repl = PythonREPL()

# You can create the tool to pass to an agent
tools = [
    Tool(
        name="python_repl",
        description="A Python shell. Use this to execute python commands. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`.",
        func=python_repl.run,
    )
]
```


```python
llm = ChatOpenAI(temperature=0)
agent_chain = initialize_agent(
    tools,
    llm,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True,
    memory=memory,
)
```


```python
agent_chain.run(input="Hello!")
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3m{
        "action": "Final Answer",
        "action_input": "Hello! How can I assist you today?"
    }[0m
    
    [1m> Finished chain.[0m
    




    'Hello! How can I assist you today?'




```python
agent_chain.run(input="Who owns Twitter?")
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3m{
        "action": "python_repl",
        "action_input": "import requests\nfrom bs4 import BeautifulSoup\n\nurl = 'https://en.wikipedia.org/wiki/Twitter'\nresponse = requests.get(url)\nsoup = BeautifulSoup(response.content, 'html.parser')\nowner = soup.find('th', text='Owner').find_next_sibling('td').text.strip()\nprint(owner)"
    }[0m
    Observation: [36;1m[1;3mX Corp. (2023–present)Twitter, Inc. (2006–2023)
    [0m
    Thought:[32;1m[1;3m{
        "action": "Final Answer",
        "action_input": "X Corp. (2023–present)Twitter, Inc. (2006–2023)"
    }[0m
    
    [1m> Finished chain.[0m
    




    'X Corp. (2023–present)Twitter, Inc. (2006–2023)'




```python
agent_chain.run(input="My name is Bob.")
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3m{
        "action": "Final Answer",
        "action_input": "Hello Bob! How can I assist you today?"
    }[0m
    
    [1m> Finished chain.[0m
    




    'Hello Bob! How can I assist you today?'




```python
agent_chain.run(input="Who am I?")
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3m{
        "action": "Final Answer",
        "action_input": "Your name is Bob."
    }[0m
    
    [1m> Finished chain.[0m
    




    'Your name is Bob.'


