# Gmail Toolkit

这个笔记本介绍了如何连接LangChain电子邮件到Gmail API。

要使用这个工具包，您需要设置您在[Gmail API文档](https://developers.google.com/gmail/api/quickstart/python#authorize_credentials_for_a_desktop_application)中解释的凭据。一旦您下载了`credentials.json`文件，您就可以开始使用Gmail API。完成这个步骤后，我们将安装所需的库。

```python
!pip install --upgrade google-api-python-client > /dev/null
!pip install --upgrade google-auth-oauthlib > /dev/null
!pip install --upgrade google-auth-httplib2 > /dev/null
!pip install beautifulsoup4 > /dev/null # 这是可选项，但对于解析HTML消息很有用
```

## 创建工具包

默认情况下，工具包会读取本地的`credentials.json`文件。您也可以手动提供一个`Credentials`对象。

```python
from langchain.agents.agent_toolkits import GmailToolkit

toolkit = GmailToolkit()
```

## 自定义身份验证

在背后，使用以下方法创建了一个`googleapi`资源。您可以手动构建一个`googleapi`资源以获得更多的身份验证控制。

```python
from langchain.tools.gmail.utils import build_resource_service, get_gmail_credentials

# 可以在这里查看范围 https://developers.google.com/gmail/api/auth/scopes
# 例如，只读范围是 'https://www.googleapis.com/auth/gmail.readonly'
credentials = get_gmail_credentials(
    token_file="token.json",
    scopes=["https://mail.google.com/"],
    client_secrets_file="credentials.json",
)
api_resource = build_resource_service(credentials=credentials)
toolkit = GmailToolkit(api_resource=api_resource)
```

```python
tools = toolkit.get_tools()
tools
```




    [GmailCreateDraft(name='create_gmail_draft', description='Use this tool to create a draft email with the provided message fields.', args_schema=<class 'langchain.tools.gmail.create_draft.CreateDraftSchema'>, return_direct=False, verbose=False, callbacks=None, callback_manager=None, api_resource=<googleapiclient.discovery.Resource object at 0x10e5c6d10>),
     GmailSendMessage(name='send_gmail_message', description='Use this tool to send email messages. The input is the message, recipents', args_schema=None, return_direct=False, verbose=False, callbacks=None, callback_manager=None, api_resource=<googleapiclient.discovery.Resource object at 0x10e5c6d10>),
     GmailSearch(name='search_gmail', description=('Use this tool to search for email messages or threads. The input must be a valid Gmail query. The output is a JSON list of the requested resource.',), args_schema=<class 'langchain.tools.gmail.search.SearchArgsSchema'>, return_direct=False, verbose=False, callbacks=None, callback_manager=None, api_resource=<googleapiclient.discovery.Resource object at 0x10e5c6d10>),
     GmailGetMessage(name='get_gmail_message', description='Use this tool to fetch an email by message ID. Returns the thread ID, snipet, body, subject, and sender.', args_schema=<class 'langchain.tools.gmail.get_message.SearchArgsSchema'>, return_direct=False, verbose=False, callbacks=None, callback_manager=None, api_resource=<googleapiclient.discovery.Resource object at 0x10e5c6d10>),
     GmailGetThread(name='get_gmail_thread', description=('Use this tool to search for email messages. The input must be a valid Gmail query. The output is a JSON list of messages.',), args_schema=<class 'langchain.tools.gmail.get_thread.GetThreadSchema'>, return_direct=False, verbose=False, callbacks=None, callback_manager=None, api_resource=<googleapiclient.discovery.Resource object at 0x10e5c6d10>)]



## 在Agent中使用

```python
from langchain import OpenAI
from langchain.agents import initialize_agent, AgentType
```

```python
llm = OpenAI(temperature=0)
agent = initialize_agent(
    tools=toolkit.get_tools(),
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
)
```

```python
agent.run(
    "Create a gmail draft for me to edit of a letter from the perspective of a sentient parrot"
    " who is looking to collaborate on some research with her"
    " estranged friend, a cat. Under no circumstances may you send the message, however."
)
```

    WARNING:root:Failed to load default session, using empty session: 0
    WARNING:root:Failed to persist run: {"detail":"Not Found"}
    

    'I have created a draft email for you to edit. The draft Id is r5681294731961864018.'


```python
agent.run("Could you search in my drafts for the latest email?")
```

    WARNING:root:Failed to load default session, using empty session: 0
    WARNING:root:Failed to persist run: {"detail":"Not Found"}
    

    "The latest email in your drafts is from hopefulparrot@gmail.com with the subject 'Collaboration Opportunity'. The body of the email reads: 'Dear [Friend], I hope this letter finds you well. I am writing to you in the hopes of rekindling our friendship and to discuss the possibility of collaborating on some research together. I know that we have had our differences in the past, but I believe that we can put them aside and work together for the greater good. I look forward to hearing from you. Sincerely, [Parrot]'"




```python

```
