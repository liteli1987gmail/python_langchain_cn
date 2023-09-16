# Telegram

>[Telegram Messenger](https://web.telegram.org/a/) 是一种全球可访问的免费、跨平台、加密、云端和集中式即时通讯服务。该应用还提供可选择的端到端加密聊天和视频通话、VoIP、文件共享和其他多种功能。

本笔记本介绍了如何将数据从 `Telegram` 加载到可以被 LangChain 吸收的格式中。

```python
from langchain.document_loaders import TelegramChatFileLoader, TelegramChatApiLoader
```

```python
loader = TelegramChatFileLoader("example_data/telegram.json")
```

```python
loader.load()
```


[Document(page_content="Henry on 2020-01-01T00:00:02: It's 2020...\n\nHenry on 2020-01-01T00:00:04: Fireworks!\n\nGrace ðŸ§¤ ðŸ\x8d’ on 2020-01-01T00:00:05: You're a minute late!\n\n", metadata={'source': 'example_data/telegram.json'})]


`TelegramChatApiLoader` 可以直接从 Telegram 中加载数据。为了导出数据，您需要对 Telegram 账户进行身份验证。

您可以从 https://my.telegram.org/auth?to=apps 获取 API_HASH 和 API_ID。

chat_entity – 建议使用频道的 [实体](https://docs.telethon.dev/en/stable/concepts/entities.html?highlight=Entity#what-is-an-entity)。

```python
loader = TelegramChatApiLoader(
    chat_entity="<CHAT_URL>",  # recommended to use Entity here
    api_hash="<API HASH >",
    api_id="<API_ID>",
    user_name="",  # needed only for caching the session.
)
```

```python
loader.load()
```


```python

```