### ChatGPT Data

>[ChatGPT](https://chat.openai.com) is an artificial intelligence (AI) chatbot developed by OpenAI.


This notebook covers how to load `conversations.json` from your `ChatGPT` data export folder.

You can get your data export by email by going to: https://chat.openai.com/ -> (Profile) - Settings -> Export data -> Confirm export.


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


