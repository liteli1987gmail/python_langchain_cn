# BabyAGI User Guide

This notebook demonstrates how to implement [BabyAGI](https://github.com/yoheinakajima/babyagi/tree/main) by [Yohei Nakajima](https://twitter.com/yoheinakajima). BabyAGI is an AI agent that can generate and pretend to execute tasks based on a given objective.

This guide will help you understand the components to create your own recursive agents.

Although BabyAGI uses specific vectorstores/model providers (Pinecone, OpenAI), one of the benefits of implementing it with LangChain is that you can easily swap those out for different options. In this implementation we use a FAISS vectorstore (because it runs locally and is free).

## Install and Import Required Modules


```python
import os
from collections import deque
from typing import Dict, List, Optional, Any

from langchain import LLMChain, OpenAI, PromptTemplate
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import BaseLLM
from langchain.vectorstores.base import VectorStore
from pydantic import BaseModel, Field
from langchain.chains.base import Chain
from langchain.experimental import BabyAGI
```

## Connect to the Vector Store

Depending on what vectorstore you use, this step may look different.


```python
from langchain.vectorstores import FAISS
from langchain.docstore import InMemoryDocstore
```


```python
# Define your embedding model
embeddings_model = OpenAIEmbeddings()
# Initialize the vectorstore as empty
import faiss

embedding_size = 1536
index = faiss.IndexFlatL2(embedding_size)
vectorstore = FAISS(embeddings_model.embed_query, index, InMemoryDocstore({}), {})
```

### Run the BabyAGI

Now it's time to create the BabyAGI controller and watch it try to accomplish your objective.


```python
OBJECTIVE = "Write a weather report for SF today"
```


```python
llm = OpenAI(temperature=0)
```


```python
# Logging of LLMChains
verbose = False
# If None, will keep on going forever
max_iterations: Optional[int] = 3
baby_agi = BabyAGI.from_llm(
    llm=llm, vectorstore=vectorstore, verbose=verbose, max_iterations=max_iterations
)
```


```python
baby_agi({"objective": OBJECTIVE})
```

    [95m[1m
    *****TASK LIST*****
    [0m[0m
    1: Make a todo list
    [92m[1m
    *****NEXT TASK*****
    [0m[0m
    1: Make a todo list
    [93m[1m
    *****TASK RESULT*****
    [0m[0m
    
    
    1. Check the weather forecast for San Francisco today
    2. Make note of the temperature, humidity, wind speed, and other relevant weather conditions
    3. Write a weather report summarizing the forecast
    4. Check for any weather alerts or warnings
    5. Share the report with the relevant stakeholders
    [95m[1m
    *****TASK LIST*****
    [0m[0m
    2: Check the current temperature in San Francisco
    3: Check the current humidity in San Francisco
    4: Check the current wind speed in San Francisco
    5: Check for any weather alerts or warnings in San Francisco
    6: Check the forecast for the next 24 hours in San Francisco
    7: Check the forecast for the next 48 hours in San Francisco
    8: Check the forecast for the next 72 hours in San Francisco
    9: Check the forecast for the next week in San Francisco
    10: Check the forecast for the next month in San Francisco
    11: Check the forecast for the next 3 months in San Francisco
    1: Write a weather report for SF today
    [92m[1m
    *****NEXT TASK*****
    [0m[0m
    2: Check the current temperature in San Francisco
    [93m[1m
    *****TASK RESULT*****
    [0m[0m
    
    
    I will check the current temperature in San Francisco. I will use an online weather service to get the most up-to-date information.
    [95m[1m
    *****TASK LIST*****
    [0m[0m
    3: Check the current UV index in San Francisco.
    4: Check the current air quality in San Francisco.
    5: Check the current precipitation levels in San Francisco.
    6: Check the current cloud cover in San Francisco.
    7: Check the current barometric pressure in San Francisco.
    8: Check the current dew point in San Francisco.
    9: Check the current wind direction in San Francisco.
    10: Check the current humidity levels in San Francisco.
    1: Check the current temperature in San Francisco to the average temperature for this time of year.
    2: Check the current visibility in San Francisco.
    11: Write a weather report for SF today.
    [92m[1m
    *****NEXT TASK*****
    [0m[0m
    3: Check the current UV index in San Francisco.
    [93m[1m
    *****TASK RESULT*****
    [0m[0m
    
    
    The current UV index in San Francisco is moderate. The UV index is expected to remain at moderate levels throughout the day. It is recommended to wear sunscreen and protective clothing when outdoors.
    [91m[1m
    *****TASK ENDING*****
    [0m[0m
    




    {'objective': 'Write a weather report for SF today'}




```python

```
