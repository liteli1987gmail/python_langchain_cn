# 2Markdown

>[2markdown](https://2markdown.com/) service transforms website content into structured markdown files.



```python
# You will need to get your own API key. See https://2markdown.com/login

api_key = ""
```


```python
from langchain.document_loaders import ToMarkdownLoader
```


```python
loader = ToMarkdownLoader.from_api_key(
    url="https://python.langchain.com/en/latest/", api_key=api_key
)
```


```python
docs = loader.load()
```


```python
print(docs[0].page_content)
```

    ## Contents
    
    - [Getting Started](#getting-started)
    - [Modules](#modules)
    - [Use Cases](#use-cases)
    - [Reference Docs](#reference-docs)
    - [LangChain Ecosystem](#langchain-ecosystem)
    - [Additional Resources](#additional-resources)
    
    ## Welcome to LangChain [\#](\#welcome-to-langchain "Permalink to this headline")
    
    **LangChain** is a framework for developing applications powered by language models. We believe that the most powerful and differentiated applications will not only call out to a language model, but will also be:
    
    1. _Data-aware_: connect a language model to other sources of data
    
    2. _Agentic_: allow a language model to interact with its environment
    
    
    The LangChain framework is designed around these principles.
    
    This is the Python specific portion of the documentation. For a purely conceptual guide to LangChain, see [here](https://docs.langchain.com/docs/). For the JavaScript documentation, see [here](https://js.langchain.com.cn).
    
    ## Getting Started [\#](\#getting-started "Permalink to this headline")
    
    How to get started using LangChain to create an Language Model application.
    
    - [Quickstart Guide](https://python.langchain.com/en/latest/getting_started/getting_started.html)
    
    
    Concepts and terminology.
    
    - [Concepts and terminology](https://python.langchain.com/en/latest/getting_started/concepts.html)
    
    
    Tutorials created by community experts and presented on YouTube.
    
    - [Tutorials](https://python.langchain.com/en/latest/getting_started/tutorials.html)
    
    
    ## Modules [\#](\#modules "Permalink to this headline")
    
    These modules are the core abstractions which we view as the building blocks of any LLM-powered application.
    
    For each module LangChain provides standard, extendable interfaces. LanghChain also provides external integrations and even end-to-end implementations for off-the-shelf use.
    
    The docs for each module contain quickstart examples, how-to guides, reference docs, and conceptual guides.
    
    The modules are (from least to most complex):
    
    - [Models](https://python.langchain.com/en/latest/modules/models.html): Supported model types and integrations.
    
    - [Prompts](https://python.langchain.com/en/latest/modules/prompts.html): Prompt management, optimization, and serialization.
    
    - [Memory](https://python.langchain.com/en/latest/modules/memory.html): Memory refers to state that is persisted between calls of a chain/agent.
    
    - [Indexes](https://python.langchain.com/en/latest/modules/data_connection.html): Language models become much more powerful when combined with application-specific data - this module contains interfaces and integrations for loading, querying and updating external data.
    
    - [Chains](https://python.langchain.com/en/latest/modules/chains.html): Chains are structured sequences of calls (to an LLM or to a different utility).
    
    - [Agents](https://python.langchain.com/en/latest/modules/agents.html): An agent is a Chain in which an LLM, given a high-level directive and a set of tools, repeatedly decides an action, executes the action and observes the outcome until the high-level directive is complete.
    
    - [Callbacks](https://python.langchain.com/en/latest/modules/callbacks/getting_started.html): Callbacks let you log and stream the intermediate steps of any chain, making it easy to observe, debug, and evaluate the internals of an application.
    
    
    ## Use Cases [\#](\#use-cases "Permalink to this headline")
    
    Best practices and built-in implementations for common LangChain use cases:
    
    - [Autonomous Agents](https://python.langchain.com/en/latest/use_cases/autonomous_agents.html): Autonomous agents are long-running agents that take many steps in an attempt to accomplish an objective. Examples include AutoGPT and BabyAGI.
    
    - [Agent Simulations](https://python.langchain.com/en/latest/use_cases/agent_simulations.html): Putting agents in a sandbox and observing how they interact with each other and react to events can be an effective way to evaluate their long-range reasoning and planning abilities.
    
    - [Personal Assistants](https://python.langchain.com/en/latest/use_cases/personal_assistants.html): One of the primary LangChain use cases. Personal assistants need to take actions, remember interactions, and have knowledge about your data.
    
    - [Question Answering](https://python.langchain.com/en/latest/use_cases/question_answering.html): Another common LangChain use case. Answering questions over specific documents, only utilizing the information in those documents to construct an answer.
    
    - [Chatbots](https://python.langchain.com/en/latest/use_cases/chatbots.html): Language models love to chat, making this a very natural use of them.
    
    - [Querying Tabular Data](https://python.langchain.com/en/latest/use_cases/tabular.html): Recommended reading if you want to use language models to query structured data (CSVs, SQL, dataframes, etc).
    
    - [Code Understanding](https://python.langchain.com/en/latest/use_cases/code.html): Recommended reading if you want to use language models to analyze code.
    
    - [Interacting with APIs](https://python.langchain.com/en/latest/use_cases/apis.html): Enabling language models to interact with APIs is extremely powerful. It gives them access to up-to-date information and allows them to take actions.
    
    - [Extraction](https://python.langchain.com/en/latest/use_cases/extraction.html): Extract structured information from text.
    
    - [Summarization](https://python.langchain.com/en/latest/use_cases/summarization.html): Compressing longer documents. A type of Data-Augmented Generation.
    
    - [Evaluation](https://python.langchain.com/en/latest/use_cases/evaluation.html): Generative models are hard to evaluate with traditional metrics. One promising approach is to use language models themselves to do the evaluation.
    
    
    ## Reference Docs [\#](\#reference-docs "Permalink to this headline")
    
    Full documentation on all methods, classes, installation methods, and integration setups for LangChain.
    
    - [Reference Documentation](https://python.langchain.com/en/latest/reference.html)
    
    
    ## LangChain Ecosystem [\#](\#langchain-ecosystem "Permalink to this headline")
    
    Guides for how other companies/products can be used with LangChain.
    
    - [LangChain Ecosystem](https://python.langchain.com/en/latest/ecosystem.html)
    
    
    ## Additional Resources [\#](\#additional-resources "Permalink to this headline")
    
    Additional resources we think may be useful as you develop your application!
    
    - [LangChainHub](https://github.com/hwchase17/langchain-hub): The LangChainHub is a place to share and explore other prompts, chains, and agents.
    
    - [Gallery](https://python.langchain.com/en/latest/additional_resources/gallery.html): A collection of our favorite projects that use LangChain. Useful for finding inspiration or seeing how things were done in other applications.
    
    - [Deployments](https://python.langchain.com/en/latest/additional_resources/deployments.html): A collection of instructions, code snippets, and template repositories for deploying LangChain apps.
    
    - [Tracing](https://python.langchain.com/en/latest/additional_resources/tracing.html): A guide on using tracing in LangChain to visualize the execution of chains and agents.
    
    - [Model Laboratory](https://python.langchain.com/en/latest/additional_resources/model_laboratory.html): Experimenting with different prompts, models, and chains is a big part of developing the best possible application. The ModelLaboratory makes it easy to do so.
    
    - [Discord](https://discord.gg/6adMQxSpJS): Join us on our Discord to discuss all things LangChain!
    
    - [YouTube](https://python.langchain.com/en/latest/additional_resources/youtube.html): A collection of the LangChain tutorials and videos.
    
    - [Production Support](https://forms.gle/57d8AmXBYp8PP8tZA): As you move your LangChains into production, we’d love to offer more comprehensive support. Please fill out this form and we’ll set up a dedicated support Slack channel.
    


```python

```
