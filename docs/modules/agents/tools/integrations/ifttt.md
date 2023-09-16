# IFTTT WebHooks

这个笔记本展示了如何使用IFTTT Webhooks。

从 https://github.com/SidU/teams-langchain-js/wiki/Connecting-IFTTT-Services。

## 创建一个Webhook

- 前往 https://ifttt.com/create

## 配置"If This"

- 在IFTTT界面上点击"If This"按钮。
- 在搜索栏中搜索"Webhooks"。
- 选择"用JSON负载接收Web请求"的第一个选项。
- 选择一个特定于您要连接的服务的事件名称。
例如，如果您要连接Spotify，可以使用"Spotify"作为您的事件名称。
- 点击"创建触发器"按钮保存设置并创建Webhook。

## 配置"Then That"

- 在IFTTT界面上点击"Then That"按钮。
- 搜索您想要连接的服务，例如Spotify。
- 从该服务中选择一个操作，例如"将曲目添加到播放列表"。
- 通过指定必要的详细信息（例如播放列表名称）配置操作，例如"Songs from AI"。
- 在您的操作中引用Webhook接收到的JSON负载。对于Spotify场景，选择"{{JsonPayload}}"作为您的搜索查询。
- 点击"创建动作"按钮保存操作设置。
- 完成配置操作后，点击"完成"按钮完成设置。

## 结束

- 要获取您的Webhook URL，请访问 https://ifttt.com/maker_webhooks/settings
- 复制IFTTT密钥值。URL的形式为 https://maker.ifttt.com/use/YOUR_IFTTT_KEY。获取YOUR_IFTTT_KEY的值。

```python
from langchain.tools.ifttt import IFTTTWebhook
```

```python
import os

key = os.environ["IFTTTKey"]
url = f"https://maker.ifttt.com/trigger/spotify/json/with/key/{key}"
tool = IFTTTWebhook(
    name="Spotify", description="Add a song to spotify playlist", url=url
)
```

```python
tool.run("taylor swift")
```
```
"恭喜！您已成功将Webhook连接到所需的服务，并且准备开始接收数据和触发动作 🎉"
```

```python

```