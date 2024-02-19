# rag-aws-kendra

这个模板是一个应用程序，利用了Amazon Kendra，一个机器学习驱动的搜索服务，和Anthropic Claude用于文本生成。该应用程序使用检索链来检索文档，以回答来自文档的问题。

它使用`boto3`库与Bedrock服务进行连接。

有关使用Amazon Kendra构建RAG应用程序的更多上下文，请查看[此页面](https://aws.amazon.com/blogs/machine-learning/quickly-build-high-accuracy-generative-ai-applications-on-enterprise-data-using-amazon-kendra-langchain-and-large-language-models/)。

## 环境设置

请确保设置和配置`boto3`以与您的AWS账户配合使用。

您可以按照[这里](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#configuration)的指南进行操作。

在使用此模板之前，您还应该设置好Kendra索引。

您可以使用[此Cloudformation模板](https://github.com/aws-samples/amazon-kendra-langchain-extensions/blob/main/kendra_retriever_samples/kendra-docs-index.yaml)创建一个示例索引。

其中包含了包含Amazon Kendra、Amazon Lex和Amazon SageMaker的AWS在线文档的示例数据。或者，如果您已经对自己的数据集进行了索引，也可以使用您自己的Amazon Kendra索引。

需要设置以下环境变量：

* `AWS_DEFAULT_REGION` - 这应该反映出正确的AWS区域。默认为`us-east-1`。
* `AWS_PROFILE` - 这应该反映出您的AWS配置文件。默认为`default`。
* `KENDRA_INDEX_ID` - 这应该是Kendra索引的索引ID。请注意，索引ID是一个包含36个字符的字母数字值，可以在索引详细信息页面中找到。

## 使用方法

要使用此包，您首先应该安装LangChain CLI：

```shell
pip install -U langchain-cli
```

要创建一个新的LangChain项目并将其安装为唯一的包，可以执行以下操作：

```shell
langchain app new my-app --package rag-aws-kendra
```

如果要将其添加到现有项目中，只需运行：

```shell
langchain app add rag-aws-kendra
```

并将以下代码添加到您的`server.py`文件中：
```python
from rag_aws_kendra.chain import chain as rag_aws_kendra_chain

add_routes(app, rag_aws_kendra_chain, path="/rag-aws-kendra")
```

（可选）现在让我们配置LangSmith。
LangSmith将帮助我们跟踪、监视和调试LangChain应用程序。
LangSmith目前处于私有测试版，您可以在[这里](https://smith.langchain.com/)注册。
如果您没有访问权限，可以跳过此部分。

```shell
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=<your-api-key>
export LANGCHAIN_PROJECT=<your-project>  # 如果未指定，默认为"default"
```

如果您在此目录中，则可以直接启动LangServe实例：

```shell
langchain serve
```

这将在本地启动一个运行在[http://localhost:8000](http://localhost:8000)的FastAPI应用程序的服务器。

我们可以在[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)上查看所有模板。
我们可以在[http://127.0.0.1:8000/rag-aws-kendra/playground](http://127.0.0.1:8000/rag-aws-kendra/playground)上访问playground。

我们可以通过以下代码访问模板：

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/rag-aws-kendra")
```
=======

请将翻译结果返回给我。