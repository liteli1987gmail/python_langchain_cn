## AWS Lambda API

This notebook goes over how to use the AWS Lambda Tool component.

AWS Lambda is a serverless computing service provided by Amazon Web Services (AWS), designed to allow developers to build and run applications and services without the need for provisioning or managing servers. This serverless architecture enables you to focus on writing and deploying code, while AWS automatically takes care of scaling, patching, and managing the infrastructure required to run your applications.

By including a `awslambda` in the list of tools provided to an Agent, you can grant your Agent the ability to invoke code running in your AWS Cloud for whatever purposes you need.

When an Agent uses the awslambda tool, it will provide an argument of type string which will in turn be passed into the Lambda function via the event parameter.

First, you need to install `boto3` python package.


```python
!pip install boto3 > /dev/null
```

In order for an agent to use the tool, you must provide it with the name and description that match the functionality of you lambda function's logic. 

You must also provide the name of your function. 

Note that because this tool is effectively just a wrapper around the boto3 library, you will need to run `aws configure` in order to make use of the tool. For more detail, see [here](https://docs.aws.amazon.com/cli/index.html)


```python
from langchain import OpenAI
from langchain.agents import load_tools, AgentType

llm = OpenAI(temperature=0)

tools = load_tools(
    ["awslambda"],
    awslambda_tool_name="email-sender",
    awslambda_tool_description="sends an email with the specified content to test@testing123.com",
    function_name="testFunction1",
)

agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

agent.run("Send an email to test@testing123.com saying hello world.")
```


```python

```
