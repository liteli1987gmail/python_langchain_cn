# rag-chroma-multi-modal

多模态LLM使得可以对图像进行问答的视觉助手成为可能。

该模板创建了一个用于幻灯片演示的视觉助手，幻灯片演示通常包含图形或图像等可视化内容。

它使用OpenCLIP嵌入将所有幻灯片图像进行嵌入，并将它们存储在Chroma中。

给定一个问题，相关的幻灯片将被检索并传递给GPT-4V进行答案合成。

![用于基于幻灯片演示图像的多模态LLM视觉助手的工作流程的示意图](https://github.com/langchain-ai/langchain/assets/122662504/b3bc8406-48ae-4707-9edf-d0b3a511b200 "多模态LLM视觉助手的工作流程示意图")

## 输入

在`/docs`目录中提供一个pdf格式的幻灯片演示。

默认情况下，该模板提供了一个关于DataDog的Q3收益的幻灯片演示，DataDog是一家公共技术公司。

可以提问的示例问题包括：
```
Datadog有多少客户？
Datadog平台在FY20、FY21和FY22的年度增长率是多少？
```

要创建幻灯片演示的索引，请运行：
```
poetry install
python ingest.py
```

## 存储

该模板将使用[OpenCLIP](https://github.com/mlfoundations/open_clip)多模态嵌入来嵌入图像。

您可以选择不同的嵌入模型选项（在此处查看结果[here](https://github.com/mlfoundations/open_clip/blob/main/docs/openclip_results.csv)）。

第一次运行应用程序时，它将自动下载多模态嵌入模型。

默认情况下，LangChain将使用性能适中但内存要求较低的嵌入模型`ViT-H-14`。

您可以在`rag_chroma_multi_modal/ingest.py`中选择其他`OpenCLIPEmbeddings`模型：
```
vectorstore_mmembd = Chroma(
    collection_name="multi-modal-rag",
    persist_directory=str(re_vectorstore_path),
    embedding_function=OpenCLIPEmbeddings(
        model_name="ViT-H-14", checkpoint="laion2b_s32b_b79k"
    ),
)
```

## LLM

该应用程序将根据文本输入和图像之间的相似性检索图像，并将它们传递给GPT-4V。

## 环境设置

将`OPENAI_API_KEY`环境变量设置为访问OpenAI GPT-4V。

## 使用方法

要使用此软件包，您首先应该安装LangChain CLI：

```shell
pip install -U langchain-cli
```

要创建一个新的LangChain项目并将其安装为唯一的软件包，可以执行以下操作：

```shell
langchain app new my-app --package rag-chroma-multi-modal
```

如果要将其添加到现有项目中，只需运行：

```shell
langchain app add rag-chroma-multi-modal
```

并将以下代码添加到您的`server.py`文件中：
```python
from rag_chroma_multi_modal import chain as rag_chroma_multi_modal_chain

add_routes(app, rag_chroma_multi_modal_chain, path="/rag-chroma-multi-modal")
```

（可选）现在让我们配置LangSmith。
LangSmith将帮助我们跟踪、监视和调试LangChain应用程序。
LangSmith目前处于私有测试阶段，您可以在[此处](https://smith.langchain.com/)注册。
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

这将在本地启动FastAPI应用程序，服务器正在[http://localhost:8000](http://localhost:8000)上运行

我们可以在[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)上查看所有模板
我们可以在[http://127.0.0.1:8000/rag-chroma-multi-modal/playground](http://127.0.0.1:8000/rag-chroma-multi-modal/playground)上访问playground

我们可以通过以下代码访问模板：

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/rag-chroma-multi-modal")
```
