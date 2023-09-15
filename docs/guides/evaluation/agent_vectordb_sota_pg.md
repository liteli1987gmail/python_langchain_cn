# Agent VectorDB Question Answering Benchmarking

Here we go over how to benchmark performance on a question answering task using an agent to route between multiple vectordatabases.

It is highly recommended that you do any evaluation/benchmarking with tracing enabled. See [here](https://python.langchain.com/guides/tracing/) for an explanation of what tracing is and how to set it up.


```python
# Comment this out if you are NOT using tracing
import os

os.environ["LANGCHAIN_HANDLER"] = "langchain"
```

## Loading the data
First, let's load the data.


```python
from langchain.evaluation.loading import load_dataset

dataset = load_dataset("agent-vectordb-qa-sota-pg")
```

    Found cached dataset json (/Users/qt/.cache/huggingface/datasets/LangChainDatasets___json/LangChainDatasets--agent-vectordb-qa-sota-pg-d3ae24016b514f92/0.0.0/fe5dd6ea2639a6df622901539cb550cf8797e5a6b2dd7af1cf934bed8e233e6e)
    100%|██████████| 1/1 [00:00<00:00, 414.42it/s]
    


```python
dataset[0]
```




    {'question': 'What is the purpose of the NATO Alliance?',
     'answer': 'The purpose of the NATO Alliance is to secure peace and stability in Europe after World War 2.',
     'steps': [{'tool': 'State of Union QA System', 'tool_input': None},
      {'tool': None, 'tool_input': 'What is the purpose of the NATO Alliance?'}]}




```python
dataset[-1]
```




    {'question': 'What is the purpose of YC?',
     'answer': 'The purpose of YC is to cause startups to be founded that would not otherwise have existed.',
     'steps': [{'tool': 'Paul Graham QA System', 'tool_input': None},
      {'tool': None, 'tool_input': 'What is the purpose of YC?'}]}



## Setting up a chain
Now we need to create some pipelines for doing question answering. Step one in that is creating indexes over the data in question.


```python
from langchain.document_loaders import TextLoader

loader = TextLoader("../../modules/state_of_the_union.txt")
```


```python
from langchain.indexes import VectorstoreIndexCreator
```


```python
vectorstore_sota = (
    VectorstoreIndexCreator(vectorstore_kwargs={"collection_name": "sota"})
    .from_loaders([loader])
    .vectorstore
)
```

    Using embedded DuckDB without persistence: data will be transient
    

Now we can create a question answering chain.


```python
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
```


```python
chain_sota = RetrievalQA.from_chain_type(
    llm=OpenAI(temperature=0),
    chain_type="stuff",
    retriever=vectorstore_sota.as_retriever(),
    input_key="question",
)
```

Now we do the same for the Paul Graham data.


```python
loader = TextLoader("../../modules/paul_graham_essay.txt")
```


```python
vectorstore_pg = (
    VectorstoreIndexCreator(vectorstore_kwargs={"collection_name": "paul_graham"})
    .from_loaders([loader])
    .vectorstore
)
```

    Using embedded DuckDB without persistence: data will be transient
    


```python
chain_pg = RetrievalQA.from_chain_type(
    llm=OpenAI(temperature=0),
    chain_type="stuff",
    retriever=vectorstore_pg.as_retriever(),
    input_key="question",
)
```

We can now set up an agent to route between them.


```python
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType

tools = [
    Tool(
        name="State of Union QA System",
        func=chain_sota.run,
        description="useful for when you need to answer questions about the most recent state of the union address. Input should be a fully formed question.",
    ),
    Tool(
        name="Paul Graham System",
        func=chain_pg.run,
        description="useful for when you need to answer questions about Paul Graham. Input should be a fully formed question.",
    ),
]
```


```python
agent = initialize_agent(
    tools,
    OpenAI(temperature=0),
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    max_iterations=4,
)
```

## Make a prediction

First, we can make predictions one datapoint at a time. Doing it at this level of granularity allows use to explore the outputs in detail, and also is a lot cheaper than running over multiple datapoints


```python
agent.run(dataset[0]["question"])
```




    'The purpose of the NATO Alliance is to secure peace and stability in Europe after World War 2.'



## Make many predictions
Now we can make predictions


```python
predictions = []
predicted_dataset = []
error_dataset = []
for data in dataset:
    new_data = {"input": data["question"], "answer": data["answer"]}
    try:
        predictions.append(agent(new_data))
        predicted_dataset.append(new_data)
    except Exception:
        error_dataset.append(new_data)
```

## Evaluate performance
Now we can evaluate the predictions. The first thing we can do is look at them by eye.


```python
predictions[0]
```




    {'input': 'What is the purpose of the NATO Alliance?',
     'answer': 'The purpose of the NATO Alliance is to secure peace and stability in Europe after World War 2.',
     'output': 'The purpose of the NATO Alliance is to secure peace and stability in Europe after World War 2.'}



Next, we can use a language model to score them programatically


```python
from langchain.evaluation.qa import QAEvalChain
```


```python
llm = OpenAI(temperature=0)
eval_chain = QAEvalChain.from_llm(llm)
graded_outputs = eval_chain.evaluate(
    predicted_dataset, predictions, question_key="input", prediction_key="output"
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




    Counter({' CORRECT': 28, ' INCORRECT': 5})



We can also filter the datapoints to the incorrect examples and look at them.


```python
incorrect = [pred for pred in predictions if pred["grade"] == " INCORRECT"]
```


```python
incorrect[0]
```




    {'input': 'What are the four common sense steps that the author suggests to move forward safely?',
     'answer': 'The four common sense steps suggested by the author to move forward safely are: stay protected with vaccines and treatments, prepare for new variants, end the shutdown of schools and businesses, and stay vigilant.',
     'output': 'The four common sense steps suggested in the most recent State of the Union address are: cutting the cost of prescription drugs, providing a pathway to citizenship for Dreamers, revising laws so businesses have the workers they need and families don’t wait decades to reunite, and protecting access to health care and preserving a woman’s right to choose.',
     'grade': ' INCORRECT'}


