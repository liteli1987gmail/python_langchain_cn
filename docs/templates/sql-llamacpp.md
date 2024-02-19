# sql-llamacpp

这个模板使用户能够使用自然语言与SQL数据库进行交互。

它使用[Mistral-7b](https://mistral.ai/news/announcing-mistral-7b/)通过[llama.cpp](https://github.com/ggerganov/llama.cpp)在Mac笔记本上本地运行推理。

## 环境设置

要设置环境，请按照以下步骤进行操作：

```shell
wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-arm64.sh
bash Miniforge3-MacOSX-arm64.sh
conda create -n llama python=3.9.16
conda activate /Users/rlm/miniforge3/envs/llama
CMAKE_ARGS="-DLLAMA_METAL=on" FORCE_CMAKE=1 pip install -U llama-cpp-python --no-cache-dir
```

## 使用方法

要使用此包，您首先应该安装LangChain CLI：

```shell
pip install -U langchain-cli
```

要创建一个新的LangChain项目并将其安装为唯一的包，可以执行以下操作：

```shell
langchain app new my-app --package sql-llamacpp
```

如果要将其添加到现有项目中，只需运行：

```shell
langchain app add sql-llamacpp
```

并将以下代码添加到您的`server.py`文件中：
```python
from sql_llamacpp import chain as sql_llamacpp_chain

add_routes(app, sql_llamacpp_chain, path="/sql-llamacpp")
```

该包将从[此处](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF)下载Mistral-7b模型。您可以选择其他文件并指定其下载路径（浏览[此处](https://huggingface.co/TheBloke)）。

此包包含一个2023年NBA名单的示例数据库。您可以在[此处](https://github.com/facebookresearch/llama-recipes/blob/main/demo_apps/StructuredLlama.ipynb)查看构建此数据库的说明。

（可选）配置LangSmith以跟踪、监视和调试LangChain应用程序。LangSmith目前处于私有测试版，您可以在[此处](https://smith.langchain.com/)注册。如果您没有访问权限，可以跳过此部分。

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

您可以在[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)上查看所有模板。
您可以在[http://127.0.0.1:8000/sql-llamacpp/playground](http://127.0.0.1:8000/sql-llamacpp/playground)上访问playground。

您可以通过以下代码访问模板：

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/sql-llamacpp")
```
=======