# 问答基准测试: Paul Graham Essay

在这里，我们将介绍如何在Paul Graham的一篇文章上对问答任务的性能进行基准测试。

强烈建议您在进行任何评估/基准测试时启用跟踪。请参阅[这里](https://langchain.readthedocs.io/en/latest/tracing.html)了解跟踪是什么以及如何设置。


```python
# 如果您未使用跟踪，请将此行注释掉
import os

os.environ["LANGCHAIN_HANDLER"] = "langchain"
```

## 加载数据
首先，让我们加载数据。


```python
from langchain.evaluation.loading import load_dataset

dataset = load_dataset("question-answering-paul-graham")
```

    找到缓存的数据集json (/Users/harrisonchase/.cache/huggingface/datasets/LangChainDatasets___json/LangChainDatasets--question-answering-paul-graham-76e8f711e038d742/0.0.0/0f7e3662623656454fcd2b650f34e886a7db4b9104504885bd462096cc7a9f51)
    


      0%|          | 0/1 [00:00<?, ?it/s]


## 设置一个链
现在我们需要创建一些用于问答的管道。第一步是针对所需的数据创建索引。


```python
from langchain.document_loaders import TextLoader

loader = TextLoader("../../modules/paul_graham_essay.txt")
```


```python
from langchain.indexes import VectorstoreIndexCreator
```


```python
vectorstore = VectorstoreIndexCreator().from_loaders([loader]).vectorstore
```

    运行Chroma使用直接本地API。将使用内存中的DuckDB。数据将是暂时的。
    

现在我们可以创建一个问答链。


```python
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
```


```python
chain = RetrievalQA.from_chain_type(
    llm=OpenAI(),
    chain_type="stuff",
    retriever=vectorstore.as_retriever(),
    input_key="question",
)
```

## 进行预测

首先，我们可以逐个数据点进行预测。以这种粒度进行预测允许我们详细探索输出，并且比运行多个数据点要便宜得多


```python
chain(dataset[0])
```




    {'question': '作者上大学前主要从事哪两个方面的工作？',
     'answer': '作者上大学前主要从事写作和编程。',
     'result': ' 写作和编程.'}



## 进行多次预测
现在我们可以进行多次预测


```python
predictions = chain.apply(dataset)
```

## 评估性能
现在我们可以评估预测结果。第一件事情是可以通过视觉查看它们。


```python
predictions[0]
```




    {'question': '作者上大学前主要从事哪两个方面的工作？',
     'answer': '作者上大学前主要从事写作和编程。',
     'result': ' 写作和编程.'}



接下来，我们可以使用语言模型对它们进行程序化评分


```python
from langchain.evaluation.qa import QAEvalChain
```


```python
llm = OpenAI(temperature=0)
eval_chain = QAEvalChain.from_llm(llm)
graded_outputs = eval_chain.evaluate(
    dataset, predictions, question_key="question", prediction_key="result"
)
```

我们可以将评分输出添加到`predictions`字典中，然后计算各个等级的数量。


```python
for i, prediction in enumerate(predictions):
    prediction["grade"] = graded_outputs[i]["text"]
```


```python
from collections import Counter

Counter([pred["grade"] for pred in predictions])
```




    Counter({' CORRECT': 12, ' INCORRECT': 10})



我们还可以将数据点过滤为错误示例并查看它们。


```python
incorrect = [pred for pred in predictions if pred["grade"] == " INCORRECT"]
```


```python
incorrect[0]
```




    {'question': '作者的论文写在哪里？',
     'answer': '作者的论文写在continuations的应用方面。',
     'result': ' 作者没有提及他们的论文是关于什么，所以不知道。',
     'grade': ' INCORRECT'}




```python

```
