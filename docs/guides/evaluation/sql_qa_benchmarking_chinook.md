# SQL 问题回答基准测试：Chinook

在这里，我们将介绍如何对 SQL 数据库上的问题回答任务进行性能基准测试。

强烈建议您在进行任何评估/基准测试时启用追踪功能。请参阅[这里](https://langchain.readthedocs.io/en/latest/tracing.html)以了解追踪是什么以及如何设置。

```python
# 如果您没有使用追踪，请注释此行
import os
os.environ["LANGCHAIN_HANDLER"] = "langchain"
```

## 加载数据

首先，让我们加载数据。

```python
from langchain.evaluation.loading import load_dataset

dataset = load_dataset("sql-qa-chinook")
```


Downloading readme:   0%|          | 0.00/21.0 [00:00<?, ?B/s]


Downloading and preparing dataset json/LangChainDatasets--sql-qa-chinook to /Users/harrisonchase/.cache/huggingface/datasets/LangChainDatasets___json/LangChainDatasets--sql-qa-chinook-7528565d2d992b47/0.0.0/0f7e3662623656454fcd2b650f34e886a7db4b9104504885bd462096cc7a9f51...


Downloading data files:   0%|          | 0/1 [00:00<?, ?it/s]


Downloading data:   0%|          | 0.00/1.44k [00:00<?, ?B/s]


Extracting data files:   0%|          | 0/1 [00:00<?, ?it/s]


Generating train split: 0 examples [00:00, ? examples/s]


Dataset json downloaded and prepared to /Users/harrisonchase/.cache/huggingface/datasets/LangChainDatasets___json/LangChainDatasets--sql-qa-chinook-7528565d2d992b47/0.0.0/0f7e3662623656454fcd2b650f34e886a7db4b9104504885bd462096cc7a9f51. Subsequent calls will reuse this data.


  0%|          | 0/1 [00:00<?, ?it/s]


```python
dataset[0]
```


{'question': '有多少员工？', 'answer': '8'}


## 设置链

这使用了示例的 Chinook 数据库。
要设置它，请按照 https://database.guide/2-sample-databases-sqlite/ 上的说明，将 `.db` 文件放在此存储库根目录下的 notebooks 文件夹中。

请注意，这里我们加载了一个简单的链。如果您想尝试更复杂的链或代理，请以不同的方式创建 `chain` 对象。

```python
from langchain import OpenAI, SQLDatabase, SQLDatabaseChain
```


```python
db = SQLDatabase.from_uri("sqlite:///../../../notebooks/Chinook.db")
llm = OpenAI(temperature=0)
```

现在我们可以创建一个 SQL 数据库链。

```python
chain = SQLDatabaseChain.from_llm(llm, db, input_key="question")
```


## 进行预测

首先，我们可以逐个数据点进行预测。以这种粒度进行预测允许我们详细探索输出，并且比多个数据点运行更便宜。

```python
chain(dataset[0])
```


{'question': '有多少员工？',
 'answer': '8',
 'result': ' 共有 8 名员工。'}


## 进行多个预测

现在我们可以进行多个预测。请注意，我们添加了 try-except，因为此链有时可能会出错（如果 SQL 编写不正确等）。

```python
predictions = []
predicted_dataset = []
error_dataset = []
for data in dataset:
    try:
        predictions.append(chain(data))
        predicted_dataset.append(data)
    except:
        error_dataset.append(data)
```


## 评估性能

现在我们可以评估预测结果。我们可以使用语言模型对其进行编程评分。

```python
from langchain.evaluation.qa import QAEvalChain
```


```python
llm = OpenAI(temperature=0)
eval_chain = QAEvalChain.from_llm(llm)
graded_outputs = eval_chain.evaluate(
    predicted_dataset, predictions, question_key="question", prediction_key="result"
)
```


我们可以将评分输出添加到 `predictions` 字典中，然后计算分级的数量。

```python
for i, prediction in enumerate(predictions):
    prediction["grade"] = graded_outputs[i]["text"]
```


```python
from collections import Counter

Counter([pred["grade"] for pred in predictions])
```




Counter({' CORRECT': 3, ' INCORRECT': 4})



我们还可以将数据点过滤为不正确的示例并查看它们。

```python
incorrect = [pred for pred in predictions if pred["grade"] == " INCORRECT"]
```


```python
incorrect[0]
```



{'question': '有多少员工也是顾客？',
 'answer': 'None',
 'result': ' 59 名员工也是顾客。',
 'grade': ' INCORRECT'}





```python

```
