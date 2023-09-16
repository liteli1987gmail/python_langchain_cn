# WhatsApp Chat
>[WhatsApp](https://www.whatsapp.com/)（也称为`WhatsApp Messenger`）是一款免费的跨平台即时通讯（IM）和网络电话（VoIP）服务。它允许用户发送文字和语音消息，进行语音和视频通话，并分享图像、文档、用户位置和其他内容。

本文档介绍了如何将`WhatsApp Chat`中的数据加载到可以被LangChain摄入的格式中。

```python
from langchain.document_loaders import WhatsAppChatLoader
```

```python
loader = WhatsAppChatLoader("example_data/whatsapp_chat.txt")
```

```python
loader.load()
```
