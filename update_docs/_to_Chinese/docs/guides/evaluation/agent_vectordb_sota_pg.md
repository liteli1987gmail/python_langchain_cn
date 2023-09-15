# Agent VectorDB Question Answering Benchmarking

这里我们将介绍如何使用代理在多个向量数据库之间进行问题回答任务的性能基准测试。

强烈建议您在进行任何评估/基准测试时启用追踪。请参阅[这里](https://python.langchain.com/guides/tracing/)了解追踪是什么以及如何设置。


```python
# 如果您没有使用追踪，请注释掉以下代码
import os

os.environ["LANGCHAIN_HANDLER"] = "langchain"
```

## 加载数据
首先，让我们加载数据。


```python
from langchain.evaluation.loading import load_dataset

dataset = load_dataset("agent-vectordb-qa-sota-pg")
```

    找到缓存的数据集json (/Users/qt/.cache/huggingface/datasets/LangChainDatasets___json/LangChainDatasets--agent-vectordb-qa-sota-pg-d3ae24016b514f92/0.0.0/fe5dd6ea2639a6df622901539cb550cf8797e5a6b2dd7af1cf934bed8e233e6e)
    100%|██████████| 1/1 [00:00<00:00, 414.42it/s]
    


```python
dataset[0]
```




    {'question': '北约联盟的目的是什么？',
     'answer': '北约联盟的目的是在二战后确保欧洲的和平与稳定。',
     'steps': [{'tool': '国情咨文问答系统', 'tool_input': None},
      {'tool': None, 'tool_input': '北约联盟的目的是什么？'}]}




```python
dataset[-1]
```




    {'question': 'YC的目的是什么？',
     'answer': 'YC的目的是创办那些本来不会存在的初创公司。',
     'steps': [{'tool': 'Paul Graham问答系统', 'tool_input': None},
      {'tool': None, 'tool_input': 'YC的目的是什么？'}]}



## 设置链
现在我们需要为问题回答创建一些流水线。其中的第一步是在问题的数据上创建索引。


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

    使用内嵌的DuckDB而无需持久化: 数据将是临时的
    

现在我们可以创建一个问题回答链。


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

现在我们对Paul Graham的数据做同样的操作。


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

    使用内嵌的DuckDB而无需持久化: 数据将是临时的
    


```python
chain_pg = RetrievalQA.from_chain_type(
    llm=OpenAI(temperature=0),
    chain_type="stuff",
    retriever=vectorstore_pg.as_retriever(),
    input_key="question",
)
```

现在我们可以设置一个代理来在它们之间进行路由。


```python
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType

tools = [
    Tool(
        name="国情咨文问答系统",
        func=chain_sota.run,
        description="当您需要回答关于最新国情咨文演讲的问题时非常有用。输入应该是一个完整的问题。",
    ),
    Tool(
        name="Paul Graham系统",
        func=chain_pg.run,
        description="当您需要回答关于Paul Graham的问题时非常有用。输入应该是一个完整的问题。",
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

## 进行预测

首先，我们可以逐个数据点进行预测。以这种粒度进行预测允许我们详细探索输出，而且比多个数据点运行更便宜。


```python
agent.run(dataset[0]["question"])
```




    '北约联盟的目的是在二战后确保欧洲的和平与稳定。'



## 进行多次预测
现在我们可以进行多次预测。


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

## 评估性能
现在我们可以评估预测结果。首先，我们可以通过目测来查看它们。


```python
predictions[0]
```




    {'input': '北约联盟的目的是什么？',
     'answer': '北约联盟的目的是在二战后确保欧洲的和平与稳定。',
     'output': '北约联盟的目的是在二战后确保欧洲的和平与稳定。'}



接下来，我们可以使用语言模型对它们进行程序化评分。


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

我们可以将评分输出添加到`predictions`字典中，然后统计各个等级的数量。


```python
for i, prediction in enumerate(predictions):
    prediction["grade"] = graded_outputs[i]["text"]
```


```python
from collections import Counter

Counter([pred["grade"] for pred in predictions])
```




    Counter({' CORRECT': 28, ' INCORRECT': 5})



我们还可以将数据点过滤为错误的示例并查看它们。


```python
incorrect = [pred for pred in predictions if pred["grade"] == " INCORRECT"]
```


```python
incorrect[0]
```




    {'input': '四个常识步骤是什么，作者建议以安全的方式前进？',
     'answer': '四个常识步骤是: 通过疫苗和治疗保护自己，为新变种做好准备，结束学校和企业的关闭，保持警惕。',
     'output': '最近国情咨文演讲中建议的四个常识步骤是: 降低处方药费用，为梦想家提供公民身份的途径，修改法律以便企业拥有他们所需的工人并且家庭不必等待数十年才能团聚，以及保护医疗保健的获取权并维护妇女选择权。',
     'grade': ' INCORRECT'}


