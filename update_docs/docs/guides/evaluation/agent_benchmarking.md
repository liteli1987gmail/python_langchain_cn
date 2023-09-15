# Agent Benchmarking: Search + Calculator

Here we go over how to benchmark performance of an agent on tasks where it has access to a calculator and a search tool.

It is highly reccomended that you do any evaluation/benchmarking with tracing enabled. See [here](https://python.langchain.com/docs/guides/tracing/) for an explanation of what tracing is and how to set it up.


```python
# Comment this out if you are NOT using tracing
import os

os.environ["LANGCHAIN_HANDLER"] = "langchain"
```

## Loading the data
First, let's load the data.


```python
from langchain.evaluation.loading import load_dataset

dataset = load_dataset("agent-search-calculator")
```

## Setting up a chain
Now we need to load an agent capable of answering these questions.


```python
from langchain.llms import OpenAI
from langchain.chains import LLMMathChain
from langchain.agents import initialize_agent, Tool, load_tools
from langchain.agents import AgentType

tools = load_tools(["serpapi", "llm-math"], llm=OpenAI(temperature=0))
agent = initialize_agent(
    tools,
    OpenAI(temperature=0),
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)
```

## Make a prediction

First, we can make predictions one datapoint at a time. Doing it at this level of granularity allows use to explore the outputs in detail, and also is a lot cheaper than running over multiple datapoints


```python
print(dataset[0]["question"])
agent.run(dataset[0]["question"])
```

## Make many predictions
Now we can make predictions


```python
agent.run(dataset[4]["question"])
```


```python
predictions = []
predicted_dataset = []
error_dataset = []
for data in dataset:
    new_data = {"input": data["question"], "answer": data["answer"]}
    try:
        predictions.append(agent(new_data))
        predicted_dataset.append(new_data)
    except Exception as e:
        predictions.append({"output": str(e), **new_data})
        error_dataset.append(new_data)
```

## Evaluate performance
Now we can evaluate the predictions. The first thing we can do is look at them by eye.


```python
predictions[0]
```

Next, we can use a language model to score them programatically


```python
from langchain.evaluation.qa import QAEvalChain
```


```python
llm = OpenAI(temperature=0)
eval_chain = QAEvalChain.from_llm(llm)
graded_outputs = eval_chain.evaluate(
    dataset, predictions, question_key="question", prediction_key="output"
)
```

We can add in the graded output to the `predictions` dict and then get a count of the grades.


```python
for i, prediction in enumerate(predictions):
    prediction["grade"] = graded_outputs[i]["text"]
```


```python
from collections import Counter

Counter([pred["grade"] for pred in predictions])
```

We can also filter the datapoints to the incorrect examples and look at them.


```python
incorrect = [pred for pred in predictions if pred["grade"] == " INCORRECT"]
```


```python
incorrect
```


```python

```
