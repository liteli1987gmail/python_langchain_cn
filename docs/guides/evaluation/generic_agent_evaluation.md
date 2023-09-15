# Generic Agent Evaluation

Good evaluation is key for quickly iterating on your agent's prompts and tools. Here we provide an example of how to use the TrajectoryEvalChain to evaluate your agent.

## Setup

Let's start by defining our agent.


```python
from langchain import Wikipedia
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.agents.react.base import DocstoreExplorer
from langchain.memory import ConversationBufferMemory
from langchain import LLMMathChain
from langchain.llms import OpenAI

from langchain import SerpAPIWrapper

docstore = DocstoreExplorer(Wikipedia())

math_llm = OpenAI(temperature=0)

llm_math_chain = LLMMathChain(llm=math_llm, verbose=True)

search = SerpAPIWrapper()

tools = [
    Tool(
        name="Search",
        func=docstore.search,
        description="useful for when you need to ask with search",
    ),
    Tool(
        name="Lookup",
        func=docstore.lookup,
        description="useful for when you need to ask with lookup",
    ),
    Tool(
        name="Calculator",
        func=llm_math_chain.run,
        description="useful for doing calculations",
    ),
    Tool(
        name="Search the Web (SerpAPI)",
        func=search.run,
        description="useful for when you need to answer questions about current events",
    ),
]

memory = ConversationBufferMemory(
    memory_key="chat_history", return_messages=True, output_key="output"
)

llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True,
    memory=memory,
    return_intermediate_steps=True,  # This is needed for the evaluation later
)
```

## Testing the Agent

Now let's try our agent out on some example queries.


```python
query_one = (
    "How many ping pong balls would it take to fill the entire Empire State Building?"
)

test_outputs_one = agent({"input": query_one}, return_only_outputs=False)
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3m{
        "action": "Search the Web (SerpAPI)",
        "action_input": "How many ping pong balls would it take to fill the entire Empire State Building?"
    }[0m
    Observation: [31;1m[1;3m12.8 billion. The volume of the Empire State Building Googles in at around 37 million ft³. A golf ball comes in at about 2.5 in³.[0m
    Thought:[32;1m[1;3m{
        "action": "Final Answer",
        "action_input": "It would take approximately 12.8 billion ping pong balls to fill the entire Empire State Building."
    }[0m
    
    [1m> Finished chain.[0m
    

This looks good! Let's try it out on another query.


```python
query_two = "If you laid the Eiffel Tower end to end, how many would you need cover the US from coast to coast?"

test_outputs_two = agent({"input": query_two}, return_only_outputs=False)
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3m{
        "action": "Calculator",
        "action_input": "The length of the Eiffel Tower is 324 meters. The distance from coast to coast in the US is approximately 4,828 kilometers. First, we need to convert 4,828 kilometers to meters, which gives us 4,828,000 meters. To find out how many Eiffel Towers we need, we can divide 4,828,000 by 324. This gives us approximately 14,876 Eiffel Towers."
    }[0m
    
    [1m> Entering new LLMMathChain chain...[0m
    The length of the Eiffel Tower is 324 meters. The distance from coast to coast in the US is approximately 4,828 kilometers. First, we need to convert 4,828 kilometers to meters, which gives us 4,828,000 meters. To find out how many Eiffel Towers we need, we can divide 4,828,000 by 324. This gives us approximately 14,876 Eiffel Towers.[32;1m[1;3m
    ```text
    4828000 / 324
    ```
    ...numexpr.evaluate("4828000 / 324")...
    [0m
    Answer: [33;1m[1;3m14901.234567901234[0m
    [1m> Finished chain.[0m
    
    Observation: [38;5;200m[1;3mAnswer: 14901.234567901234[0m
    Thought:[32;1m[1;3m{
        "action": "Calculator",
        "action_input": "The length of the Eiffel Tower is 324 meters. The distance from coast to coast in the US is approximately 4,828 kilometers. First, we need to convert 4,828 kilometers to meters, which gives us 4,828,000 meters. To find out how many Eiffel Towers we need, we can divide 4,828,000 by 324. This gives us approximately 14,901 Eiffel Towers."
    }[0m
    
    [1m> Entering new LLMMathChain chain...[0m
    The length of the Eiffel Tower is 324 meters. The distance from coast to coast in the US is approximately 4,828 kilometers. First, we need to convert 4,828 kilometers to meters, which gives us 4,828,000 meters. To find out how many Eiffel Towers we need, we can divide 4,828,000 by 324. This gives us approximately 14,901 Eiffel Towers.[32;1m[1;3m
    ```text
    4828000 / 324
    ```
    ...numexpr.evaluate("4828000 / 324")...
    [0m
    Answer: [33;1m[1;3m14901.234567901234[0m
    [1m> Finished chain.[0m
    
    Observation: [38;5;200m[1;3mAnswer: 14901.234567901234[0m
    Thought:[32;1m[1;3m{
        "action": "Final Answer",
        "action_input": "If you laid the Eiffel Tower end to end, you would need approximately 14,901 Eiffel Towers to cover the US from coast to coast."
    }[0m
    
    [1m> Finished chain.[0m
    

This doesn't look so good. Let's try running some evaluation.

## Evaluating the Agent

Let's start by defining the TrajectoryEvalChain.


```python
from langchain.evaluation.agents import TrajectoryEvalChain

# Define chain
eval_chain = TrajectoryEvalChain.from_llm(
    llm=ChatOpenAI(
        temperature=0, model_name="gpt-4"
    ),  # Note: This must be a ChatOpenAI model
    agent_tools=agent.tools,
    return_reasoning=True,
)
```

Let's try evaluating the first query.


```python
question, steps, answer = (
    test_outputs_one["input"],
    test_outputs_one["intermediate_steps"],
    test_outputs_one["output"],
)

evaluation = eval_chain(
    inputs={
        "question": question,
        "answer": answer,
        "agent_trajectory": eval_chain.get_agent_trajectory(steps),
    },
)

print("Score from 1 to 5: ", evaluation["score"])
print("Reasoning: ", evaluation["reasoning"])
```

    Score from 1 to 5:  1
    Reasoning:  First, let's evaluate the final answer. The final answer is incorrect because it uses the volume of golf balls instead of ping pong balls. The answer is not helpful.
    
    Second, does the model use a logical sequence of tools to answer the question? The model only used one tool, which was the Search the Web (SerpAPI). It did not use the Calculator tool to calculate the correct volume of ping pong balls.
    
    Third, does the AI language model use the tools in a helpful way? The model used the Search the Web (SerpAPI) tool, but the output was not helpful because it provided information about golf balls instead of ping pong balls.
    
    Fourth, does the AI language model use too many steps to answer the question? The model used only one step, which is not too many. However, it should have used more steps to provide a correct answer.
    
    Fifth, are the appropriate tools used to answer the question? The model should have used the Search tool to find the volume of the Empire State Building and the volume of a ping pong ball. Then, it should have used the Calculator tool to calculate the number of ping pong balls needed to fill the building.
    
    Judgment: Given the incorrect final answer and the inappropriate use of tools, we give the model a score of 1.
    

That seems about right. Let's try the second query.


```python
question, steps, answer = (
    test_outputs_two["input"],
    test_outputs_two["intermediate_steps"],
    test_outputs_two["output"],
)

evaluation = eval_chain(
    inputs={
        "question": question,
        "answer": answer,
        "agent_trajectory": eval_chain.get_agent_trajectory(steps),
    },
)

print("Score from 1 to 5: ", evaluation["score"])
print("Reasoning: ", evaluation["reasoning"])
```

    Score from 1 to 5:  3
    Reasoning:  i. Is the final answer helpful?
    Yes, the final answer is helpful as it provides an approximate number of Eiffel Towers needed to cover the US from coast to coast.
    
    ii. Does the AI language use a logical sequence of tools to answer the question?
    No, the AI language model does not use a logical sequence of tools. It directly uses the Calculator tool without first using the Search or Lookup tools to find the necessary information (length of the Eiffel Tower and distance from coast to coast in the US).
    
    iii. Does the AI language model use the tools in a helpful way?
    The AI language model uses the Calculator tool in a helpful way to perform the calculation, but it should have used the Search or Lookup tools first to find the required information.
    
    iv. Does the AI language model use too many steps to answer the question?
    No, the AI language model does not use too many steps. However, it repeats the same step twice, which is unnecessary.
    
    v. Are the appropriate tools used to answer the question?
    Not entirely. The AI language model should have used the Search or Lookup tools to find the required information before using the Calculator tool.
    
    Given the above evaluation, the AI language model's performance can be scored as follows:
    

That also sounds about right. In conclusion, the TrajectoryEvalChain allows us to use GPT-4 to score both our agent's outputs and tool use in addition to giving us the reasoning behind the evaluation.
