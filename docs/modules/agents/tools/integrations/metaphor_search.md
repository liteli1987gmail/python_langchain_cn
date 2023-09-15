# Metaphor Search

This notebook goes over how to use Metaphor search.

First, you need to set up the proper API keys and environment variables. Request an API key [here](Sign up for early access here).

Then enter your API key as an environment variable.


```python
import os

os.environ["METAPHOR_API_KEY"] = ""
```


```python
from langchain.utilities import MetaphorSearchAPIWrapper
```


```python
search = MetaphorSearchAPIWrapper()
```

# Call the API
`results` takes in a Metaphor-optimized search query and a number of results (up to 500). It returns a list of results with title, url, author, and creation date.


```python
search.results("The best blog post about AI safety is definitely this: ", 10)
```

# Adding filters
We can also add filters to our search. 
include_domains: Optional[List[str]] - List of domains to include in the search. If specified, results will only come from these domains. Only one of include_domains and exclude_domains should be specified.
exclude_domains: Optional[List[str]] - List of domains to exclude in the search. If specified, results will only come from these domains. Only one of include_domains and exclude_domains should be specified.
start_crawl_date: Optional[str] - "Crawl date" refers to the date that Metaphor discovered a link, which is more granular and can be more useful than published date. If start_crawl_date is specified, results will only include links that were crawled after start_crawl_date. Must be specified in ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)
end_crawl_date: Optional[str] - "Crawl date" refers to the date that Metaphor discovered a link, which is more granular and can be more useful than published date. If endCrawlDate is specified, results will only include links that were crawled before end_crawl_date. Must be specified in ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)
start_published_date: Optional[str] - If specified, only links with a published date after start_published_date will be returned. Must be specified in ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ). Note that for some links, we have no published date, and these links will be excluded from the results if start_published_date is specified.
end_published_date: Optional[str] - If specified, only links with a published date before end_published_date will be returned. Must be specified in ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ). Note that for some links, we have no published date, and these links will be excluded from the results if end_published_date is specified.

See full docs [here](https://metaphorapi.readme.io/)


```python
search.results("The best blog post about AI safety is definitely this: ", 10, include_domains=["lesswrong.com"], start_published_date="2019-01-01")
```

# Use Metaphor as a tool
Metaphor can be used as a tool that gets URLs that other tools such as browsing tools.


```python
%pip install playwright
from langchain.agents.agent_toolkits import PlayWrightBrowserToolkit
from langchain.tools.playwright.utils import (
    create_async_playwright_browser,  # A synchronous browser is available, though it isn't compatible with jupyter.
)

async_browser = create_async_playwright_browser()
toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=async_browser)
tools = toolkit.get_tools()

tools_by_name = {tool.name: tool for tool in tools}
print(tools_by_name.keys())
navigate_tool = tools_by_name["navigate_browser"]
extract_text = tools_by_name["extract_text"]
```


```python
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.tools import MetaphorSearchResults

llm = ChatOpenAI(model_name="gpt-4", temperature=0.7)

metaphor_tool = MetaphorSearchResults(api_wrapper=search)

agent_chain = initialize_agent(
    [metaphor_tool, extract_text, navigate_tool],
    llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)

agent_chain.run(
    "find me an interesting tweet about AI safety using Metaphor, then tell me the first sentence in the post. Do not finish until able to retrieve the first sentence."
)
```


```python

```
