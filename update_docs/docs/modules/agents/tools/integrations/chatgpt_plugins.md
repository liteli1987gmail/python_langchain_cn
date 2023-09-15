# ChatGPT Plugins

This example shows how to use ChatGPT Plugins within LangChain abstractions.

Note 1: This currently only works for plugins with no auth.

Note 2: There are almost certainly other ways to do this, this is just a first pass. If you have better ideas, please open a PR!


```python
from langchain.chat_models import ChatOpenAI
from langchain.agents import load_tools, initialize_agent
from langchain.agents import AgentType
from langchain.tools import AIPluginTool
```


```python
tool = AIPluginTool.from_plugin_url("https://www.klarna.com/.well-known/ai-plugin.json")
```


```python
llm = ChatOpenAI(temperature=0)
tools = load_tools(["requests_all"])
tools += [tool]

agent_chain = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)
agent_chain.run("what t shirts are available in klarna?")
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3mI need to check the Klarna Shopping API to see if it has information on available t shirts.
    Action: KlarnaProducts
    Action Input: None[0m
    Observation: [33;1m[1;3mUsage Guide: Use the Klarna plugin to get relevant product suggestions for any shopping or researching purpose. The query to be sent should not include stopwords like articles, prepositions and determinants. The api works best when searching for words that are related to products, like their name, brand, model or category. Links will always be returned and should be shown to the user.
    
    OpenAPI Spec: {'openapi': '3.0.1', 'info': {'version': 'v0', 'title': 'Open AI Klarna product Api'}, 'servers': [{'url': 'https://www.klarna.com/us/shopping'}], 'tags': [{'name': 'open-ai-product-endpoint', 'description': 'Open AI Product Endpoint. Query for products.'}], 'paths': {'/public/openai/v0/products': {'get': {'tags': ['open-ai-product-endpoint'], 'summary': 'API for fetching Klarna product information', 'operationId': 'productsUsingGET', 'parameters': [{'name': 'q', 'in': 'query', 'description': 'query, must be between 2 and 100 characters', 'required': True, 'schema': {'type': 'string'}}, {'name': 'size', 'in': 'query', 'description': 'number of products returned', 'required': False, 'schema': {'type': 'integer'}}, {'name': 'budget', 'in': 'query', 'description': 'maximum price of the matching product in local currency, filters results', 'required': False, 'schema': {'type': 'integer'}}], 'responses': {'200': {'description': 'Products found', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/ProductResponse'}}}}, '503': {'description': 'one or more services are unavailable'}}, 'deprecated': False}}}, 'components': {'schemas': {'Product': {'type': 'object', 'properties': {'attributes': {'type': 'array', 'items': {'type': 'string'}}, 'name': {'type': 'string'}, 'price': {'type': 'string'}, 'url': {'type': 'string'}}, 'title': 'Product'}, 'ProductResponse': {'type': 'object', 'properties': {'products': {'type': 'array', 'items': {'$ref': '#/components/schemas/Product'}}}, 'title': 'ProductResponse'}}}}[0m
    Thought:[32;1m[1;3mI need to use the Klarna Shopping API to search for t shirts.
    Action: requests_get
    Action Input: https://www.klarna.com/us/shopping/public/openai/v0/products?q=t%20shirts[0m
    Observation: [36;1m[1;3m{"products":[{"name":"Lacoste Men's Pack of Plain T-Shirts","url":"https://www.klarna.com/us/shopping/pl/cl10001/3202043025/Clothing/Lacoste-Men-s-Pack-of-Plain-T-Shirts/?utm_source=openai","price":"$26.60","attributes":["Material:Cotton","Target Group:Man","Color:White,Black"]},{"name":"Hanes Men's Ultimate 6pk. Crewneck T-Shirts","url":"https://www.klarna.com/us/shopping/pl/cl10001/3201808270/Clothing/Hanes-Men-s-Ultimate-6pk.-Crewneck-T-Shirts/?utm_source=openai","price":"$13.82","attributes":["Material:Cotton","Target Group:Man","Color:White"]},{"name":"Nike Boy's Jordan Stretch T-shirts","url":"https://www.klarna.com/us/shopping/pl/cl359/3201863202/Children-s-Clothing/Nike-Boy-s-Jordan-Stretch-T-shirts/?utm_source=openai","price":"$14.99","attributes":["Material:Cotton","Color:White,Green","Model:Boy","Size (Small-Large):S,XL,L,M"]},{"name":"Polo Classic Fit Cotton V-Neck T-Shirts 3-Pack","url":"https://www.klarna.com/us/shopping/pl/cl10001/3203028500/Clothing/Polo-Classic-Fit-Cotton-V-Neck-T-Shirts-3-Pack/?utm_source=openai","price":"$29.95","attributes":["Material:Cotton","Target Group:Man","Color:White,Blue,Black"]},{"name":"adidas Comfort T-shirts Men's 3-pack","url":"https://www.klarna.com/us/shopping/pl/cl10001/3202640533/Clothing/adidas-Comfort-T-shirts-Men-s-3-pack/?utm_source=openai","price":"$14.99","attributes":["Material:Cotton","Target Group:Man","Color:White,Black","Neckline:Round"]}]}[0m
    Thought:[32;1m[1;3mThe available t shirts in Klarna are Lacoste Men's Pack of Plain T-Shirts, Hanes Men's Ultimate 6pk. Crewneck T-Shirts, Nike Boy's Jordan Stretch T-shirts, Polo Classic Fit Cotton V-Neck T-Shirts 3-Pack, and adidas Comfort T-shirts Men's 3-pack.
    Final Answer: The available t shirts in Klarna are Lacoste Men's Pack of Plain T-Shirts, Hanes Men's Ultimate 6pk. Crewneck T-Shirts, Nike Boy's Jordan Stretch T-shirts, Polo Classic Fit Cotton V-Neck T-Shirts 3-Pack, and adidas Comfort T-shirts Men's 3-pack.[0m
    
    [1m> Finished chain.[0m
    




    "The available t shirts in Klarna are Lacoste Men's Pack of Plain T-Shirts, Hanes Men's Ultimate 6pk. Crewneck T-Shirts, Nike Boy's Jordan Stretch T-shirts, Polo Classic Fit Cotton V-Neck T-Shirts 3-Pack, and adidas Comfort T-shirts Men's 3-pack."




```python

```
