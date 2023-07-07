Databricks
==========

[Databricks](https://www.databricks.com/) Lakehouse 平台将数据、分析和 AI 统一在一个平台上。

Databricks 以多种方式支持 LangChain 生态系统：

1. 用于 SQLDatabase Chain 的 Databricks 连接器：SQLDatabase.from_databricks()通过 LangChain 提供了一种在 Databricks 上查询数据的简单方式。
2. Databricks 托管的 MLflow 与 LangChain 集成：通过较少的步骤跟踪和提供 LangChain 应用程序。
3. Databricks 作为 LLM 提供者：通过服务端点或集群驱动程序代理应用程序在 Databricks 上部署精细调整的 LLMs，并使用 langchain.llms.Databricks 查询它。
4. Databricks Dolly：Databricks 开源的 Dolly 允许商业使用，并可通过 Hugging Face Hub 访问。

SQLDatabase Chain 的 Databricks 连接器
----------------------------------------------
您可以使用 LangChain 的 SQLDatabase 包装器连接到 [Databricks 运行时](https://docs.databricks.com/runtime/index.html) 和 [Databricks SQL](https://www.databricks.com/product/databricks-sql)。有关详细信息，请参阅笔记本 [连接到 Databricks](./databricks/databricks.html)。

Databricks 托管的 MLflow 与 LangChain 集成
---------------------------------------------------

MLflow 是一个开源平台，用于管理机器学习生命周期，包括实验、可重复性、部署和中央模型注册表。有关 MLflow 与 LangChain 集成的详细信息，请参阅笔记本 [MLflow 回调处理程序](./mlflow_tracking.ipynb)。

Databricks 提供了一个完全托管和托管的 MLflow 版本，集成了企业安全功能、高可用性和其他 Databricks 工作空间功能，如实验和运行管理以及笔记本修订捕获。Databricks 上的 MLflow 为跟踪和保护机器学习模型训练运行以及运行机器学习项目提供了集成体验。有关更多详细信息，请参阅 [MLflow 指南](https://docs.databricks.com/mlflow/index.html)。

Databricks 托管的 MLflow 使在 Databricks 上开发 LangChain 应用程序更加便捷。对于 MLflow 跟踪，您不需要设置跟踪 URI。对于 MLflow 模型服务，您可以将 LangChain Chains 保存在 MLflow langchain 风格中，然后通过 Databricks 上的几次点击注册和提供 Chain，凭据由 MLflow 模型服务安全管理。

Databricks 作为 LLM 提供者
-----------------------------

笔记本 [将 Databricks 端点包装为 LLMs](../modules/models/llms/integrations/databricks.html) 介绍了在 LangChain 中将 Databricks 端点包装为 LLMs 的方法。它支持两种类型的端点：建议在生产和开发中使用的服务端点，以及建议在交互式开发中使用的集群驱动程序代理应用程序。

Databricks 端点支持 Dolly，但也非常适合托管像 MPT-7B 这样的模型，或者来自 Hugging Face 生态系统的任何其他模型。Databricks 端点还可以与 OpenAI 等专有模型一起使用，为企业提供治理层。

Databricks Dolly
----------------

Databricks 的 Dolly 是在 Databricks 机器学习平台上训练的一个遵循指令的大型语言模型，可用于商业用途。该模型在 Hugging Face Hub 上作为 databricks/dolly-v2-12b 提供。有关通过 Hugging Face Hub 与 LangChain 集成访问它的说明，请参阅笔记本 [Hugging Face Hub](../modules/models/llms/integrations/huggingface_hub.html)。
