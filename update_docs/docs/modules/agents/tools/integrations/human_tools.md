# Human as a tool

Human are AGI so they can certainly be used as a tool to help out AI agent 
when it is confused.


```python
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.agents import load_tools, initialize_agent
from langchain.agents import AgentType

llm = ChatOpenAI(temperature=0.0)
math_llm = OpenAI(temperature=0.0)
tools = load_tools(
    ["human", "llm-math"],
    llm=math_llm,
)

agent_chain = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)
```

In the above code you can see the tool takes input directly from command line.
You can customize `prompt_func` and `input_func` according to your need (as shown below).


```python
agent_chain.run("What's my friend Eric's surname?")
# Answer with 'Zhu'
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3mI don't know Eric's surname, so I should ask a human for guidance.
    Action: Human
    Action Input: "What is Eric's surname?"[0m
    
    What is Eric's surname?
     Zhu
    
    Observation: [36;1m[1;3mZhu[0m
    Thought:[32;1m[1;3mI now know Eric's surname is Zhu.
    Final Answer: Eric's surname is Zhu.[0m
    
    [1m> Finished chain.[0m
    




    "Eric's surname is Zhu."



## Configuring the Input Function

By default, the `HumanInputRun` tool uses the python `input` function to get input from the user.
You can customize the input_func to be anything you'd like.
For instance, if you want to accept multi-line input, you could do the following:


```python
def get_input() -> str:
    print("Insert your text. Enter 'q' or press Ctrl-D (or Ctrl-Z on Windows) to end.")
    contents = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line == "q":
            break
        contents.append(line)
    return "\n".join(contents)


# You can modify the tool when loading
tools = load_tools(["human", "ddg-search"], llm=math_llm, input_func=get_input)
```


```python
# Or you can directly instantiate the tool
from langchain.tools import HumanInputRun

tool = HumanInputRun(input_func=get_input)
```


```python
agent_chain = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)
```


```python
agent_chain.run("I need help attributing a quote")
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3mI should ask a human for guidance
    Action: Human
    Action Input: "Can you help me attribute a quote?"[0m
    
    Can you help me attribute a quote?
    Insert your text. Enter 'q' or press Ctrl-D (or Ctrl-Z on Windows) to end.
     vini
     vidi
     vici
     q
    
    Observation: [36;1m[1;3mvini
    vidi
    vici[0m
    Thought:[32;1m[1;3mI need to provide more context about the quote
    Action: Human
    Action Input: "The quote is 'Veni, vidi, vici'"[0m
    
    The quote is 'Veni, vidi, vici'
    Insert your text. Enter 'q' or press Ctrl-D (or Ctrl-Z on Windows) to end.
     oh who said it 
     q
    
    Observation: [36;1m[1;3moh who said it [0m
    Thought:[32;1m[1;3mI can use DuckDuckGo Search to find out who said the quote
    Action: DuckDuckGo Search
    Action Input: "Who said 'Veni, vidi, vici'?"[0m
    Observation: [33;1m[1;3mUpdated on September 06, 2019. "Veni, vidi, vici" is a famous phrase said to have been spoken by the Roman Emperor Julius Caesar (100-44 BCE) in a bit of stylish bragging that impressed many of the writers of his day and beyond. The phrase means roughly "I came, I saw, I conquered" and it could be pronounced approximately Vehnee, Veedee ... Veni, vidi, vici (Classical Latin: [weːniː wiːdiː wiːkiː], Ecclesiastical Latin: [ˈveni ˈvidi ˈvitʃi]; "I came; I saw; I conquered") is a Latin phrase used to refer to a swift, conclusive victory.The phrase is popularly attributed to Julius Caesar who, according to Appian, used the phrase in a letter to the Roman Senate around 47 BC after he had achieved a quick victory in his short ... veni, vidi, vici Latin quotation from Julius Caesar ve· ni, vi· di, vi· ci ˌwā-nē ˌwē-dē ˈwē-kē ˌvā-nē ˌvē-dē ˈvē-chē : I came, I saw, I conquered Articles Related to veni, vidi, vici 'In Vino Veritas' and Other Latin... Dictionary Entries Near veni, vidi, vici Venite veni, vidi, vici Venizélos See More Nearby Entries Cite this Entry Style The simplest explanation for why veni, vidi, vici is a popular saying is that it comes from Julius Caesar, one of history's most famous figures, and has a simple, strong meaning: I'm powerful and fast. But it's not just the meaning that makes the phrase so powerful. Caesar was a gifted writer, and the phrase makes use of Latin grammar to ... One of the best known and most frequently quoted Latin expression, veni, vidi, vici may be found hundreds of times throughout the centuries used as an expression of triumph. The words are said to have been used by Caesar as he was enjoying a triumph.[0m
    Thought:[32;1m[1;3mI now know the final answer
    Final Answer: Julius Caesar said the quote "Veni, vidi, vici" which means "I came, I saw, I conquered".[0m
    
    [1m> Finished chain.[0m
    




    'Julius Caesar said the quote "Veni, vidi, vici" which means "I came, I saw, I conquered".'




```python

```
