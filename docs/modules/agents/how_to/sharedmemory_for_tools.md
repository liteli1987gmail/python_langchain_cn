# 代理和工具之间的共享内存

这个笔记本介绍了如何给**代理**和**工具**都添加内存。在阅读本笔记本之前，请先阅读以下笔记本，因为本笔记本是基于它们之上的：

- [向 LLM 链添加内存](../../../memory/integrations/adding_memory.html)
- [自定义代理](../../agents/custom_agent.html)

我们将创建一个自定义代理。该代理具有访问对话内存、搜索工具和摘要工具的功能。而且，摘要工具还需要访问对话内存。

```python
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from langchain.memory import ConversationBufferMemory, ReadOnlySharedMemory
from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.utilities import GoogleSearchAPIWrapper
```

```python
# 省略部分代码
```

我们现在可以构建 LLMChain，并创建代理。

```python
llm_chain = LLMChain(llm=OpenAI(temperature=0), prompt=prompt)
agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=True)
agent_chain = AgentExecutor.from_agent_and_tools(
    agent=agent, tools=tools, verbose=True, memory=memory
)
```

```python
agent_chain.run(input="What is ChatGPT?")
```

```
> 进入新的 AgentExecutor 链...
Thought: 我应该研究 ChatGPT 来回答这个问题。
Action: Search
Action Input: "ChatGPT"
Observation: Nov 30, 2022 ... We've trained a model called ChatGPT which interacts in a conversational way. The dialogue format makes it possible for ChatGPT to answer ... ChatGPT is an artificial intelligence chatbot developed by OpenAI and launched in November 2022. It is built on top of OpenAI's GPT-3 family of large ... ChatGPT. We've trained a model called ChatGPT which interacts in a conversational way. The dialogue format makes it possible for ChatGPT to answer ... Feb 2, 2023 ... ChatGPT, the popular chatbot from OpenAI, is estimated to have reached 100 million monthly active users in January, just two months after ... 2 days ago ... ChatGPT recently launched a new version of its own plagiarism detection tool, with hopes that it will squelch some of the criticism around how ... An API for accessing new AI models developed by OpenAI. Feb 19, 2023 ... ChatGPT is an AI chatbot system that OpenAI released in November to show off and test what a very large, powerful AI system can accomplish. You ... ChatGPT is fine-tuned from GPT-3.5, a language model trained to produce text. ChatGPT was optimized for dialogue by using Reinforcement Learning with Human ... 3 days ago ... Visual ChatGPT connects ChatGPT and a series of Visual Foundation Models to enable sending and receiving images during chatting. Dec 1, 2022 ... ChatGPT is a natural language processing tool driven by AI technology that allows you to have human-like conversations and much more with a ..."
Thought:[32;1m I now know the final answer.
Final Answer: ChatGPT is an artificial intelligence chatbot developed by OpenAI and launched in November 2022. It is built on top of OpenAI's GPT-3 family of large language models and is optimized for dialogue by using Reinforcement Learning with Human-in-the-Loop. It is also capable of sending and receiving images during chatting.
Finished chain.

> Finished chain.


"ChatGPT is an artificial intelligence chatbot developed by OpenAI and launched in November 2022. It is built on top of OpenAI's GPT-3 family of large language models and is optimized for dialogue by using Reinforcement Learning with Human-in-the-Loop. It is also capable of sending and receiving images during chatting."

```python
# 省略部分代码
```

```python
agent_chain.run(input="Who developed it?")
```

```
> 进入新的 AgentExecutor 链...
Thought: 我需要找出谁开发了 ChatGPT
Action: Search
Action Input: Who developed ChatGPT
Observation: ChatGPT is an artificial intelligence chatbot developed by OpenAI and launched in November 2022. It is built on top of OpenAI's GPT-3 family of large ... Feb 15, 2023 ... Who owns Chat GPT? Chat GPT is owned and developed by AI research and deployment company, OpenAI. The organization is headquartered in San ... Feb 8, 2023 ... ChatGPT is an AI chatbot developed by San Francisco-based startup OpenAI. OpenAI was co-founded in 2015 by Elon Musk and Sam Altman and is ... Dec 7, 2022 ... ChatGPT is an AI chatbot designed and developed by OpenAI. The bot works by generating text responses based on human-user input, like questions ... Jan 12, 2023 ... In 2019, Microsoft invested $1 billion in OpenAI, the tiny San Francisco company that designed ChatGPT. And in the years since, it has quietly ... Jan 25, 2023 ... The inside story of ChatGPT: How OpenAI founder Sam Altman built the world's hottest technology with billions from Microsoft. Dec 3, 2022 ... ChatGPT went viral on social media for its ability to do anything from code to write essays. · The company that created the AI chatbot has a ... Jan 17, 2023 ... While many Americans were nursing hangovers on New Year's Day, 22-year-old Edward Tian was working feverishly on a new app to combat misuse ... ChatGPT is a language model created by OpenAI, an artificial intelligence research laboratory consisting of a team of researchers and engineers focused on ... 1 day ago ... Everyone is talking about ChatGPT, developed by OpenAI. This is such a great tool that has helped to make AI more accessible to a wider ..."
Thought:[32;1m I now know the final answer
Final Answer: ChatGPT was developed by OpenAI.
Finished chain.

> Finished chain.


"ChatGPT was developed by OpenAI."

```python
# 省略部分代码
```

```python
agent_chain.run(
    input="Thanks. Summarize the conversation, for my daughter 5 years old."
)
```

```
> 进入新的 AgentExecutor 链...
Thought: 我需要为一个 5 岁的孩子简化对话
Action: Summary
Action Input: My daughter 5 years old

> 进入新的 LLMChain 链...
Prompt after formatting:
This is a conversation between a human and a bot:

Human: What is ChatGPT?
AI: ChatGPT is an artificial intelligence chatbot developed by OpenAI and launched in November 2022. It is built on top of OpenAI's GPT-3 family of large language models and is optimized for dialogue by using Reinforcement Learning with Human-in-the-Loop. It is also capable of sending and receiving images during chatting.
Human: Who developed it?
AI: ChatGPT was developed by OpenAI.

Write a summary of the conversation for My daughter 5 years old:

> Finished chain.

Observation: The conversation was about ChatGPT, an artificial intelligence chatbot developed by OpenAI. It is designed to have conversations with humans and can also send and receive images.
Thought: I now know the final answer.
Final Answer: ChatGPT is an artificial intelligence chatbot developed by OpenAI that can have conversations with humans and send and receive images.
Finished chain.

"ChatGPT is an artificial intelligence chatbot developed by OpenAI that can have conversations with humans and send and receive images."

```python
# 省略部分代码
```

```python
print(agent_chain.memory.buffer)
```

```
Human: What is ChatGPT?
AI: ChatGPT is an artificial intelligence chatbot developed by OpenAI and launched in November 2022. It is built on top of OpenAI's GPT-3 family of large language models and is optimized for dialogue by using Reinforcement Learning with Human-in-the-Loop. It is also capable of sending and receiving images during chatting.
Human: Who developed it?
AI: ChatGPT was developed by OpenAI.
Human: My daughter 5 years old
AI: The conversation was about ChatGPT, an artificial intelligence chatbot developed by OpenAI. It is designed to have conversations with humans and can also send and receive images.
Human: Thanks. Summarize the conversation, for my daughter 5 years old.
AI: ChatGPT is an artificial intelligence chatbot developed by OpenAI that can have conversations with humans and send and receive images.

```