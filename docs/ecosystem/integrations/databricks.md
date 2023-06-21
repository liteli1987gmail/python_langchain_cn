Databricks
==========

[Databricks](https://www.databricks.com/) Lakehouse平台将数据、分析和AI统一在一个平台上。

Databricks以多种方式支持LangChain生态系统：

1. 用于SQLDatabase Chain的Databricks连接器：SQLDatabase.from_databricks()通过LangChain提供了一种在Databricks上查询数据的简单方式。
2. Databricks托管的MLflow与LangChain集成：通过较少的步骤跟踪和提供LangChain应用程序。
3. Databricks作为LLM提供者：通过服务端点或集群驱动程序代理应用程序在Databricks上部署精细调整的LLMs，并使用langchain.llms.Databricks查询它。
4. Databricks Dolly：Databricks开源的Dolly允许商业使用，并可通过Hugging Face Hub访问。

SQLDatabase Chain的Databricks连接器
----------------------------------------------
您可以使用LangChain的SQLDatabase包装器连接到[Databricks运行时](https://docs.databricks.com/runtime/index.html)和[Databricks SQL](https://www.databricks.com/product/databricks-sql)。有关详细信息，请参阅笔记本[连接到Databricks](./databricks/databricks.html)。

Databricks托管的MLflow与LangChain集成
---------------------------------------------------

MLflow是一个开源平台，用于管理机器学习生命周期，包括实验、可重复性、部署和中央模型注册表。有关MLflow与LangChain集成的详细信息，请参阅笔记本[MLflow回调处理程序](./mlflow_tracking.ipynb)。

Databricks提供了一个完全托管和托管的MLflow版本，集成了企业安全功能、高可用性和其他Databricks工作空间功能，如实验和运行管理以及笔记本修订捕获。Databricks上的MLflow为跟踪和保护机器学习模型训练运行以及运行机器学习项目提供了集成体验。有关更多详细信息，请参阅[MLflow指南](https://docs.databricks.com/mlflow/index.html)。

Databricks托管的MLflow使在Databricks上开发LangChain应用程序更加便捷。对于MLflow跟踪，您不需要设置跟踪URI。对于MLflow模型服务，您可以将LangChain Chains保存在MLflow langchain风格中，然后通过Databricks上的几次点击注册和提供Chain，凭据由MLflow模型服务安全管理。

Databricks作为LLM提供者
-----------------------------

笔记本[将Databricks端点包装为LLMs](../modules/models/llms/integrations/databricks.html)介绍了在LangChain中将Databricks端点包装为LLMs的方法。它支持两种类型的端点：建议在生产和开发中使用的服务端点，以及建议在交互式开发中使用的集群驱动程序代理应用程序。

Databricks端点支持Dolly，但也非常适合托管像MPT-7B这样的模型，或者来自Hugging Face生态系统的任何其他模型。Databricks端点还可以与OpenAI等专有模型一起使用，为企业提供治理层。

Databricks Dolly
----------------

Databricks的Dolly是在Databricks机器学习平台上训练的一个遵循指令的大型语言模型，可用于商业用途。该模型在Hugging Face Hub上作为databricks/dolly-v2-12b提供。有关通过Hugging Face Hub与LangChain集成访问它的说明，请参阅笔记本[Hugging Face Hub](../modules/models/llms/integrations/huggingface_hub.html)。
