# 问题回答基准测试: 国情咨文

在这里，我们将介绍如何对国情咨文上的问题回答任务进行性能基准测试。

强烈建议在进行任何评估/基准测试时启用追踪。有关追踪是什么以及如何设置，请参见[这里](https$：//langchain.readthedocs.io/en/latest/tracing.html)。


```python
# 如果您不使用追踪，请将此代码注释掉
import os

os.environ["LANGCHAIN_HANDLER"] = "langchain"
```

## 加载数据
首先，让我们加载数据。


```python
from langchain.evaluation.loading import load_dataset

dataset = load_dataset("question-answering-state-of-the-union")
```

    找到缓存的数据集JSON（/Users/harrisonchase/.cache/huggingface/datasets/LangChainDatasets___json/LangChainDatasets--question-answering-state-of-the-union-a7e5a3b2db4f440d/0.0.0/0f7e3662623656454fcd2b650f34e886a7db4b9104504885bd462096cc7a9f51）
    


      0％|          | 0/1 [00$：00<?, ?it/s]


## 创建链式结构
现在我们需要创建一些用于问题回答的管道。其中一步是针对所讨论的数据创建索引。


```python
from langchain.document_loaders import TextLoader

loader = TextLoader("../../modules/state_of_the_union.txt")
```


```python
from langchain.indexes import VectorstoreIndexCreator
```


```python
vectorstore = VectorstoreIndexCreator().from_loaders([loader]).vectorstore
```

    使用直接本地API运行Chroma。将在内存中使用DuckDB数据库。数据将是暂时的。
    

现在我们可以创建一个问题回答链。


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
首先，我们可以逐个数据点进行预测。以这种细粒度的方式进行预测允许我们详细探索输出，并且比多个数据点运行要便宜得多。


```python
chain(dataset[0])
```




    {'question': '北约联盟的目的是什么？',
     'answer': '北约联盟的目的是在第二次世界大战后确保欧洲的和平与稳定。',
     'result': '北约联盟的目的是在第二次世界大战后确保欧洲的和平与稳定。'}



## 进行多次预测
现在我们可以进行多次预测。


```python
predictions = chain.apply(dataset)
```

## 评估性能
现在我们可以评估预测结果。首先，我们可以通过目测来查看它们。


```python
predictions[0]
```




    {'question': '北约联盟的目的是什么？',
     'answer': '北约联盟的目的是在第二次世界大战后确保欧洲的和平与稳定。',
     'result': '北约联盟的目的是在第二次世界大战后确保欧洲的和平与稳定。'}



接下来，我们可以使用语言模型对其进行编程评分。


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




    Counter({' CORRECT': 7, ' INCORRECT': 4})



我们还可以将数据点筛选为不正确的示例并查看它们。


```python
incorrect = [pred for pred in predictions if pred["grade"] == " INCORRECT"]
```


```python
incorrect[0]
```




    {'question': '美国司法部正在采取什么措施打击俄罗斯寡头的犯罪行为？',
     'answer': '美国司法部正在组建一个专门的工作组来打击俄罗斯寡头的犯罪行为。',
     'result': '美国司法部正在组建一个专门的工作组来打击俄罗斯寡头的犯罪行为，并任命一名首席检察官负责处理疫情欺诈。',
     'grade': ' INCORRECT'}




```python

```
