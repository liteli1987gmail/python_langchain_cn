# LLM数学

评估会做数学的链。


```python
# 如果您没有使用跟踪，请注释掉此行
import os

os.environ["LANGCHAIN_HANDLER"] = "langchain"
```


```python
from langchain.evaluation.loading import load_dataset

dataset = load_dataset("llm-math")
```


    正在下载readme:   0%|          | 0.00/21.0 [00:00<?, ?B/s]


    正在下载并准备数据集 json/LangChainDatasets--llm-math 到 /Users/harrisonchase/.cache/huggingface/datasets/LangChainDatasets___json/LangChainDatasets--llm-math-509b11d101165afa/0.0.0/0f7e3662623656454fcd2b650f34e886a7db4b9104504885bd462096cc7a9f51...
    


    正在下载数据文件:   0%|          | 0/1 [00:00<?, ?it/s]



    正在下载数据:   0%|          | 0.00/631 [00:00<?, ?B/s]



    正在提取数据文件:   0%|          | 0/1 [00:00<?, ?it/s]



    正在生成训练集: 0 个样本 [00:00, ? 个样本/s]


    数据集 json 下载并准备完成，保存在 /Users/harrisonchase/.cache/huggingface/datasets/LangChainDatasets___json/LangChainDatasets--llm-math-509b11d101165afa/0.0.0/0f7e3662623656454fcd2b650f34e886a7db4b9104504885bd462096cc7a9f51。以后的调用将重用这些数据。
    


      0%|          | 0/1 [00:00<?, ?it/s]


## 设置链
现在我们需要创建一些用于做数学运算的管道。


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
    input:  2的3.171次方
    expected output : 9.006708689094099
    prediction:  9.006708689094099
    input:  五加三的平方减一
    expected output : 13.0
    prediction:  13.0
    input:  2097乘以27.31
    expected output : 57269.07
    prediction:  57269.07
    input:  两千零九十七乘以二十七点三一
    expected output : 57269.07
    prediction:  57269.07
    input:  209758除以2714
    expected output : 77.28739867354459
    prediction:  77.28739867354459
    input:  209758.857除以2714.31
    expected output : 77.27888745205964
    prediction:  77.27888745205964
    


```python

```
