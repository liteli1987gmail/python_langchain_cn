# Gmail Toolkit

This notebook walks through connecting a LangChain email to the Gmail API.

To use this toolkit, you will need to set up your credentials explained in the [Gmail API docs](https://developers.google.com/gmail/api/quickstart/python#authorize_credentials_for_a_desktop_application). Once you've downloaded the `credentials.json` file, you can start using the Gmail API. Once this is done, we'll install the required libraries.


```python
!pip install --upgrade google-api-python-client > /dev/null
!pip install --upgrade google-auth-oauthlib > /dev/null
!pip install --upgrade google-auth-httplib2 > /dev/null
!pip install beautifulsoup4 > /dev/null # This is optional but is useful for parsing HTML messages
```

## Create the Toolkit

By default the toolkit reads the local `credentials.json` file. You can also manually provide a `Credentials` object.


```python
from langchain.agents.agent_toolkits import GmailToolkit

toolkit = GmailToolkit()
```

## Customizing Authentication

Behind the scenes, a `googleapi` resource is created using the following methods. 
you can manually build a `googleapi` resource for more auth control. 


```python
from langchain.tools.gmail.utils import build_resource_service, get_gmail_credentials

# Can review scopes here https://developers.google.com/gmail/api/auth/scopes
# For instance, readonly scope is 'https://www.googleapis.com/auth/gmail.readonly'
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



## Use within an Agent


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
