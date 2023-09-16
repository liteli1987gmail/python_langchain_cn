# Facebook Chat
[Messenger](https://en.wikipedia.org/wiki/Messenger_(software)) 是一款由 `Meta Platforms` 开发的美国专有即时消息应用程序和平台。该公司于2008年启动的 `Facebook Chat` 在2010年进行了改版。本笔记本介绍了如何将 [Facebook 聊天记录](https://www.facebook.com/business/help/1646890868956360) 加载到可被 LangChain 导入的格式中。
```python
# pip install pandas
```
```python
from langchain.document_loaders import FacebookChatLoader
```
```python
loader = FacebookChatLoader("example_data/facebook_chat.json")
```
```python
loader.load()
```


    [Document(page_content='User 2 on 2023-02-05 03:46:11: Bye!\n\nUser 1 on 2023-02-05 03:43:55: Oh no worries! Bye\n\nUser 2 on 2023-02-05 03:24:37: No Im sorry it was my mistake, the blue one is not for sale\n\nUser 1 on 2023-02-05 03:05:40: I thought you were selling the blue one!\n\nUser 1 on 2023-02-05 03:05:09: Im not interested in this bag. Im interested in the blue one!\n\nUser 2 on 2023-02-05 03:04:28: Here is $129\n\nUser 2 on 2023-02-05 03:04:05: Online is at least $100\n\nUser 1 on 2023-02-05 02:59:59: How much do you want?\n\nUser 2 on 2023-02-04 22:17:56: Goodmorning! $50 is too low.\n\nUser 1 on 2023-02-04 14:17:02: Hi! Im interested in your bag. Im offering $50. Let me know if you are interested. Thanks!\n\n', metadata={'source': 'example_data/facebook_chat.json'})]

