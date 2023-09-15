# Shared memory across agents and tools

This notebook goes over adding memory to **both** of an Agent and its tools. Before going through this notebook, please walk through the following notebooks, as this will build on top of both of them:

- [Adding memory to an LLM Chain](../../../memory/integrations/adding_memory.html)
- [Custom Agents](../../agents/custom_agent.html)

We are going to create a custom Agent. The agent has access to a conversation memory, search tool, and a summarization tool. And, the summarization tool also needs access to the conversation memory.


```python
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from langchain.memory import ConversationBufferMemory, ReadOnlySharedMemory
from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.utilities import GoogleSearchAPIWrapper
```


```python
template = """This is a conversation between a human and a bot:

{chat_history}

Write a summary of the conversation for {input}:
"""

prompt = PromptTemplate(input_variables=["input", "chat_history"], template=template)
memory = ConversationBufferMemory(memory_key="chat_history")
readonlymemory = ReadOnlySharedMemory(memory=memory)
summry_chain = LLMChain(
    llm=OpenAI(),
    prompt=prompt,
    verbose=True,
    memory=readonlymemory,  # use the read-only memory to prevent the tool from modifying the memory
)
```


```python
search = GoogleSearchAPIWrapper()
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="useful for when you need to answer questions about current events",
    ),
    Tool(
        name="Summary",
        func=summry_chain.run,
        description="useful for when you summarize a conversation. The input to this tool should be a string, representing who will read this summary.",
    ),
]
```


```python
prefix = """Have a conversation with a human, answering the following questions as best you can. You have access to the following tools:"""
suffix = """Begin!"

{chat_history}
Question: {input}
{agent_scratchpad}"""

prompt = ZeroShotAgent.create_prompt(
    tools,
    prefix=prefix,
    suffix=suffix,
    input_variables=["input", "chat_history", "agent_scratchpad"],
)
```

We can now construct the LLMChain, with the Memory object, and then create the agent.


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

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3mThought: I should research ChatGPT to answer this question.
    Action: Search
    Action Input: "ChatGPT"[0m
    Observation: [36;1m[1;3mNov 30, 2022 ... We've trained a model called ChatGPT which interacts in a conversational way. The dialogue format makes it possible for ChatGPT to answer ... ChatGPT is an artificial intelligence chatbot developed by OpenAI and launched in November 2022. It is built on top of OpenAI's GPT-3 family of large ... ChatGPT. We've trained a model called ChatGPT which interacts in a conversational way. The dialogue format makes it possible for ChatGPT to answer ... Feb 2, 2023 ... ChatGPT, the popular chatbot from OpenAI, is estimated to have reached 100 million monthly active users in January, just two months after ... 2 days ago ... ChatGPT recently launched a new version of its own plagiarism detection tool, with hopes that it will squelch some of the criticism around how ... An API for accessing new AI models developed by OpenAI. Feb 19, 2023 ... ChatGPT is an AI chatbot system that OpenAI released in November to show off and test what a very large, powerful AI system can accomplish. You ... ChatGPT is fine-tuned from GPT-3.5, a language model trained to produce text. ChatGPT was optimized for dialogue by using Reinforcement Learning with Human ... 3 days ago ... Visual ChatGPT connects ChatGPT and a series of Visual Foundation Models to enable sending and receiving images during chatting. Dec 1, 2022 ... ChatGPT is a natural language processing tool driven by AI technology that allows you to have human-like conversations and much more with a ...[0m
    Thought:[32;1m[1;3m I now know the final answer.
    Final Answer: ChatGPT is an artificial intelligence chatbot developed by OpenAI and launched in November 2022. It is built on top of OpenAI's GPT-3 family of large language models and is optimized for dialogue by using Reinforcement Learning with Human-in-the-Loop. It is also capable of sending and receiving images during chatting.[0m
    
    [1m> Finished chain.[0m
    




    "ChatGPT is an artificial intelligence chatbot developed by OpenAI and launched in November 2022. It is built on top of OpenAI's GPT-3 family of large language models and is optimized for dialogue by using Reinforcement Learning with Human-in-the-Loop. It is also capable of sending and receiving images during chatting."



To test the memory of this agent, we can ask a followup question that relies on information in the previous exchange to be answered correctly.


```python
agent_chain.run(input="Who developed it?")
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3mThought: I need to find out who developed ChatGPT
    Action: Search
    Action Input: Who developed ChatGPT[0m
    Observation: [36;1m[1;3mChatGPT is an artificial intelligence chatbot developed by OpenAI and launched in November 2022. It is built on top of OpenAI's GPT-3 family of large ... Feb 15, 2023 ... Who owns Chat GPT? Chat GPT is owned and developed by AI research and deployment company, OpenAI. The organization is headquartered in San ... Feb 8, 2023 ... ChatGPT is an AI chatbot developed by San Francisco-based startup OpenAI. OpenAI was co-founded in 2015 by Elon Musk and Sam Altman and is ... Dec 7, 2022 ... ChatGPT is an AI chatbot designed and developed by OpenAI. The bot works by generating text responses based on human-user input, like questions ... Jan 12, 2023 ... In 2019, Microsoft invested $1 billion in OpenAI, the tiny San Francisco company that designed ChatGPT. And in the years since, it has quietly ... Jan 25, 2023 ... The inside story of ChatGPT: How OpenAI founder Sam Altman built the world's hottest technology with billions from Microsoft. Dec 3, 2022 ... ChatGPT went viral on social media for its ability to do anything from code to write essays. · The company that created the AI chatbot has a ... Jan 17, 2023 ... While many Americans were nursing hangovers on New Year's Day, 22-year-old Edward Tian was working feverishly on a new app to combat misuse ... ChatGPT is a language model created by OpenAI, an artificial intelligence research laboratory consisting of a team of researchers and engineers focused on ... 1 day ago ... Everyone is talking about ChatGPT, developed by OpenAI. This is such a great tool that has helped to make AI more accessible to a wider ...[0m
    Thought:[32;1m[1;3m I now know the final answer
    Final Answer: ChatGPT was developed by OpenAI.[0m
    
    [1m> Finished chain.[0m
    




    'ChatGPT was developed by OpenAI.'




```python
agent_chain.run(
    input="Thanks. Summarize the conversation, for my daughter 5 years old."
)
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3mThought: I need to simplify the conversation for a 5 year old.
    Action: Summary
    Action Input: My daughter 5 years old[0m
    
    [1m> Entering new LLMChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mThis is a conversation between a human and a bot:
    
    Human: What is ChatGPT?
    AI: ChatGPT is an artificial intelligence chatbot developed by OpenAI and launched in November 2022. It is built on top of OpenAI's GPT-3 family of large language models and is optimized for dialogue by using Reinforcement Learning with Human-in-the-Loop. It is also capable of sending and receiving images during chatting.
    Human: Who developed it?
    AI: ChatGPT was developed by OpenAI.
    
    Write a summary of the conversation for My daughter 5 years old:
    [0m
    
    [1m> Finished chain.[0m
    
    Observation: [33;1m[1;3m
    The conversation was about ChatGPT, an artificial intelligence chatbot. It was created by OpenAI and can send and receive images while chatting.[0m
    Thought:[32;1m[1;3m I now know the final answer.
    Final Answer: ChatGPT is an artificial intelligence chatbot created by OpenAI that can send and receive images while chatting.[0m
    
    [1m> Finished chain.[0m
    




    'ChatGPT is an artificial intelligence chatbot created by OpenAI that can send and receive images while chatting.'



Confirm that the memory was correctly updated.


```python
print(agent_chain.memory.buffer)
```

    Human: What is ChatGPT?
    AI: ChatGPT is an artificial intelligence chatbot developed by OpenAI and launched in November 2022. It is built on top of OpenAI's GPT-3 family of large language models and is optimized for dialogue by using Reinforcement Learning with Human-in-the-Loop. It is also capable of sending and receiving images during chatting.
    Human: Who developed it?
    AI: ChatGPT was developed by OpenAI.
    Human: Thanks. Summarize the conversation, for my daughter 5 years old.
    AI: ChatGPT is an artificial intelligence chatbot created by OpenAI that can send and receive images while chatting.
    

For comparison, below is a bad example that uses the same memory for both the Agent and the tool.


```python
## This is a bad practice for using the memory.
## Use the ReadOnlySharedMemory class, as shown above.

template = """This is a conversation between a human and a bot:

{chat_history}

Write a summary of the conversation for {input}:
"""

prompt = PromptTemplate(input_variables=["input", "chat_history"], template=template)
memory = ConversationBufferMemory(memory_key="chat_history")
summry_chain = LLMChain(
    llm=OpenAI(),
    prompt=prompt,
    verbose=True,
    memory=memory,  # <--- this is the only change
)

search = GoogleSearchAPIWrapper()
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="useful for when you need to answer questions about current events",
    ),
    Tool(
        name="Summary",
        func=summry_chain.run,
        description="useful for when you summarize a conversation. The input to this tool should be a string, representing who will read this summary.",
    ),
]

prefix = """Have a conversation with a human, answering the following questions as best you can. You have access to the following tools:"""
suffix = """Begin!"

{chat_history}
Question: {input}
{agent_scratchpad}"""

prompt = ZeroShotAgent.create_prompt(
    tools,
    prefix=prefix,
    suffix=suffix,
    input_variables=["input", "chat_history", "agent_scratchpad"],
)

llm_chain = LLMChain(llm=OpenAI(temperature=0), prompt=prompt)
agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=True)
agent_chain = AgentExecutor.from_agent_and_tools(
    agent=agent, tools=tools, verbose=True, memory=memory
)
```


```python
agent_chain.run(input="What is ChatGPT?")
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3mThought: I should research ChatGPT to answer this question.
    Action: Search
    Action Input: "ChatGPT"[0m
    Observation: [36;1m[1;3mNov 30, 2022 ... We've trained a model called ChatGPT which interacts in a conversational way. The dialogue format makes it possible for ChatGPT to answer ... ChatGPT is an artificial intelligence chatbot developed by OpenAI and launched in November 2022. It is built on top of OpenAI's GPT-3 family of large ... ChatGPT. We've trained a model called ChatGPT which interacts in a conversational way. The dialogue format makes it possible for ChatGPT to answer ... Feb 2, 2023 ... ChatGPT, the popular chatbot from OpenAI, is estimated to have reached 100 million monthly active users in January, just two months after ... 2 days ago ... ChatGPT recently launched a new version of its own plagiarism detection tool, with hopes that it will squelch some of the criticism around how ... An API for accessing new AI models developed by OpenAI. Feb 19, 2023 ... ChatGPT is an AI chatbot system that OpenAI released in November to show off and test what a very large, powerful AI system can accomplish. You ... ChatGPT is fine-tuned from GPT-3.5, a language model trained to produce text. ChatGPT was optimized for dialogue by using Reinforcement Learning with Human ... 3 days ago ... Visual ChatGPT connects ChatGPT and a series of Visual Foundation Models to enable sending and receiving images during chatting. Dec 1, 2022 ... ChatGPT is a natural language processing tool driven by AI technology that allows you to have human-like conversations and much more with a ...[0m
    Thought:[32;1m[1;3m I now know the final answer.
    Final Answer: ChatGPT is an artificial intelligence chatbot developed by OpenAI and launched in November 2022. It is built on top of OpenAI's GPT-3 family of large language models and is optimized for dialogue by using Reinforcement Learning with Human-in-the-Loop. It is also capable of sending and receiving images during chatting.[0m
    
    [1m> Finished chain.[0m
    




    "ChatGPT is an artificial intelligence chatbot developed by OpenAI and launched in November 2022. It is built on top of OpenAI's GPT-3 family of large language models and is optimized for dialogue by using Reinforcement Learning with Human-in-the-Loop. It is also capable of sending and receiving images during chatting."




```python
agent_chain.run(input="Who developed it?")
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3mThought: I need to find out who developed ChatGPT
    Action: Search
    Action Input: Who developed ChatGPT[0m
    Observation: [36;1m[1;3mChatGPT is an artificial intelligence chatbot developed by OpenAI and launched in November 2022. It is built on top of OpenAI's GPT-3 family of large ... Feb 15, 2023 ... Who owns Chat GPT? Chat GPT is owned and developed by AI research and deployment company, OpenAI. The organization is headquartered in San ... Feb 8, 2023 ... ChatGPT is an AI chatbot developed by San Francisco-based startup OpenAI. OpenAI was co-founded in 2015 by Elon Musk and Sam Altman and is ... Dec 7, 2022 ... ChatGPT is an AI chatbot designed and developed by OpenAI. The bot works by generating text responses based on human-user input, like questions ... Jan 12, 2023 ... In 2019, Microsoft invested $1 billion in OpenAI, the tiny San Francisco company that designed ChatGPT. And in the years since, it has quietly ... Jan 25, 2023 ... The inside story of ChatGPT: How OpenAI founder Sam Altman built the world's hottest technology with billions from Microsoft. Dec 3, 2022 ... ChatGPT went viral on social media for its ability to do anything from code to write essays. · The company that created the AI chatbot has a ... Jan 17, 2023 ... While many Americans were nursing hangovers on New Year's Day, 22-year-old Edward Tian was working feverishly on a new app to combat misuse ... ChatGPT is a language model created by OpenAI, an artificial intelligence research laboratory consisting of a team of researchers and engineers focused on ... 1 day ago ... Everyone is talking about ChatGPT, developed by OpenAI. This is such a great tool that has helped to make AI more accessible to a wider ...[0m
    Thought:[32;1m[1;3m I now know the final answer
    Final Answer: ChatGPT was developed by OpenAI.[0m
    
    [1m> Finished chain.[0m
    




    'ChatGPT was developed by OpenAI.'




```python
agent_chain.run(
    input="Thanks. Summarize the conversation, for my daughter 5 years old."
)
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3mThought: I need to simplify the conversation for a 5 year old.
    Action: Summary
    Action Input: My daughter 5 years old[0m
    
    [1m> Entering new LLMChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mThis is a conversation between a human and a bot:
    
    Human: What is ChatGPT?
    AI: ChatGPT is an artificial intelligence chatbot developed by OpenAI and launched in November 2022. It is built on top of OpenAI's GPT-3 family of large language models and is optimized for dialogue by using Reinforcement Learning with Human-in-the-Loop. It is also capable of sending and receiving images during chatting.
    Human: Who developed it?
    AI: ChatGPT was developed by OpenAI.
    
    Write a summary of the conversation for My daughter 5 years old:
    [0m
    
    [1m> Finished chain.[0m
    
    Observation: [33;1m[1;3m
    The conversation was about ChatGPT, an artificial intelligence chatbot developed by OpenAI. It is designed to have conversations with humans and can also send and receive images.[0m
    Thought:[32;1m[1;3m I now know the final answer.
    Final Answer: ChatGPT is an artificial intelligence chatbot developed by OpenAI that can have conversations with humans and send and receive images.[0m
    
    [1m> Finished chain.[0m
    




    'ChatGPT is an artificial intelligence chatbot developed by OpenAI that can have conversations with humans and send and receive images.'



The final answer is not wrong, but we see the 3rd Human input is actually from the agent in the memory because the memory was modified by the summary tool.


```python
print(agent_chain.memory.buffer)
```

    Human: What is ChatGPT?
    AI: ChatGPT is an artificial intelligence chatbot developed by OpenAI and launched in November 2022. It is built on top of OpenAI's GPT-3 family of large language models and is optimized for dialogue by using Reinforcement Learning with Human-in-the-Loop. It is also capable of sending and receiving images during chatting.
    Human: Who developed it?
    AI: ChatGPT was developed by OpenAI.
    Human: My daughter 5 years old
    AI: 
    The conversation was about ChatGPT, an artificial intelligence chatbot developed by OpenAI. It is designed to have conversations with humans and can also send and receive images.
    Human: Thanks. Summarize the conversation, for my daughter 5 years old.
    AI: ChatGPT is an artificial intelligence chatbot developed by OpenAI that can have conversations with humans and send and receive images.
    
