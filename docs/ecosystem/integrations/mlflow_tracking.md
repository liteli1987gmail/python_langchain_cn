# MLflow

This notebook goes over how to track your LangChain experiments into your MLflow Server


```python
!pip install azureml-mlflow
!pip install pandas
!pip install textstat
!pip install spacy
!pip install openai
!pip install google-search-results
!python -m spacy download en_core_web_sm
```


```python
import os

os.environ["MLFLOW_TRACKING_URI"] = ""
os.environ["OPENAI_API_KEY"] = ""
os.environ["SERPAPI_API_KEY"] = ""
```


```python
from langchain.callbacks import MlflowCallbackHandler
from langchain.llms import OpenAI
```


```python
"""Main function.

This function is used to try the callback handler.
Scenarios:
1. OpenAI LLM
2. Chain with multiple SubChains on multiple generations
3. Agent with Tools
"""
mlflow_callback = MlflowCallbackHandler()
llm = OpenAI(
    model_name="gpt-3.5-turbo", temperature=0, callbacks=[mlflow_callback], verbose=True
)
```


```python
# SCENARIO 1 - LLM
llm_result = llm.generate(["Tell me a joke"])

mlflow_callback.flush_tracker(llm)
```


```python
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
```


```python
# SCENARIO 2 - Chain
template = """You are a playwright. Given the title of play, it is your job to write a synopsis for that title.
Title: {title}
Playwright: This is a synopsis for the above play:"""
prompt_template = PromptTemplate(input_variables=["title"], template=template)
synopsis_chain = LLMChain(llm=llm, prompt=prompt_template, callbacks=[mlflow_callback])

test_prompts = [
    {
        "title": "documentary about good video games that push the boundary of game design"
    },
]
synopsis_chain.apply(test_prompts)
mlflow_callback.flush_tracker(synopsis_chain)
```


```python
from langchain.agents import initialize_agent, load_tools
from langchain.agents import AgentType
```


```python
# SCENARIO 3 - Agent with Tools
tools = load_tools(["serpapi", "llm-math"], llm=llm, callbacks=[mlflow_callback])
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    callbacks=[mlflow_callback],
    verbose=True,
)
agent.run(
    "Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?"
)
mlflow_callback.flush_tracker(agent, finish=True)
```
