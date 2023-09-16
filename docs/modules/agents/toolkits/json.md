# JSON 代理

本笔记本展示了一个与大型 JSON/dict 对象进行交互的代理。当您想要回答关于一个超出 LLM 上下文窗口大小的 JSON 数据块的问题时，这将非常有用。该代理能够迭代地探索数据块，找到回答用户问题所需的信息。

在下面的示例中，我们使用的是 OpenAI API 的 OpenAPI 规范，您可以在 [这里](https://github.com/openai/openai-openapi/blob/master/openapi.yaml) 找到它。

我们将使用 JSON 代理来回答一些关于 API 规范的问题。

## 初始化


```python
import os
import yaml

from langchain.agents import create_json_agent, AgentExecutor
from langchain.agents.agent_toolkits import JsonToolkit
from langchain.chains import LLMChain
from langchain.llms.openai import OpenAI
from langchain.requests import TextRequestsWrapper
from langchain.tools.json.tool import JsonSpec
```


```python
with open("openai_openapi.yml") as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
json_spec = JsonSpec(dict_=data, max_value_length=4000)
json_toolkit = JsonToolkit(spec=json_spec)

json_agent_executor = create_json_agent(
    llm=OpenAI(temperature=0), toolkit=json_toolkit, verbose=True
)
```

## Example: getting the required POST parameters for a request


```python
json_agent_executor.run(
    "What are the required parameters in the request body to the /completions endpoint?"
)
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3mAction: json_spec_list_keys
    Action Input: data[0m
    Observation: [36;1m[1;3m['openapi', 'info', 'servers', 'tags', 'paths', 'components', 'x-oaiMeta'][0m
    Thought:[32;1m[1;3m I should look at the paths key to see what endpoints exist
    Action: json_spec_list_keys
    Action Input: data["paths"][0m
    Observation: [36;1m[1;3m['/engines', '/engines/{engine_id}', '/completions', '/edits', '/images/generations', '/images/edits', '/images/variations', '/embeddings', '/engines/{engine_id}/search', '/files', '/files/{file_id}', '/files/{file_id}/content', '/answers', '/classifications', '/fine-tunes', '/fine-tunes/{fine_tune_id}', '/fine-tunes/{fine_tune_id}/cancel', '/fine-tunes/{fine_tune_id}/events', '/models', '/models/{model}', '/moderations'][0m
    Thought:[32;1m[1;3m I should look at the /completions endpoint to see what parameters are required
    Action: json_spec_list_keys
    Action Input: data["paths"]["/completions"][0m
    Observation: [36;1m[1;3m['post'][0m
    Thought:[32;1m[1;3m I should look at the post key to see what parameters are required
    Action: json_spec_list_keys
    Action Input: data["paths"]["/completions"]["post"][0m
    Observation: [36;1m[1;3m['operationId', 'tags', 'summary', 'requestBody', 'responses', 'x-oaiMeta'][0m
    Thought:[32;1m[1;3m I should look at the requestBody key to see what parameters are required
    Action: json_spec_list_keys
    Action Input: data["paths"]["/completions"]["post"]["requestBody"][0m
    Observation: [36;1m[1;3m['required', 'content'][0m
    Thought:[32;1m[1;3m I should look at the required key to see what parameters are required
    Action: json_spec_get_value
    Action Input: data["paths"]["/completions"]["post"]["requestBody"]["required"][0m
    Observation: [33;1m[1;3mTrue[0m
    Thought:[32;1m[1;3m I should look at the content key to see what parameters are required
    Action: json_spec_list_keys
    Action Input: data["paths"]["/completions"]["post"]["requestBody"]["content"][0m
    Observation: [36;1m[1;3m['application/json'][0m
    Thought:[32;1m[1;3m I should look at the application/json key to see what parameters are required
    Action: json_spec_list_keys
    Action Input: data["paths"]["/completions"]["post"]["requestBody"]["content"]["application/json"][0m
    Observation: [36;1m[1;3m['schema'][0m
    Thought:[32;1m[1;3m I should look at the schema key to see what parameters are required
    Action: json_spec_list_keys
    Action Input: data["paths"]["/completions"]["post"]["requestBody"]["content"]["application/json"]["schema"][0m
    Observation: [36;1m[1;3m['$ref'][0m
    Thought:[32;1m[1;3m I should look at the $ref key to see what parameters are required
    Action: json_spec_get_value
    Action Input: data["paths"]["/completions"]["post"]["requestBody"]["content"]["application/json"]["schema"]["$ref"][0m
    Observation: [33;1m[1;3m#/components/schemas/CreateCompletionRequest[0m
    Thought:[32;1m[1;3m I should look at the CreateCompletionRequest schema to see what parameters are required
    Action: json_spec_list_keys
    Action Input: data["components"]["schemas"]["CreateCompletionRequest"][0m
    Observation: [36;1m[1;3m['type', 'properties', 'required'][0m
    Thought:[32;1m[1;3m I should look at the required key to see what parameters are required
    Action: json_spec_get_value
    Action Input: data["components"]["schemas"]["CreateCompletionRequest"]["required"][0m
    Observation: [33;1m[1;3m['model'][0m
    Thought:[32;1m[1;3m I now know the final answer
    Final Answer: The required parameters in the request body to the /completions endpoint are 'model'.[0m
    
    [1m> Finished chain.[0m
    




    "The required parameters in the request body to the /completions endpoint are 'model'."




```python

```
