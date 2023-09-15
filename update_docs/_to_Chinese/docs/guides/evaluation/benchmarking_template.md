# 基准模板

这是一个示例笔记本，可用于为您选择的任务创建基准测试笔记本。评估是非常困难的，因此我们非常欢迎任何可以使人们更容易进行实验的贡献

强烈建议您在启用跟踪的情况下进行任何评估/基准测试。请参见[此处](https://langchain.readthedocs.io/en/latest/tracing.html)了解跟踪的解释和设置方法


```python
# 如果您不使用跟踪，请注释掉此行
import os

os.environ["LANGCHAIN_HANDLER"] = "langchain"
```

## 加载数据

首先，让我们加载数据。


```python
# 本笔记本应该展示如何从Hugging Face上的LangChainDatasets加载数据集

# 请将您的数据集上传到https://huggingface.co/LangChainDatasets

# 传递给`load_dataset`的值不应带有`LangChainDatasets/`前缀
from langchain.evaluation.loading import load_dataset

dataset = load_dataset("TODO")
```

## 设置链

下一节应该有一个设置链的示例，可以在此数据集上运行。


```python

```

## 进行预测

首先，我们可以逐个数据点进行预测。以这种粒度进行预测允许我们详细探索输出，而且比在多个数据点上运行要便宜得多


```python
# 在这里放置在单个数据点（`dataset[0]`）上运行链的示例
```

## 进行多次预测
现在我们可以进行预测。


```python
# 在这里放置对多个预测运行链的示例

# 有时只需使用`chain.apply(dataset)`即可

# 其他情况下，您可能希望编写一个for循环以捕获错误
```

## 评估性能

在这里提供评估性能的指南。


```python

```
