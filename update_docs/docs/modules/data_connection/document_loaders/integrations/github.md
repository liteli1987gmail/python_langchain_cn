# GitHub

This notebooks shows how you can load issues and pull requests (PRs) for a given repository on [GitHub](https://github.com/). We will use the LangChain Python repository as an example.

## Setup access token

To access the GitHub API, you need a personal access token - you can set up yours here: https://github.com/settings/tokens?type=beta. You can either set this token as the environment variable ``GITHUB_PERSONAL_ACCESS_TOKEN`` and it will be automatically pulled in, or you can pass it in directly at initializaiton as the ``access_token`` named parameter.


```python
# If you haven't set your access token as an environment variable, pass it in here.
from getpass import getpass

ACCESS_TOKEN = getpass()
```

## Load Issues and PRs


```python
from langchain.document_loaders import GitHubIssuesLoader
```


```python
loader = GitHubIssuesLoader(
    repo="hwchase17/langchain",
    access_token=ACCESS_TOKEN,  # delete/comment out this argument if you've set the access token as an env var.
    creator="UmerHA",
)
```

Let's load all issues and PRs created by "UmerHA".

Here's a list of all filters you can use:
- include_prs
- milestone
- state
- assignee
- creator
- mentioned
- labels
- sort
- direction
- since

For more info, see https://docs.github.com/en/rest/issues/issues?apiVersion=2022-11-28#list-repository-issues.


```python
docs = loader.load()
```


```python
print(docs[0].page_content)
print(docs[0].metadata)
```

    # Creates GitHubLoader (#5257)
    
    GitHubLoader is a DocumentLoader that loads issues and PRs from GitHub.
    
    Fixes #5257
    
    Community members can review the PR once tests pass. Tag maintainers/contributors who might be interested:
    DataLoaders
    - @eyurtsev
    
    {'url': 'https://github.com/hwchase17/langchain/pull/5408', 'title': 'DocumentLoader for GitHub', 'creator': 'UmerHA', 'created_at': '2023-05-29T14:50:53Z', 'comments': 0, 'state': 'open', 'labels': ['enhancement', 'lgtm', 'doc loader'], 'assignee': None, 'milestone': None, 'locked': False, 'number': 5408, 'is_pull_request': True}
    

## Only load issues

By default, the GitHub API returns considers pull requests to also be issues. To only get 'pure' issues (i.e., no pull requests), use `include_prs=False`


```python
loader = GitHubIssuesLoader(
    repo="hwchase17/langchain",
    access_token=ACCESS_TOKEN,  # delete/comment out this argument if you've set the access token as an env var.
    creator="UmerHA",
    include_prs=False,
)
docs = loader.load()
```


```python
print(docs[0].page_content)
print(docs[0].metadata)
```

    ### System Info
    
    LangChain version = 0.0.167
    Python version = 3.11.0
    System = Windows 11 (using Jupyter)
    
    ### Who can help?
    
    - @hwchase17
    - @agola11
    - @UmerHA (I have a fix ready, will submit a PR)
    
    ### Information
    
    - [ ] The official example notebooks/scripts
    - [X] My own modified scripts
    
    ### Related Components
    
    - [X] LLMs/Chat Models
    - [ ] Embedding Models
    - [X] Prompts / Prompt Templates / Prompt Selectors
    - [ ] Output Parsers
    - [ ] Document Loaders
    - [ ] Vector Stores / Retrievers
    - [ ] Memory
    - [ ] Agents / Agent Executors
    - [ ] Tools / Toolkits
    - [ ] Chains
    - [ ] Callbacks/Tracing
    - [ ] Async
    
    ### Reproduction
    
    ```
    import os
    os.environ["OPENAI_API_KEY"] = "..."
    
    from langchain.chains import LLMChain
    from langchain.chat_models import ChatOpenAI
    from langchain.prompts import PromptTemplate
    from langchain.prompts.chat import ChatPromptTemplate
    from langchain.schema import messages_from_dict
    
    role_strings = [
        ("system", "you are a bird expert"), 
        ("human", "which bird has a point beak?")
    ]
    prompt = ChatPromptTemplate.from_role_strings(role_strings)
    chain = LLMChain(llm=ChatOpenAI(), prompt=prompt)
    chain.run({})
    ```
    
    ### Expected behavior
    
    Chain should run
    {'url': 'https://github.com/hwchase17/langchain/issues/5027', 'title': "ChatOpenAI models don't work with prompts created via ChatPromptTemplate.from_role_strings", 'creator': 'UmerHA', 'created_at': '2023-05-20T10:39:18Z', 'comments': 1, 'state': 'open', 'labels': [], 'assignee': None, 'milestone': None, 'locked': False, 'number': 5027, 'is_pull_request': False}
    


```python

```
