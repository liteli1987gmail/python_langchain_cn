# 从包中启动LangServe

您还可以直接从包中启动LangServe，而无需将其拉入项目中。
当您开发一个包并希望快速测试时，这可能非常有用。
这样做的缺点是，您对LangServe API的配置控制较少，
因此对于正式的项目，我们建议创建一个完整的项目。

要做到这一点，首先将工作目录更改为包本身。
例如，如果您当前在这个`templates`模块中，您可以进入`pirate-speak`包：

```shell
cd pirate-speak
```

在这个包中有一个`pyproject.toml`文件。
该文件包含一个`tool.langchain`部分，其中包含有关如何使用此包的信息。
例如，在`pirate-speak`中，我们可以看到：

```text
[tool.langserve]
export_module = "pirate_speak.chain"
export_attr = "chain"
```

可以使用这些信息自动启动LangServe实例。
为此，请确保已安装CLI：

```shell
pip install -U langchain-cli
```

然后运行：

```shell
langchain template serve
```

这将为该链启动端点、文档和游乐场。
例如，您可以在[http://127.0.0.1:8000/playground/](http://127.0.0.1:8000/playground/)上访问游乐场。

![LangServe游乐场Web界面的屏幕截图，显示输入和输出字段。](/img/playground.png "LangServe游乐场界面")