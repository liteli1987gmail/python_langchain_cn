# 问题回答基准测试：Paul Graham Essay

在这里，我们将介绍如何在Paul Graham的文章上对问题回答任务的性能进行基准测试。

强烈建议您在启用跟踪的情况下进行任何评估/基准测试。有关跟踪是什么以及如何设置的解释，请参见[这里](https$：//langchain.readthedocs.io/en/latest/tracing.html)。

```python
# 如果您不使用跟踪，请将其注释
import os

os.environ["LANGCHAIN_HANDLER"] = "langchain"
```

## 加载数据
首先，让我们加载数据。

```python
from langchain.evaluation.loading import load_dataset

dataset = load_dataset("question-answering-paul-graham")
```

    找到缓存的数据集json（/Users/harrisonchase/.cache/huggingface/datasets/LangChainDatasets___json/LangChainDatasets--question-answering-paul-graham-76e8f711e038d742/0.0.0/0f7e3662623656454fcd2b650f34e886a7db4b9104504885bd462096cc7a9f51）
    


      0%|          | 0/1 [00:00<?, ?it/s]


## 设置管道
现在我们需要创建一些用于问题回答的管道。其中第一步是在相关数据上创建索引。


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

    使用直接的本地API运行Chroma。 使用DuckDB内存中的数据库。 数据将是短暂的。
    

现在我们可以创建一个问题回答的管道。


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
首先，我们可以逐个数据点进行预测。以这种粒度进行预测可以让我们详细了解输出结果，而且比运行多个数据点要便宜得多。


```python
chain(dataset[0])
```




    {'question': '作者在上大学之前主要从事哪两个方面的工作？',
     'answer': '作者在上大学之前主要从事写作和编程。',
     'result': '写作和编程。'}



## 进行多次预测
现在我们可以进行多次预测。


```python
predictions = chain.apply(dataset)
```

## 评估性能
现在我们可以评估预测结果。首先，我们可以直接查看预测结果。


```python
predictions[0]
```




    {'question': '作者在上大学之前主要从事哪两个方面的工作？',
     'answer': '作者在上大学之前主要从事写作和编程。',
     'result': '写作和编程。'}



接下来，我们可以使用语言模型对它们进行程序化评分。


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




    Counter({'CORRECT': 12, 'INCORRECT': 10})



我们还可以将数据点过滤为错误示例并查看它们。


```python
incorrect = [pred for pred in predictions if pred["grade"] == "INCORRECT"]
```


```python
incorrect[0]
```




    {'question': '作者写的论文是关于什么的？',
     'answer': '作者的论文是关于continuations的应用。',
     'result': '作者没有提到他们的论文是关于什么，所以不得而知。',
     'grade': 'INCORRECT'}




```python

```
