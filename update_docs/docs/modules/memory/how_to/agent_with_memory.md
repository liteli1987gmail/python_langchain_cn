# How to add Memory to an Agent

This notebook goes over adding memory to an Agent. Before going through this notebook, please walkthrough the following notebooks, as this will build on top of both of them:

- [Adding memory to an LLM Chain](adding_memory.html)
- [Custom Agents](../../agents/agents/custom_agent.html)

In order to add a memory to an agent we are going to the the following steps:

1. We are going to create an LLMChain with memory.
2. We are going to use that LLMChain to create a custom Agent.

For the purposes of this exercise, we are going to create a simple custom Agent that has access to a search tool and utilizes the `ConversationBufferMemory` class.


```python
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain import OpenAI, LLMChain
from langchain.utilities import GoogleSearchAPIWrapper
```


```python
search = GoogleSearchAPIWrapper()
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="useful for when you need to answer questions about current events",
    )
]
```

Notice the usage of the `chat_history` variable in the PromptTemplate, which matches up with the dynamic key name in the ConversationBufferMemory.


```python
prefix = """Have a conversation with a human, answering the following questions as best you can. You have access to the following tools:"""
suffix = """Begin!"

{chat_history}
Question: {input}
{agent_scratchpad}"""

prompt = ZeroShotAgent.create_prompt(
    tools,
    prefix=prefix,
    suffix=suffix,
    input_variables=["input", "chat_history", "agent_scratchpad"],
)
memory = ConversationBufferMemory(memory_key="chat_history")
```

We can now construct the LLMChain, with the Memory object, and then create the agent.


```python
llm_chain = LLMChain(llm=OpenAI(temperature=0), prompt=prompt)
agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=True)
agent_chain = AgentExecutor.from_agent_and_tools(
    agent=agent, tools=tools, verbose=True, memory=memory
)
```


```python
agent_chain.run(input="How many people live in canada?")
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3mThought: I need to find out the population of Canada
    Action: Search
    Action Input: Population of Canada[0m
    Observation: [36;1m[1;3mThe current population of Canada is 38,566,192 as of Saturday, December 31, 2022, based on Worldometer elaboration of the latest United Nations data. · Canada ... Additional information related to Canadian population trends can be found on Statistics Canada's Population and Demography Portal. Population of Canada (real- ... Index to the latest information from the Census of Population. This survey conducted by Statistics Canada provides a statistical portrait of Canada and its ... 14 records ... Estimated number of persons by quarter of a year and by year, Canada, provinces and territories. The 2021 Canadian census counted a total population of 36,991,981, an increase of around 5.2 percent over the 2016 figure. ... Between 1990 and 2008, the ... ( 2 ) Census reports and other statistical publications from national statistical offices, ( 3 ) Eurostat: Demographic Statistics, ( 4 ) United Nations ... Canada is a country in North America. Its ten provinces and three territories extend from ... Population. • Q4 2022 estimate. 39,292,355 (37th). Information is available for the total Indigenous population and each of the three ... The term 'Aboriginal' or 'Indigenous' used on the Statistics Canada ... Jun 14, 2022 ... Determinants of health are the broad range of personal, social, economic and environmental factors that determine individual and population ... COVID-19 vaccination coverage across Canada by demographics and key populations. Updated every Friday at 12:00 PM Eastern Time.[0m
    Thought:[32;1m[1;3m I now know the final answer
    Final Answer: The current population of Canada is 38,566,192 as of Saturday, December 31, 2022, based on Worldometer elaboration of the latest United Nations data.[0m
    [1m> Finished AgentExecutor chain.[0m
    




    'The current population of Canada is 38,566,192 as of Saturday, December 31, 2022, based on Worldometer elaboration of the latest United Nations data.'



To test the memory of this agent, we can ask a followup question that relies on information in the previous exchange to be answered correctly.


```python
agent_chain.run(input="what is their national anthem called?")
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3mThought: I need to find out what the national anthem of Canada is called.
    Action: Search
    Action Input: National Anthem of Canada[0m
    Observation: [36;1m[1;3mJun 7, 2010 ... https://twitter.com/CanadaImmigrantCanadian National Anthem O Canada in HQ - complete with lyrics, captions, vocals & music.LYRICS:O Canada! Nov 23, 2022 ... After 100 years of tradition, O Canada was proclaimed Canada's national anthem in 1980. The music for O Canada was composed in 1880 by Calixa ... O Canada, national anthem of Canada. It was proclaimed the official national anthem on July 1, 1980. “God Save the Queen” remains the royal anthem of Canada ... O Canada! Our home and native land! True patriot love in all of us command. Car ton bras sait porter l'épée,. Il sait porter la croix! "O Canada" (French: Ô Canada) is the national anthem of Canada. The song was originally commissioned by Lieutenant Governor of Quebec Théodore Robitaille ... Feb 1, 2018 ... It was a simple tweak — just two words. But with that, Canada just voted to make its national anthem, “O Canada,” gender neutral, ... "O Canada" was proclaimed Canada's national anthem on July 1,. 1980, 100 years after it was first sung on June 24, 1880. The music. Patriotic music in Canada dates back over 200 years as a distinct category from British or French patriotism, preceding the first legal steps to ... Feb 4, 2022 ... English version: O Canada! Our home and native land! True patriot love in all of us command. With glowing hearts we ... Feb 1, 2018 ... Canada's Senate has passed a bill making the country's national anthem gender-neutral. If you're not familiar with the words to “O Canada,” ...[0m
    Thought:[32;1m[1;3m I now know the final answer.
    Final Answer: The national anthem of Canada is called "O Canada".[0m
    [1m> Finished AgentExecutor chain.[0m
    




    'The national anthem of Canada is called "O Canada".'



We can see that the agent remembered that the previous question was about Canada, and properly asked Google Search what the name of Canada's national anthem was.

For fun, let's compare this to an agent that does NOT have memory.


```python
prefix = """Have a conversation with a human, answering the following questions as best you can. You have access to the following tools:"""
suffix = """Begin!"

Question: {input}
{agent_scratchpad}"""

prompt = ZeroShotAgent.create_prompt(
    tools, prefix=prefix, suffix=suffix, input_variables=["input", "agent_scratchpad"]
)
llm_chain = LLMChain(llm=OpenAI(temperature=0), prompt=prompt)
agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=True)
agent_without_memory = AgentExecutor.from_agent_and_tools(
    agent=agent, tools=tools, verbose=True
)
```


```python
agent_without_memory.run("How many people live in canada?")
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3mThought: I need to find out the population of Canada
    Action: Search
    Action Input: Population of Canada[0m
    Observation: [36;1m[1;3mThe current population of Canada is 38,566,192 as of Saturday, December 31, 2022, based on Worldometer elaboration of the latest United Nations data. · Canada ... Additional information related to Canadian population trends can be found on Statistics Canada's Population and Demography Portal. Population of Canada (real- ... Index to the latest information from the Census of Population. This survey conducted by Statistics Canada provides a statistical portrait of Canada and its ... 14 records ... Estimated number of persons by quarter of a year and by year, Canada, provinces and territories. The 2021 Canadian census counted a total population of 36,991,981, an increase of around 5.2 percent over the 2016 figure. ... Between 1990 and 2008, the ... ( 2 ) Census reports and other statistical publications from national statistical offices, ( 3 ) Eurostat: Demographic Statistics, ( 4 ) United Nations ... Canada is a country in North America. Its ten provinces and three territories extend from ... Population. • Q4 2022 estimate. 39,292,355 (37th). Information is available for the total Indigenous population and each of the three ... The term 'Aboriginal' or 'Indigenous' used on the Statistics Canada ... Jun 14, 2022 ... Determinants of health are the broad range of personal, social, economic and environmental factors that determine individual and population ... COVID-19 vaccination coverage across Canada by demographics and key populations. Updated every Friday at 12:00 PM Eastern Time.[0m
    Thought:[32;1m[1;3m I now know the final answer
    Final Answer: The current population of Canada is 38,566,192 as of Saturday, December 31, 2022, based on Worldometer elaboration of the latest United Nations data.[0m
    [1m> Finished AgentExecutor chain.[0m
    




    'The current population of Canada is 38,566,192 as of Saturday, December 31, 2022, based on Worldometer elaboration of the latest United Nations data.'




```python
agent_without_memory.run("what is their national anthem called?")
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3mThought: I should look up the answer
    Action: Search
    Action Input: national anthem of [country][0m
    Observation: [36;1m[1;3mMost nation states have an anthem, defined as "a song, as of praise, devotion, or patriotism"; most anthems are either marches or hymns in style. List of all countries around the world with its national anthem. ... Title and lyrics in the language of the country and translated into English, Aug 1, 2021 ... 1. Afghanistan, "Milli Surood" (National Anthem) · 2. Armenia, "Mer Hayrenik" (Our Fatherland) · 3. Azerbaijan (a transcontinental country with ... A national anthem is a patriotic musical composition symbolizing and evoking eulogies of the history and traditions of a country or nation. National Anthem of Every Country ; Fiji, “Meda Dau Doka” (“God Bless Fiji”) ; Finland, “Maamme”. (“Our Land”) ; France, “La Marseillaise” (“The Marseillaise”). You can find an anthem in the menu at the top alphabetically or you can use the search feature. This site is focussed on the scholarly study of national anthems ... Feb 13, 2022 ... The 38-year-old country music artist had the honor of singing the National Anthem during this year's big game, and she did not disappoint. Oldest of the World's National Anthems ; France, La Marseillaise (“The Marseillaise”), 1795 ; Argentina, Himno Nacional Argentino (“Argentine National Anthem”) ... Mar 3, 2022 ... Country music star Jessie James Decker gained the respect of music and hockey fans alike after a jaw-dropping rendition of "The Star-Spangled ... This list shows the country on the left, the national anthem in the ... There are many countries over the world who have a national anthem of their own.[0m
    Thought:[32;1m[1;3m I now know the final answer
    Final Answer: The national anthem of [country] is [name of anthem].[0m
    [1m> Finished AgentExecutor chain.[0m
    




    'The national anthem of [country] is [name of anthem].'




```python

```
