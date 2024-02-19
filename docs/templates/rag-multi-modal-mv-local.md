# rag-multi-modal-mv-local

视觉搜索对于许多使用iPhone或Android设备的人来说是一个熟悉的应用程序。它允许用户使用自然语言搜索照片。

通过开源的多模态LLM的发布，您可以为自己的私人照片集构建这种类型的应用程序。

此模板演示了如何对您的照片集执行私人视觉搜索和问答。

它使用您选择的开源多模态LLM为每张照片创建图像摘要，嵌入摘要，并将其存储在Chroma中。

给定一个问题，相关的照片将被检索并传递给多模态LLM进行答案合成。

![使用多模态LLM进行视觉搜索过程的图示，包括食物图片、字幕、数据库、问题输入以及使用多模态LLM合成答案的过程。](https://github.com/langchain-ai/langchain/assets/122662504/cd9b3d82-9b06-4a39-8490-7482466baf43 "视觉搜索过程图示")

## 输入

在`/docs`目录中提供一组照片。

默认情况下，此模板有一个包含3张食物图片的玩具集合。

该应用程序将根据提供的关键字或问题查找和总结照片：
```
我吃了什么样的冰淇淋？
```

在实践中，可以测试更大的图像语料库。

要创建图像的索引，请运行：
```
poetry install
python ingest.py
```

## 存储

以下是模板将用于创建幻灯片索引的过程（参见[博客](https://blog.langchain.dev/multi-modal-rag-template/)）：

* 给定一组图像
* 使用本地多模态LLM（[bakllava](https://ollama.ai/library/bakllava)）对每个图像进行总结
* 将图像摘要与原始图像的链接嵌入
* 根据图像摘要与用户输入之间的相似性，检索相关图像（使用Ollama嵌入）
* 将这些图像传递给bakllava进行答案合成

默认情况下，这将使用[LocalFileStore](https://python.langchain.com/docs/integrations/stores/file_system)存储图像，并使用Chroma存储摘要。

## LLM和嵌入模型

我们将使用[Ollama](https://python.langchain.com/docs/integrations/chat/ollama#multi-modal)生成图像摘要、嵌入和最终的图像问答。

下载最新版本的Ollama：https://ollama.ai/

获取一个开源的多模态LLM：例如https://ollama.ai/library/bakllava

获取一个开源的嵌入模型：例如https://ollama.ai/library/llama2:7b

```
ollama pull bakllava
ollama pull llama2:7b
```

该应用程序默认配置为`bakllava`。但是您可以在`chain.py`和`ingest.py`中更改此配置以使用不同的下载模型。

该应用程序将根据文本输入和图像摘要之间的相似性检索图像，并将图像传递给`bakllava`。

## 使用方法

要使用此软件包，您首先应该安装LangChain CLI：

```shell
pip install -U langchain-cli
```

要创建一个新的LangChain项目并将其安装为唯一的软件包，可以执行以下操作：

```shell
langchain app new my-app --package rag-multi-modal-mv-local
```

如果要将其添加到现有项目中，只需运行：

```shell
langchain app add rag-multi-modal-mv-local
```

并将以下代码添加到您的`server.py`文件中：
```python
from rag_multi_modal_mv_local import chain as rag_multi_modal_mv_local_chain

add_routes(app, rag_multi_modal_mv_local_chain, path="/rag-multi-modal-mv-local")
```

（可选）现在让我们配置LangSmith。
LangSmith将帮助我们跟踪、监视和调试LangChain应用程序。
LangSmith目前处于私有测试版，您可以在[此处](https://smith.langchain.com/)注册。
如果您没有访问权限，可以跳过此部分

```shell
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=<your-api-key>
export LANGCHAIN_PROJECT=<your-project>  # 如果未指定，默认为"default"
```

如果您在此目录中，则可以直接启动LangServe实例：

```shell
langchain serve
```

这将在本地启动FastAPI应用程序，服务器正在运行，地址为
[http://localhost:8000](http://localhost:8000)

我们可以在[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)上查看所有模板
我们可以在[http://127.0.0.1:8000/rag-multi-modal-mv-local/playground](http://127.0.0.1:8000/rag-multi-modal-mv-local/playground)上访问playground

我们可以通过以下代码访问模板：

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/rag-multi-modal-mv-local")
```
=======