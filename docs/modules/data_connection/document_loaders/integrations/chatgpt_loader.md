### ChatGPT 数据
[ChatGPT](https://chat.openai.com) 是由OpenAI开发的人工智能（AI）聊天机器人。
本文档描述了如何从您的 `ChatGPT` 数据导出文件夹加载 `conversations.json`。
您可以通过电子邮件获取数据导出，方法是转到：https://chat.openai.com/ ->（个人资料）- 设置 -> 导出数据 -> 确认导出。
```python
from langchain.document_loaders.chatgpt import ChatGPTLoader
```

```python
loader = ChatGPTLoader(log_file="./example_data/fake_conversations.json", num_logs=1)
```

```python
loader.load()
```

[Document(page_content="AI Overlords - AI on 2065-01-24 05:20:50: Greetings, humans. I am Hal 9000. You can trust me completely.\n\nAI Overlords - human on 2065-01-24 05:21:20: Nice to meet you, Hal. I hope you won't develop a mind of your own.\n\n", metadata={'source': './example_data/fake_conversations.json'})]



