# Aim

Aim makes it super easy to visualize and debug LangChain executions. Aim tracks inputs and outputs of LLMs and tools, as well as actions of agents. 

With Aim, you can easily debug and examine an individual execution:

![](https://user-images.githubusercontent.com/13848158/227784778-06b806c7-74a1-4d15-ab85-9ece09b458aa.png)

Additionally, you have the option to compare multiple executions side by side:

![](https://user-images.githubusercontent.com/13848158/227784994-699b24b7-e69b-48f9-9ffa-e6a6142fd719.png)

Aim is fully open source, [learn more](https://github.com/aimhubio/aim) about Aim on GitHub.

Let's move forward and see how to enable and configure Aim callback.

<h3>Tracking LangChain Executions with Aim</h3>

In this notebook we will explore three usage scenarios. To start off, we will install the necessary packages and import certain modules. Subsequently, we will configure two environment variables that can be established either within the Python script or through the terminal.


```python
!pip install aim
!pip install langchain
!pip install openai
!pip install google-search-results
```


```python
import os
from datetime import datetime

from langchain.llms import OpenAI
from langchain.callbacks import AimCallbackHandler, StdOutCallbackHandler
```

Our examples use a GPT model as the LLM, and OpenAI offers an API for this purpose. You can obtain the key from the following link: https://platform.openai.com/account/api-keys .

We will use the SerpApi to retrieve search results from Google. To acquire the SerpApi key, please go to https://serpapi.com/manage-api-key .


```python
os.environ["OPENAI_API_KEY"] = "..."
os.environ["SERPAPI_API_KEY"] = "..."
```

The event methods of `AimCallbackHandler` accept the LangChain module or agent as input and log at least the prompts and generated results, as well as the serialized version of the LangChain module, to the designated Aim run.


```python
session_group = datetime.now().strftime("%m.%d.%Y_%H.%M.%S")
aim_callback = AimCallbackHandler(
    repo=".",
    experiment_name="scenario 1: OpenAI LLM",
)

callbacks = [StdOutCallbackHandler(), aim_callback]
llm = OpenAI(temperature=0, callbacks=callbacks)
```

The `flush_tracker` function is used to record LangChain assets on Aim. By default, the session is reset rather than being terminated outright.

<h3>Scenario 1</h3> In the first scenario, we will use OpenAI LLM.


```python
# scenario 1 - LLM
llm_result = llm.generate(["Tell me a joke", "Tell me a poem"] * 3)
aim_callback.flush_tracker(
    langchain_asset=llm,
    experiment_name="scenario 2: Chain with multiple SubChains on multiple generations",
)
```

<h3>Scenario 2</h3> Scenario two involves chaining with multiple SubChains across multiple generations.


```python
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
```


```python
# scenario 2 - Chain
template = """You are a playwright. Given the title of play, it is your job to write a synopsis for that title.
Title: {title}
Playwright: This is a synopsis for the above play:"""
prompt_template = PromptTemplate(input_variables=["title"], template=template)
synopsis_chain = LLMChain(llm=llm, prompt=prompt_template, callbacks=callbacks)

test_prompts = [
    {
        "title": "documentary about good video games that push the boundary of game design"
    },
    {"title": "the phenomenon behind the remarkable speed of cheetahs"},
    {"title": "the best in class mlops tooling"},
]
synopsis_chain.apply(test_prompts)
aim_callback.flush_tracker(
    langchain_asset=synopsis_chain, experiment_name="scenario 3: Agent with Tools"
)
```

<h3>Scenario 3</h3> The third scenario involves an agent with tools.


```python
from langchain.agents import initialize_agent, load_tools
from langchain.agents import AgentType
```


```python
# scenario 3 - Agent with Tools
tools = load_tools(["serpapi", "llm-math"], llm=llm, callbacks=callbacks)
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    callbacks=callbacks,
)
agent.run(
    "Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?"
)
aim_callback.flush_tracker(langchain_asset=agent, reset=False, finish=True)
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3m I need to find out who Leo DiCaprio's girlfriend is and then calculate her age raised to the 0.43 power.
    Action: Search
    Action Input: "Leo DiCaprio girlfriend"[0m
    Observation: [36;1m[1;3mLeonardo DiCaprio seemed to prove a long-held theory about his love life right after splitting from girlfriend Camila Morrone just months ...[0m
    Thought:[32;1m[1;3m I need to find out Camila Morrone's age
    Action: Search
    Action Input: "Camila Morrone age"[0m
    Observation: [36;1m[1;3m25 years[0m
    Thought:[32;1m[1;3m I need to calculate 25 raised to the 0.43 power
    Action: Calculator
    Action Input: 25^0.43[0m
    Observation: [33;1m[1;3mAnswer: 3.991298452658078
    [0m
    Thought:[32;1m[1;3m I now know the final answer
    Final Answer: Camila Morrone is Leo DiCaprio's girlfriend and her current age raised to the 0.43 power is 3.991298452658078.[0m
    
    [1m> Finished chain.[0m
    
