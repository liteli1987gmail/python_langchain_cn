# Baseten（ Baseten ）

学习如何在 Baseten 上使用 LangChain 与部署的模型

## 安装和设置

- 创建一个 [Baseten](https://baseten.co) 账户和 [API key](https://docs.baseten.co/settings/api-keys).
- 使用 `pip install baseten` 安装 Baseten Python 客户端
- 使用 API key 进行身份验证 `baseten login`

## 调用模型

Baseten 通过 LLM 模块与 LangChain 集成，为部署在 Baseten 工作区上的模型提供了标准化和互操作的接口。

您可以从 [Baseten 模型库](https://app.baseten.co/explore/) 随时一键部署基础模型，如 WizardLM 和 Alpaca，或者如果您有自己的模型，可以按照 [此教程](https://docs.baseten.co/deploying-models/deploy) 部署它。

在这个示例中，我们将使用 WizardLM。[在这里部署 WizardLM](https://app.baseten.co/explore/wizardlm)，并按照部署的 [模型版本 ID](https://docs.baseten.co/managing-models/manage) 进行操作。

```python
from langchain.llms import Baseten

wizardlm = Baseten(model="MODEL_VERSION_ID", verbose=True)

wizardlm("What is the difference between a Wizard and a Sorcerer?")
```
