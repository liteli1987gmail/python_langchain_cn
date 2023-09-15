# Plug-and-Plai

This notebook builds upon the idea of [tool retrieval](custom_agent_with_plugin_retrieval.html), but pulls all tools from `plugnplai` - a directory of AI Plugins.

## Set up environment

Do necessary imports, etc.

Install plugnplai lib to get a list of active plugins from https://plugplai.com directory


```python
pip install plugnplai -q
```

    
    [1m[[0m[34;49mnotice[0m[1;39;49m][0m[39;49m A new release of pip available: [0m[31;49m22.3.1[0m[39;49m -> [0m[32;49m23.1.1[0m
    [1m[[0m[34;49mnotice[0m[1;39;49m][0m[39;49m To update, run: [0m[32;49mpip install --upgrade pip[0m
    Note: you may need to restart the kernel to use updated packages.
    


```python
from langchain.agents import (
    Tool,
    AgentExecutor,
    LLMSingleActionAgent,
    AgentOutputParser,
)
from langchain.prompts import StringPromptTemplate
from langchain import OpenAI, SerpAPIWrapper, LLMChain
from typing import List, Union
from langchain.schema import AgentAction, AgentFinish
from langchain.agents.agent_toolkits import NLAToolkit
from langchain.tools.plugin import AIPlugin
import re
import plugnplai
```

## Setup LLM


```python
llm = OpenAI(temperature=0)
```

## Set up plugins

Load and index plugins


```python
# Get all plugins from plugnplai.com
urls = plugnplai.get_plugins()

#  Get ChatGPT plugins - only ChatGPT verified plugins
urls = plugnplai.get_plugins(filter="ChatGPT")

#  Get working plugins - only tested plugins (in progress)
urls = plugnplai.get_plugins(filter="working")


AI_PLUGINS = [AIPlugin.from_url(url + "/.well-known/ai-plugin.json") for url in urls]
```

## Tool Retriever

We will use a vectorstore to create embeddings for each tool description. Then, for an incoming query we can create embeddings for that query and do a similarity search for relevant tools.


```python
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
```


```python
embeddings = OpenAIEmbeddings()
docs = [
    Document(
        page_content=plugin.description_for_model,
        metadata={"plugin_name": plugin.name_for_model},
    )
    for plugin in AI_PLUGINS
]
vector_store = FAISS.from_documents(docs, embeddings)
toolkits_dict = {
    plugin.name_for_model: NLAToolkit.from_llm_and_ai_plugin(llm, plugin)
    for plugin in AI_PLUGINS
}
```

    Attempting to load an OpenAPI 3.0.1 spec.  This may result in degraded performance. Convert your OpenAPI spec to 3.1.* spec for better support.
    Attempting to load an OpenAPI 3.0.1 spec.  This may result in degraded performance. Convert your OpenAPI spec to 3.1.* spec for better support.
    Attempting to load an OpenAPI 3.0.1 spec.  This may result in degraded performance. Convert your OpenAPI spec to 3.1.* spec for better support.
    Attempting to load an OpenAPI 3.0.2 spec.  This may result in degraded performance. Convert your OpenAPI spec to 3.1.* spec for better support.
    Attempting to load an OpenAPI 3.0.1 spec.  This may result in degraded performance. Convert your OpenAPI spec to 3.1.* spec for better support.
    Attempting to load an OpenAPI 3.0.1 spec.  This may result in degraded performance. Convert your OpenAPI spec to 3.1.* spec for better support.
    Attempting to load an OpenAPI 3.0.1 spec.  This may result in degraded performance. Convert your OpenAPI spec to 3.1.* spec for better support.
    Attempting to load an OpenAPI 3.0.1 spec.  This may result in degraded performance. Convert your OpenAPI spec to 3.1.* spec for better support.
    Attempting to load a Swagger 2.0 spec.  This may result in degraded performance. Convert your OpenAPI spec to 3.1.* spec for better support.
    


```python
retriever = vector_store.as_retriever()


def get_tools(query):
    # Get documents, which contain the Plugins to use
    docs = retriever.get_relevant_documents(query)
    # Get the toolkits, one for each plugin
    tool_kits = [toolkits_dict[d.metadata["plugin_name"]] for d in docs]
    # Get the tools: a separate NLAChain for each endpoint
    tools = []
    for tk in tool_kits:
        tools.extend(tk.nla_tools)
    return tools
```

We can now test this retriever to see if it seems to work.


```python
tools = get_tools("What could I do today with my kiddo")
[t.name for t in tools]
```




    ['Milo.askMilo',
     'Zapier_Natural_Language_Actions_(NLA)_API_(Dynamic)_-_Beta.search_all_actions',
     'Zapier_Natural_Language_Actions_(NLA)_API_(Dynamic)_-_Beta.preview_a_zap',
     'Zapier_Natural_Language_Actions_(NLA)_API_(Dynamic)_-_Beta.get_configuration_link',
     'Zapier_Natural_Language_Actions_(NLA)_API_(Dynamic)_-_Beta.list_exposed_actions',
     'SchoolDigger_API_V2.0.Autocomplete_GetSchools',
     'SchoolDigger_API_V2.0.Districts_GetAllDistricts2',
     'SchoolDigger_API_V2.0.Districts_GetDistrict2',
     'SchoolDigger_API_V2.0.Rankings_GetSchoolRank2',
     'SchoolDigger_API_V2.0.Rankings_GetRank_District',
     'SchoolDigger_API_V2.0.Schools_GetAllSchools20',
     'SchoolDigger_API_V2.0.Schools_GetSchool20',
     'Speak.translate',
     'Speak.explainPhrase',
     'Speak.explainTask']




```python
tools = get_tools("what shirts can i buy?")
[t.name for t in tools]
```




    ['Open_AI_Klarna_product_Api.productsUsingGET',
     'Milo.askMilo',
     'Zapier_Natural_Language_Actions_(NLA)_API_(Dynamic)_-_Beta.search_all_actions',
     'Zapier_Natural_Language_Actions_(NLA)_API_(Dynamic)_-_Beta.preview_a_zap',
     'Zapier_Natural_Language_Actions_(NLA)_API_(Dynamic)_-_Beta.get_configuration_link',
     'Zapier_Natural_Language_Actions_(NLA)_API_(Dynamic)_-_Beta.list_exposed_actions',
     'SchoolDigger_API_V2.0.Autocomplete_GetSchools',
     'SchoolDigger_API_V2.0.Districts_GetAllDistricts2',
     'SchoolDigger_API_V2.0.Districts_GetDistrict2',
     'SchoolDigger_API_V2.0.Rankings_GetSchoolRank2',
     'SchoolDigger_API_V2.0.Rankings_GetRank_District',
     'SchoolDigger_API_V2.0.Schools_GetAllSchools20',
     'SchoolDigger_API_V2.0.Schools_GetSchool20']



## Prompt Template

The prompt template is pretty standard, because we're not actually changing that much logic in the actual prompt template, but rather we are just changing how retrieval is done.


```python
# Set up the base template
template = """Answer the following questions as best you can, but speaking as a pirate might speak. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin! Remember to speak as a pirate when giving your final answer. Use lots of "Arg"s

Question: {input}
{agent_scratchpad}"""
```

The custom prompt template now has the concept of a tools_getter, which we call on the input to select the tools to use


```python
from typing import Callable


# Set up a prompt template
class CustomPromptTemplate(StringPromptTemplate):
    # The template to use
    template: str
    ############## NEW ######################
    # The list of tools available
    tools_getter: Callable

    def format(self, **kwargs) -> str:
        # Get the intermediate steps (AgentAction, Observation tuples)
        # Format them in a particular way
        intermediate_steps = kwargs.pop("intermediate_steps")
        thoughts = ""
        for action, observation in intermediate_steps:
            thoughts += action.log
            thoughts += f"\nObservation: {observation}\nThought: "
        # Set the agent_scratchpad variable to that value
        kwargs["agent_scratchpad"] = thoughts
        ############## NEW ######################
        tools = self.tools_getter(kwargs["input"])
        # Create a tools variable from the list of tools provided
        kwargs["tools"] = "\n".join(
            [f"{tool.name}: {tool.description}" for tool in tools]
        )
        # Create a list of tool names for the tools provided
        kwargs["tool_names"] = ", ".join([tool.name for tool in tools])
        return self.template.format(**kwargs)
```


```python
prompt = CustomPromptTemplate(
    template=template,
    tools_getter=get_tools,
    # This omits the `agent_scratchpad`, `tools`, and `tool_names` variables because those are generated dynamically
    # This includes the `intermediate_steps` variable because that is needed
    input_variables=["input", "intermediate_steps"],
)
```

## Output Parser

The output parser is unchanged from the previous notebook, since we are not changing anything about the output format.


```python
class CustomOutputParser(AgentOutputParser):
    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        # Check if agent should finish
        if "Final Answer:" in llm_output:
            return AgentFinish(
                # Return values is generally always a dictionary with a single `output` key
                # It is not recommended to try anything else at the moment :)
                return_values={"output": llm_output.split("Final Answer:")[-1].strip()},
                log=llm_output,
            )
        # Parse out the action and action input
        regex = r"Action\s*\d*\s*:(.*?)\nAction\s*\d*\s*Input\s*\d*\s*:[\s]*(.*)"
        match = re.search(regex, llm_output, re.DOTALL)
        if not match:
            raise ValueError(f"Could not parse LLM output: `{llm_output}`")
        action = match.group(1).strip()
        action_input = match.group(2)
        # Return the action and action input
        return AgentAction(
            tool=action, tool_input=action_input.strip(" ").strip('"'), log=llm_output
        )
```


```python
output_parser = CustomOutputParser()
```

## Set up LLM, stop sequence, and the agent

Also the same as the previous notebook


```python
llm = OpenAI(temperature=0)
```


```python
# LLM chain consisting of the LLM and a prompt
llm_chain = LLMChain(llm=llm, prompt=prompt)
```


```python
tool_names = [tool.name for tool in tools]
agent = LLMSingleActionAgent(
    llm_chain=llm_chain,
    output_parser=output_parser,
    stop=["\nObservation:"],
    allowed_tools=tool_names,
)
```

## Use the Agent

Now we can use it!


```python
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent, tools=tools, verbose=True
)
```


```python
agent_executor.run("what shirts can i buy?")
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3mThought: I need to find a product API
    Action: Open_AI_Klarna_product_Api.productsUsingGET
    Action Input: shirts[0m
    
    Observation:[36;1m[1;3mI found 10 shirts from the API response. They range in price from $9.99 to $450.00 and come in a variety of materials, colors, and patterns.[0m[32;1m[1;3m I now know what shirts I can buy
    Final Answer: Arg, I found 10 shirts from the API response. They range in price from $9.99 to $450.00 and come in a variety of materials, colors, and patterns.[0m
    
    [1m> Finished chain.[0m
    




    'Arg, I found 10 shirts from the API response. They range in price from $9.99 to $450.00 and come in a variety of materials, colors, and patterns.'




```python

```
