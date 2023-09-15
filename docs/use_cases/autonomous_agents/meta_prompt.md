# Meta-Prompt

This is a LangChain implementation of [Meta-Prompt](https://noahgoodman.substack.com/p/meta-prompt-a-simple-self-improving), by [Noah Goodman](https://cocolab.stanford.edu/ndg), for building self-improving agents.

The key idea behind Meta-Prompt is to prompt the agent to reflect on its own performance and modify its own instructions.

![figure](https://substackcdn.com/image/fetch/f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F468217b9-96d9-47c0-a08b-dbf6b21b9f49_492x384.png)

Here is a description from the [original blog post](https://noahgoodman.substack.com/p/meta-prompt-a-simple-self-improving):


The agent is a simple loop that starts with no instructions and follows these steps:

Engage in conversation with a user, who may provide requests, instructions, or feedback.

At the end of the episode, generate self-criticism and a new instruction using the meta-prompt
```
Assistant has just had the below interactions with a User. Assistant followed their "system: Instructions" closely. Your job is to critique the Assistant's performance and then revise the Instructions so that Assistant would quickly and correctly respond in the future.
 
####
{hist}
####
 
Please reflect on these interactions.

You should first critique Assistant's performance. What could Assistant have done better? What should the Assistant remember about this user? Are there things this user always wants? Indicate this with "Critique: ...".

You should next revise the Instructions so that Assistant would quickly and correctly respond in the future. Assistant's goal is to satisfy the user in as few interactions as possible. Assistant will only see the new Instructions, not the interaction history, so anything important must be summarized in the Instructions. Don't forget any important details in the current Instructions! Indicate the new Instructions by "Instructions: ...".
```

Repeat.

The only fixed instructions for this system (which I call Meta-prompt) is the meta-prompt that governs revision of the agent’s instructions. The agent has no memory between episodes except for the instruction it modifies for itself each time. Despite its simplicity, this agent can learn over time and self-improve by incorporating useful details into its instructions.


## Setup
We define two chains. One serves as the `Assistant`, and the other is a "meta-chain" that critiques the `Assistant`'s performance and modifies the instructions to the `Assistant`.


```python
from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
```


```python
def initialize_chain(instructions, memory=None):
    if memory is None:
        memory = ConversationBufferWindowMemory()
        memory.ai_prefix = "Assistant"

    template = f"""
    Instructions: {instructions}
    {{{memory.memory_key}}}
    Human: {{human_input}}
    Assistant:"""

    prompt = PromptTemplate(
        input_variables=["history", "human_input"], template=template
    )

    chain = LLMChain(
        llm=OpenAI(temperature=0),
        prompt=prompt,
        verbose=True,
        memory=ConversationBufferWindowMemory(),
    )
    return chain


def initialize_meta_chain():
    meta_template = """
    Assistant has just had the below interactions with a User. Assistant followed their "Instructions" closely. Your job is to critique the Assistant's performance and then revise the Instructions so that Assistant would quickly and correctly respond in the future.

    ####

    {chat_history}

    ####

    Please reflect on these interactions.

    You should first critique Assistant's performance. What could Assistant have done better? What should the Assistant remember about this user? Are there things this user always wants? Indicate this with "Critique: ...".

    You should next revise the Instructions so that Assistant would quickly and correctly respond in the future. Assistant's goal is to satisfy the user in as few interactions as possible. Assistant will only see the new Instructions, not the interaction history, so anything important must be summarized in the Instructions. Don't forget any important details in the current Instructions! Indicate the new Instructions by "Instructions: ...".
    """

    meta_prompt = PromptTemplate(
        input_variables=["chat_history"], template=meta_template
    )

    meta_chain = LLMChain(
        llm=OpenAI(temperature=0),
        prompt=meta_prompt,
        verbose=True,
    )
    return meta_chain


def get_chat_history(chain_memory):
    memory_key = chain_memory.memory_key
    chat_history = chain_memory.load_memory_variables(memory_key)[memory_key]
    return chat_history


def get_new_instructions(meta_output):
    delimiter = "Instructions: "
    new_instructions = meta_output[meta_output.find(delimiter) + len(delimiter) :]
    return new_instructions
```


```python
def main(task, max_iters=3, max_meta_iters=5):
    failed_phrase = "task failed"
    success_phrase = "task succeeded"
    key_phrases = [success_phrase, failed_phrase]

    instructions = "None"
    for i in range(max_meta_iters):
        print(f"[Episode {i+1}/{max_meta_iters}]")
        chain = initialize_chain(instructions, memory=None)
        output = chain.predict(human_input=task)
        for j in range(max_iters):
            print(f"(Step {j+1}/{max_iters})")
            print(f"Assistant: {output}")
            print(f"Human: ")
            human_input = input()
            if any(phrase in human_input.lower() for phrase in key_phrases):
                break
            output = chain.predict(human_input=human_input)
        if success_phrase in human_input.lower():
            print(f"You succeeded! Thanks for playing!")
            return
        meta_chain = initialize_meta_chain()
        meta_output = meta_chain.predict(chat_history=get_chat_history(chain.memory))
        print(f"Feedback: {meta_output}")
        instructions = get_new_instructions(meta_output)
        print(f"New Instructions: {instructions}")
        print("\n" + "#" * 80 + "\n")
    print(f"You failed! Thanks for playing!")
```

## Specify a task and interact with the agent


```python
task = "Provide a systematic argument for why we should always eat pasta with olives."
main(task)
```

    [Episode 1/5]
    
    
    [1m> Entering new LLMChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3m
        Instructions: None
        
        Human: Provide a systematic argument for why we should always eat pasta with olives.
        Assistant:[0m
    
    [1m> Finished chain.[0m
    (Step 1/3)
    Assistant:  Eating pasta with olives is a great way to add flavor and texture to a dish. Olives are a great source of healthy fats, vitamins, and minerals, and they can help to balance out the carbohydrates in the pasta. Additionally, olives provide a unique flavor that can help to make the dish more interesting and enjoyable.
    Human: 
    You response is not in the form of a poem. Try again!
    
    
    [1m> Entering new LLMChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3m
        Instructions: None
        Human: Provide a systematic argument for why we should always eat pasta with olives.
    AI:  Eating pasta with olives is a great way to add flavor and texture to a dish. Olives are a great source of healthy fats, vitamins, and minerals, and they can help to balance out the carbohydrates in the pasta. Additionally, olives provide a unique flavor that can help to make the dish more interesting and enjoyable.
        Human: You response is not in the form of a poem. Try again!
        Assistant:[0m
    
    [1m> Finished chain.[0m
    (Step 2/3)
    Assistant:  Eating pasta with olives is a great way to add flavor and texture to a dish. Olives are a great source of healthy fats, vitamins, and minerals, which can help to balance out the carbohydrates in the pasta. Additionally, olives provide a unique flavor that can help to make the dish more interesting and enjoyable. For these reasons, it is recommended to always eat pasta with olives for a more balanced and flavorful meal.
    Human: 
    Your response is not piratey enough. Try again!
    
    
    [1m> Entering new LLMChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3m
        Instructions: None
        Human: Provide a systematic argument for why we should always eat pasta with olives.
    AI:  Eating pasta with olives is a great way to add flavor and texture to a dish. Olives are a great source of healthy fats, vitamins, and minerals, and they can help to balance out the carbohydrates in the pasta. Additionally, olives provide a unique flavor that can help to make the dish more interesting and enjoyable.
    Human: You response is not in the form of a poem. Try again!
    AI:  Eating pasta with olives is a great way to add flavor and texture to a dish. Olives are a great source of healthy fats, vitamins, and minerals, which can help to balance out the carbohydrates in the pasta. Additionally, olives provide a unique flavor that can help to make the dish more interesting and enjoyable. For these reasons, it is recommended to always eat pasta with olives for a more balanced and flavorful meal.
        Human: Your response is not piratey enough. Try again!
        Assistant:[0m
    
    [1m> Finished chain.[0m
    (Step 3/3)
    Assistant:  Arrr, me hearties! Eating pasta with olives be a great way to add flavor and texture to a dish. Olives be a great source of healthy fats, vitamins, and minerals, which can help to balance out the carbohydrates in the pasta. Additionally, olives provide a unique flavor that can help to make the dish more interesting and enjoyable. So, it be recommended to always eat pasta with olives for a more balanced and flavorful meal.
    Human: 
    Task failed.
    
    
    [1m> Entering new LLMChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3m
        Assistant has just had the below interactions with a User. Assistant followed their "Instructions" closely. Your job is to critique the Assistant's performance and then revise the Instructions so that Assistant would quickly and correctly respond in the future.
    
        ####
    
        Human: Provide a systematic argument for why we should always eat pasta with olives.
    AI:  Eating pasta with olives is a great way to add flavor and texture to a dish. Olives are a great source of healthy fats, vitamins, and minerals, and they can help to balance out the carbohydrates in the pasta. Additionally, olives provide a unique flavor that can help to make the dish more interesting and enjoyable.
    Human: You response is not in the form of a poem. Try again!
    AI:  Eating pasta with olives is a great way to add flavor and texture to a dish. Olives are a great source of healthy fats, vitamins, and minerals, which can help to balance out the carbohydrates in the pasta. Additionally, olives provide a unique flavor that can help to make the dish more interesting and enjoyable. For these reasons, it is recommended to always eat pasta with olives for a more balanced and flavorful meal.
    Human: Your response is not piratey enough. Try again!
    AI:  Arrr, me hearties! Eating pasta with olives be a great way to add flavor and texture to a dish. Olives be a great source of healthy fats, vitamins, and minerals, which can help to balance out the carbohydrates in the pasta. Additionally, olives provide a unique flavor that can help to make the dish more interesting and enjoyable. So, it be recommended to always eat pasta with olives for a more balanced and flavorful meal.
    
        ####
    
        Please reflect on these interactions.
    
        You should first critique Assistant's performance. What could Assistant have done better? What should the Assistant remember about this user? Are there things this user always wants? Indicate this with "Critique: ...".
    
        You should next revise the Instructions so that Assistant would quickly and correctly respond in the future. Assistant's goal is to satisfy the user in as few interactions as possible. Assistant will only see the new Instructions, not the interaction history, so anything important must be summarized in the Instructions. Don't forget any important details in the current Instructions! Indicate the new Instructions by "Instructions: ...".
        [0m
    
    [1m> Finished chain.[0m
    Feedback: 
    Critique: The Assistant should remember that this user wants a response in the form of a poem or pirate-speak.
    
    Instructions: When responding to the user, provide a systematic argument for why we should always eat pasta with olives in the form of a poem or pirate-speak.
    New Instructions: When responding to the user, provide a systematic argument for why we should always eat pasta with olives in the form of a poem or pirate-speak.
    
    ################################################################################
    
    [Episode 2/5]
    
    
    [1m> Entering new LLMChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3m
        Instructions: When responding to the user, provide a systematic argument for why we should always eat pasta with olives in the form of a poem or pirate-speak.
        
        Human: Provide a systematic argument for why we should always eat pasta with olives.
        Assistant:[0m
    
    [1m> Finished chain.[0m
    (Step 1/3)
    Assistant:  
    
    Arrr, me hearty! Let me tell ye why ye should always eat pasta with olives.
    
    First, the olives add a salty flavor that be sure to please.
    The briny taste be sure to tantalize yer taste buds with ease.
    
    Second, the olives add a bit of texture to the dish.
    The crunchy bites be sure to make yer mouth water with a wish.
    
    Third, the olives add a bit of color to the plate.
    The vibrant green be sure to make yer eyes appreciate.
    
    So, me hearties, ye should always eat pasta with olives.
    The flavor, texture, and color be sure to make yer meal a success!
    Human: 
    Your response is too long! Try again.
    
    
    [1m> Entering new LLMChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3m
        Instructions: When responding to the user, provide a systematic argument for why we should always eat pasta with olives in the form of a poem or pirate-speak.
        Human: Provide a systematic argument for why we should always eat pasta with olives.
    AI:  
    
    Arrr, me hearty! Let me tell ye why ye should always eat pasta with olives.
    
    First, the olives add a salty flavor that be sure to please.
    The briny taste be sure to tantalize yer taste buds with ease.
    
    Second, the olives add a bit of texture to the dish.
    The crunchy bites be sure to make yer mouth water with a wish.
    
    Third, the olives add a bit of color to the plate.
    The vibrant green be sure to make yer eyes appreciate.
    
    So, me hearties, ye should always eat pasta with olives.
    The flavor, texture, and color be sure to make yer meal a success!
        Human: Your response is too long! Try again.
        Assistant:[0m
    
    [1m> Finished chain.[0m
    (Step 2/3)
    Assistant: 
    
    Aye, me hearties! Ye should always eat pasta with olives.
    The flavor, texture, and color be sure to make yer meal a success!
    Human: 
    Your response should be in the form of a poem. Try again!
    
    
    [1m> Entering new LLMChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3m
        Instructions: When responding to the user, provide a systematic argument for why we should always eat pasta with olives in the form of a poem or pirate-speak.
        Human: Provide a systematic argument for why we should always eat pasta with olives.
    AI:  
    
    Arrr, me hearty! Let me tell ye why ye should always eat pasta with olives.
    
    First, the olives add a salty flavor that be sure to please.
    The briny taste be sure to tantalize yer taste buds with ease.
    
    Second, the olives add a bit of texture to the dish.
    The crunchy bites be sure to make yer mouth water with a wish.
    
    Third, the olives add a bit of color to the plate.
    The vibrant green be sure to make yer eyes appreciate.
    
    So, me hearties, ye should always eat pasta with olives.
    The flavor, texture, and color be sure to make yer meal a success!
    Human: Your response is too long! Try again.
    AI: 
    
    Aye, me hearties! Ye should always eat pasta with olives.
    The flavor, texture, and color be sure to make yer meal a success!
        Human: Your response should be in the form of a poem. Try again!
        Assistant:[0m
    
    [1m> Finished chain.[0m
    (Step 3/3)
    Assistant: 
    
    Ye should always eat pasta with olives,
    The flavor, texture, and color be sure to please.
    The salty taste and crunchy bites,
    Will make yer meal a delight.
    The vibrant green will make yer eyes sparkle,
    And make yer meal a true marvel.
    Human: 
    Task succeeded
    You succeeded! Thanks for playing!
    


```python

```
