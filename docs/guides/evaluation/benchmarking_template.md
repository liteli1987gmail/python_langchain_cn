# Benchmarking Template

This is an example notebook that can be used to create a benchmarking notebook for a task of your choice. Evaluation is really hard, and so we greatly welcome any contributions that can make it easier for people to experiment

It is highly reccomended that you do any evaluation/benchmarking with tracing enabled. See [here](https://langchain.readthedocs.io/en/latest/tracing.html) for an explanation of what tracing is and how to set it up.


```python
# Comment this out if you are NOT using tracing
import os

os.environ["LANGCHAIN_HANDLER"] = "langchain"
```

## Loading the data

First, let's load the data.


```python
# This notebook should so how to load the dataset from LangChainDatasets on Hugging Face

# Please upload your dataset to https://huggingface.co/LangChainDatasets

# The value passed into `load_dataset` should NOT have the `LangChainDatasets/` prefix
from langchain.evaluation.loading import load_dataset

dataset = load_dataset("TODO")
```

## Setting up a chain

This next section should have an example of setting up a chain that can be run on this dataset.


```python

```

## Make a prediction

First, we can make predictions one datapoint at a time. Doing it at this level of granularity allows use to explore the outputs in detail, and also is a lot cheaper than running over multiple datapoints


```python
# Example of running the chain on a single datapoint (`dataset[0]`) goes here
```

## Make many predictions
Now we can make predictions.


```python
# Example of running the chain on many predictions goes here

# Sometimes its as simple as `chain.apply(dataset)`

# Othertimes you may want to write a for loop to catch errors
```

## Evaluate performance

Any guide to evaluating performance in a more systematic manner goes here.


```python

```
