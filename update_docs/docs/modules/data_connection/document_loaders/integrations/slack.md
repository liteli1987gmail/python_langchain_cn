# Slack

>[Slack](https://slack.com/) 是一个即时通讯程序。

这个笔记本介绍了如何从 Slack 导出生成的 Zip 文件中加载文档。

要获得这个 Slack 导出，请按照以下说明操作：

## 🟡 自己导入数据集的说明

导出您的 Slack 数据。您可以通过转到您的 Workspace Management 页面并点击 Import/Export 选项 ({your_slack_domain}.slack.com/services/export) 来完成此操作。然后，选择正确的日期范围并点击“开始导出”。当导出准备好时，Slack 会向您发送一封电子邮件和一条直接消息。

下载将在您的下载文件夹中生成一个 `.zip` 文件（或者根据您的操作系统配置，可以在其他地方找到您的下载文件）。复制 `.zip` 文件的路径，并将其分配给下面的 `LOCAL_ZIPFILE`。

```python
from langchain.document_loaders import SlackDirectoryLoader
```


```python
# 可选地设置您的 Slack URL。这将在文档源中提供正确的 URL。
SLACK_WORKSPACE_URL = "https://xxx.slack.com"
LOCAL_ZIPFILE = ""  # 在此处粘贴到您的 Slack zip 文件的本地路径。

loader = SlackDirectoryLoader(LOCAL_ZIPFILE, SLACK_WORKSPACE_URL)
```


```python
docs = loader.load()
docs
```