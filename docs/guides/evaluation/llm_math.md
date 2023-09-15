# LLM Math

Evaluating chains that know how to do math.


```python
# Comment this out if you are NOT using tracing
import os

os.environ["LANGCHAIN_HANDLER"] = "langchain"
```


```python
from langchain.evaluation.loading import load_dataset

dataset = load_dataset("llm-math")
```


    Downloading readme:   0%|          | 0.00/21.0 [00:00<?, ?B/s]


    Downloading and preparing dataset json/LangChainDatasets--llm-math to /Users/harrisonchase/.cache/huggingface/datasets/LangChainDatasets___json/LangChainDatasets--llm-math-509b11d101165afa/0.0.0/0f7e3662623656454fcd2b650f34e886a7db4b9104504885bd462096cc7a9f51...
    


    Downloading data files:   0%|          | 0/1 [00:00<?, ?it/s]



    Downloading data:   0%|          | 0.00/631 [00:00<?, ?B/s]



    Extracting data files:   0%|          | 0/1 [00:00<?, ?it/s]



    Generating train split: 0 examples [00:00, ? examples/s]


    Dataset json downloaded and prepared to /Users/harrisonchase/.cache/huggingface/datasets/LangChainDatasets___json/LangChainDatasets--llm-math-509b11d101165afa/0.0.0/0f7e3662623656454fcd2b650f34e886a7db4b9104504885bd462096cc7a9f51. Subsequent calls will reuse this data.
    


      0%|          | 0/1 [00:00<?, ?it/s]


## Setting up a chain
Now we need to create some pipelines for doing math.


```python
from langchain.llms import OpenAI
from langchain.chains import LLMMathChain
```


```python
llm = OpenAI()
```


```python
chain = LLMMathChain(llm=llm)
```


```python
predictions = chain.apply(dataset)
```


```python
numeric_output = [float(p["answer"].strip().strip("Answer: ")) for p in predictions]
```


```python
correct = [example["answer"] == numeric_output[i] for i, example in enumerate(dataset)]
```


```python
sum(correct) / len(correct)
```




    1.0




```python
for i, example in enumerate(dataset):
    print("input: ", example["question"])
    print("expected output :", example["answer"])
    print("prediction: ", numeric_output[i])
```

    input:  5
    expected output : 5.0
    prediction:  5.0
    input:  5 + 3
    expected output : 8.0
    prediction:  8.0
    input:  2^3.171
    expected output : 9.006708689094099
    prediction:  9.006708689094099
    input:    2 ^3.171 
    expected output : 9.006708689094099
    prediction:  9.006708689094099
    input:  two to the power of three point one hundred seventy one
    expected output : 9.006708689094099
    prediction:  9.006708689094099
    input:  five + three squared minus 1
    expected output : 13.0
    prediction:  13.0
    input:  2097 times 27.31
    expected output : 57269.07
    prediction:  57269.07
    input:  two thousand ninety seven times twenty seven point thirty one
    expected output : 57269.07
    prediction:  57269.07
    input:  209758 / 2714
    expected output : 77.28739867354459
    prediction:  77.28739867354459
    input:  209758.857 divided by 2714.31
    expected output : 77.27888745205964
    prediction:  77.27888745205964
    


```python

```
