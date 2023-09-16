# 基准模板

这是一个示例笔记本，可用于为您选择的任务创建基准笔记本。评估非常困难，因此我们非常欢迎任何可以使人们更容易进行实验的贡献

强烈建议您在启用跟踪的情况下进行任何评估/基准测试。有关跟踪是什么以及如何设置它的解释，请参见[这里](https://langchain.readthedocs.io/en/latest/tracing.html)


```python
# 如果您不使用跟踪，请注释掉此行
import os

os.environ["LANGCHAIN_HANDLER"] = "langchain"
```

## 加载数据

首先，让我们加载数据。


```python
# 此笔记本应该展示如何从Hugging Face的LangChainDatasets加载数据集

# 请将您的数据集上传到https://huggingface.co/LangChainDatasets

# `load_dataset` 中传递的值不应具有`LangChainDatasets/`前缀
from langchain.evaluation.loading import load_dataset

dataset = load_dataset("TODO")
```

## 设置链

接下来的部分应该有一个设置可以在该数据集上运行的链的示例。


```python

```

## 进行预测

首先，我们可以逐个数据点进行预测。以这种粒度进行预测允许我们详细探索输出，而且比运行多个数据点要便宜得多


```python
# 在这里放置在单个数据点上运行链的示例（`dataset[0]`）
```

## 进行多次预测

现在我们可以进行预测。


```python
# 在这里放置在多个预测上运行链的示例

# 有时只需简单地使用 `chain.apply(dataset)`

# 其他情况下，您可能需要编写一个for循环来捕获错误
```

## 评估性能

任何关于以更系统的方式评估性能的指南都在这里。


```python

```
