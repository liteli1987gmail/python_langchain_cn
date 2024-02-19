# Langchain - Robocorp Action Server

这个模板可以将[Robocorp Action Server](https://github.com/robocorp/robocorp)作为Agent的工具来使用。

## 使用方法

要使用这个包，你首先需要安装LangChain CLI:

```shell
pip install -U langchain-cli
```

要创建一个新的LangChain项目并将其作为唯一的包安装，可以执行以下操作:

```shell
langchain app new my-app --package robocorp-action-server
```

如果你想将其添加到现有项目中，只需运行:

```shell
langchain app add robocorp-action-server
```

并将以下代码添加到你的`server.py`文件中:

```python
from robocorp_action_server import agent_executor as action_server_chain

add_routes(app, action_server_chain, path="/robocorp-action-server")
```

### 运行Action Server

要运行Action Server，你需要安装Robocorp Action Server

```bash
pip install -U robocorp-action-server
```

然后你可以使用以下命令运行Action Server:

```bash
action-server new
cd ./your-project-name
action-server start
```

### 配置LangSmith（可选）

LangSmith将帮助我们跟踪、监控和调试LangChain应用程序。
LangSmith目前处于私有测试版，你可以在[这里](https://smith.langchain.com/)注册。
如果你没有访问权限，可以跳过此部分

```shell
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=<your-api-key>
export LANGCHAIN_PROJECT=<your-project>  # 如果未指定，默认为"default"
```

### 启动LangServe实例

如果你在此目录中，可以直接通过以下命令启动LangServe实例:

```shell
langchain serve
```

这将在本地启动FastAPI应用程序的服务器，地址为
[http://localhost:8000](http://localhost:8000)

我们可以在[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)上查看所有模板
我们可以在[http://127.0.0.1:8000/robocorp-action-server/playground](http://127.0.0.1:8000/robocorp-action-server/playground)上访问playground

我们可以通过以下代码访问模板:

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/robocorp-action-server")
```
=======