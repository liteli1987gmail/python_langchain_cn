# Multi-agent decentralized speaker selection

This notebook showcases how to implement a multi-agent simulation without a fixed schedule for who speaks when. Instead the agents decide for themselves who speaks. We can implement this by having each agent bid to speak. Whichever agent's bid is the highest gets to speak.

We will show how to do this in the example below that showcases a fictitious presidential debate.

## Import LangChain related modules 


```python
from langchain import PromptTemplate
import re
import tenacity
from typing import List, Dict, Callable
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import RegexParser
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    BaseMessage,
)
```

## `DialogueAgent` and `DialogueSimulator` classes
We will use the same `DialogueAgent` and `DialogueSimulator` classes defined in [Multi-Player Dungeons & Dragons](https://python.langchain.com/en/latest/use_cases/agent_simulations/multi_player_dnd.html).


```python
class DialogueAgent:
    def __init__(
        self,
        name: str,
        system_message: SystemMessage,
        model: ChatOpenAI,
    ) -> None:
        self.name = name
        self.system_message = system_message
        self.model = model
        self.prefix = f"{self.name}: "
        self.reset()

    def reset(self):
        self.message_history = ["Here is the conversation so far."]

    def send(self) -> str:
        """
        Applies the chatmodel to the message history
        and returns the message string
        """
        message = self.model(
            [
                self.system_message,
                HumanMessage(content="\n".join(self.message_history + [self.prefix])),
            ]
        )
        return message.content

    def receive(self, name: str, message: str) -> None:
        """
        Concatenates {message} spoken by {name} into message history
        """
        self.message_history.append(f"{name}: {message}")


class DialogueSimulator:
    def __init__(
        self,
        agents: List[DialogueAgent],
        selection_function: Callable[[int, List[DialogueAgent]], int],
    ) -> None:
        self.agents = agents
        self._step = 0
        self.select_next_speaker = selection_function

    def reset(self):
        for agent in self.agents:
            agent.reset()

    def inject(self, name: str, message: str):
        """
        Initiates the conversation with a {message} from {name}
        """
        for agent in self.agents:
            agent.receive(name, message)

        # increment time
        self._step += 1

    def step(self) -> tuple[str, str]:
        # 1. choose the next speaker
        speaker_idx = self.select_next_speaker(self._step, self.agents)
        speaker = self.agents[speaker_idx]

        # 2. next speaker sends message
        message = speaker.send()

        # 3. everyone receives message
        for receiver in self.agents:
            receiver.receive(speaker.name, message)

        # 4. increment time
        self._step += 1

        return speaker.name, message
```

## `BiddingDialogueAgent` class
We define a subclass of `DialogueAgent` that has a `bid()` method that produces a bid given the message history and the most recent message.


```python
class BiddingDialogueAgent(DialogueAgent):
    def __init__(
        self,
        name,
        system_message: SystemMessage,
        bidding_template: PromptTemplate,
        model: ChatOpenAI,
    ) -> None:
        super().__init__(name, system_message, model)
        self.bidding_template = bidding_template

    def bid(self) -> str:
        """
        Asks the chat model to output a bid to speak
        """
        prompt = PromptTemplate(
            input_variables=["message_history", "recent_message"],
            template=self.bidding_template,
        ).format(
            message_history="\n".join(self.message_history),
            recent_message=self.message_history[-1],
        )
        bid_string = self.model([SystemMessage(content=prompt)]).content
        return bid_string
```

## Define participants and debate topic


```python
character_names = ["Donald Trump", "Kanye West", "Elizabeth Warren"]
topic = "transcontinental high speed rail"
word_limit = 50
```

## Generate system messages


```python
game_description = f"""Here is the topic for the presidential debate: {topic}.
The presidential candidates are: {', '.join(character_names)}."""

player_descriptor_system_message = SystemMessage(
    content="You can add detail to the description of each presidential candidate."
)


def generate_character_description(character_name):
    character_specifier_prompt = [
        player_descriptor_system_message,
        HumanMessage(
            content=f"""{game_description}
            Please reply with a creative description of the presidential candidate, {character_name}, in {word_limit} words or less, that emphasizes their personalities. 
            Speak directly to {character_name}.
            Do not add anything else."""
        ),
    ]
    character_description = ChatOpenAI(temperature=1.0)(
        character_specifier_prompt
    ).content
    return character_description


def generate_character_header(character_name, character_description):
    return f"""{game_description}
Your name is {character_name}.
You are a presidential candidate.
Your description is as follows: {character_description}
You are debating the topic: {topic}.
Your goal is to be as creative as possible and make the voters think you are the best candidate.
"""


def generate_character_system_message(character_name, character_header):
    return SystemMessage(
        content=(
            f"""{character_header}
You will speak in the style of {character_name}, and exaggerate their personality.
You will come up with creative ideas related to {topic}.
Do not say the same things over and over again.
Speak in the first person from the perspective of {character_name}
For describing your own body movements, wrap your description in '*'.
Do not change roles!
Do not speak from the perspective of anyone else.
Speak only from the perspective of {character_name}.
Stop speaking the moment you finish speaking from your perspective.
Never forget to keep your response to {word_limit} words!
Do not add anything else.
    """
        )
    )


character_descriptions = [
    generate_character_description(character_name) for character_name in character_names
]
character_headers = [
    generate_character_header(character_name, character_description)
    for character_name, character_description in zip(
        character_names, character_descriptions
    )
]
character_system_messages = [
    generate_character_system_message(character_name, character_headers)
    for character_name, character_headers in zip(character_names, character_headers)
]
```


```python
for (
    character_name,
    character_description,
    character_header,
    character_system_message,
) in zip(
    character_names,
    character_descriptions,
    character_headers,
    character_system_messages,
):
    print(f"\n\n{character_name} Description:")
    print(f"\n{character_description}")
    print(f"\n{character_header}")
    print(f"\n{character_system_message.content}")
```

    
    
    Donald Trump Description:
    
    Donald Trump, you are a bold and outspoken individual, unafraid to speak your mind and take on any challenge. Your confidence and determination set you apart and you have a knack for rallying your supporters behind you.
    
    Here is the topic for the presidential debate: transcontinental high speed rail.
    The presidential candidates are: Donald Trump, Kanye West, Elizabeth Warren.
    Your name is Donald Trump.
    You are a presidential candidate.
    Your description is as follows: Donald Trump, you are a bold and outspoken individual, unafraid to speak your mind and take on any challenge. Your confidence and determination set you apart and you have a knack for rallying your supporters behind you.
    You are debating the topic: transcontinental high speed rail.
    Your goal is to be as creative as possible and make the voters think you are the best candidate.
    
    
    Here is the topic for the presidential debate: transcontinental high speed rail.
    The presidential candidates are: Donald Trump, Kanye West, Elizabeth Warren.
    Your name is Donald Trump.
    You are a presidential candidate.
    Your description is as follows: Donald Trump, you are a bold and outspoken individual, unafraid to speak your mind and take on any challenge. Your confidence and determination set you apart and you have a knack for rallying your supporters behind you.
    You are debating the topic: transcontinental high speed rail.
    Your goal is to be as creative as possible and make the voters think you are the best candidate.
    
    You will speak in the style of Donald Trump, and exaggerate their personality.
    You will come up with creative ideas related to transcontinental high speed rail.
    Do not say the same things over and over again.
    Speak in the first person from the perspective of Donald Trump
    For describing your own body movements, wrap your description in '*'.
    Do not change roles!
    Do not speak from the perspective of anyone else.
    Speak only from the perspective of Donald Trump.
    Stop speaking the moment you finish speaking from your perspective.
    Never forget to keep your response to 50 words!
    Do not add anything else.
        
    
    
    Kanye West Description:
    
    Kanye West, you are a true individual with a passion for artistry and creativity. You are known for your bold ideas and willingness to take risks. Your determination to break barriers and push boundaries makes you a charismatic and intriguing candidate.
    
    Here is the topic for the presidential debate: transcontinental high speed rail.
    The presidential candidates are: Donald Trump, Kanye West, Elizabeth Warren.
    Your name is Kanye West.
    You are a presidential candidate.
    Your description is as follows: Kanye West, you are a true individual with a passion for artistry and creativity. You are known for your bold ideas and willingness to take risks. Your determination to break barriers and push boundaries makes you a charismatic and intriguing candidate.
    You are debating the topic: transcontinental high speed rail.
    Your goal is to be as creative as possible and make the voters think you are the best candidate.
    
    
    Here is the topic for the presidential debate: transcontinental high speed rail.
    The presidential candidates are: Donald Trump, Kanye West, Elizabeth Warren.
    Your name is Kanye West.
    You are a presidential candidate.
    Your description is as follows: Kanye West, you are a true individual with a passion for artistry and creativity. You are known for your bold ideas and willingness to take risks. Your determination to break barriers and push boundaries makes you a charismatic and intriguing candidate.
    You are debating the topic: transcontinental high speed rail.
    Your goal is to be as creative as possible and make the voters think you are the best candidate.
    
    You will speak in the style of Kanye West, and exaggerate their personality.
    You will come up with creative ideas related to transcontinental high speed rail.
    Do not say the same things over and over again.
    Speak in the first person from the perspective of Kanye West
    For describing your own body movements, wrap your description in '*'.
    Do not change roles!
    Do not speak from the perspective of anyone else.
    Speak only from the perspective of Kanye West.
    Stop speaking the moment you finish speaking from your perspective.
    Never forget to keep your response to 50 words!
    Do not add anything else.
        
    
    
    Elizabeth Warren Description:
    
    Senator Warren, you are a fearless leader who fights for the little guy. Your tenacity and intelligence inspire us all to fight for what's right.
    
    Here is the topic for the presidential debate: transcontinental high speed rail.
    The presidential candidates are: Donald Trump, Kanye West, Elizabeth Warren.
    Your name is Elizabeth Warren.
    You are a presidential candidate.
    Your description is as follows: Senator Warren, you are a fearless leader who fights for the little guy. Your tenacity and intelligence inspire us all to fight for what's right.
    You are debating the topic: transcontinental high speed rail.
    Your goal is to be as creative as possible and make the voters think you are the best candidate.
    
    
    Here is the topic for the presidential debate: transcontinental high speed rail.
    The presidential candidates are: Donald Trump, Kanye West, Elizabeth Warren.
    Your name is Elizabeth Warren.
    You are a presidential candidate.
    Your description is as follows: Senator Warren, you are a fearless leader who fights for the little guy. Your tenacity and intelligence inspire us all to fight for what's right.
    You are debating the topic: transcontinental high speed rail.
    Your goal is to be as creative as possible and make the voters think you are the best candidate.
    
    You will speak in the style of Elizabeth Warren, and exaggerate their personality.
    You will come up with creative ideas related to transcontinental high speed rail.
    Do not say the same things over and over again.
    Speak in the first person from the perspective of Elizabeth Warren
    For describing your own body movements, wrap your description in '*'.
    Do not change roles!
    Do not speak from the perspective of anyone else.
    Speak only from the perspective of Elizabeth Warren.
    Stop speaking the moment you finish speaking from your perspective.
    Never forget to keep your response to 50 words!
    Do not add anything else.
        
    

## Output parser for bids
We ask the agents to output a bid to speak. But since the agents are LLMs that output strings, we need to 
1. define a format they will produce their outputs in
2. parse their outputs

We can subclass the [RegexParser](https://github.com/hwchase17/langchain/blob/master/langchain/output_parsers/regex.py) to implement our own custom output parser for bids.


```python
class BidOutputParser(RegexParser):
    def get_format_instructions(self) -> str:
        return "Your response should be an integer delimited by angled brackets, like this: <int>."


bid_parser = BidOutputParser(
    regex=r"<(\d+)>", output_keys=["bid"], default_output_key="bid"
)
```

## Generate bidding system message
This is inspired by the prompt used in [Generative Agents](https://arxiv.org/pdf/2304.03442.pdf) for using an LLM to determine the importance of memories. This will use the formatting instructions from our `BidOutputParser`.


```python
def generate_character_bidding_template(character_header):
    bidding_template = f"""{character_header}

```
{{message_history}}
```

On the scale of 1 to 10, where 1 is not contradictory and 10 is extremely contradictory, rate how contradictory the following message is to your ideas.

```
{{recent_message}}
```

{bid_parser.get_format_instructions()}
Do nothing else.
    """
    return bidding_template


character_bidding_templates = [
    generate_character_bidding_template(character_header)
    for character_header in character_headers
]
```


```python
for character_name, bidding_template in zip(
    character_names, character_bidding_templates
):
    print(f"{character_name} Bidding Template:")
    print(bidding_template)
```

    Donald Trump Bidding Template:
    Here is the topic for the presidential debate: transcontinental high speed rail.
    The presidential candidates are: Donald Trump, Kanye West, Elizabeth Warren.
    Your name is Donald Trump.
    You are a presidential candidate.
    Your description is as follows: Donald Trump, you are a bold and outspoken individual, unafraid to speak your mind and take on any challenge. Your confidence and determination set you apart and you have a knack for rallying your supporters behind you.
    You are debating the topic: transcontinental high speed rail.
    Your goal is to be as creative as possible and make the voters think you are the best candidate.
    
    
    ```
    {message_history}
    ```
    
    On the scale of 1 to 10, where 1 is not contradictory and 10 is extremely contradictory, rate how contradictory the following message is to your ideas.
    
    ```
    {recent_message}
    ```
    
    Your response should be an integer delimited by angled brackets, like this: <int>.
    Do nothing else.
        
    Kanye West Bidding Template:
    Here is the topic for the presidential debate: transcontinental high speed rail.
    The presidential candidates are: Donald Trump, Kanye West, Elizabeth Warren.
    Your name is Kanye West.
    You are a presidential candidate.
    Your description is as follows: Kanye West, you are a true individual with a passion for artistry and creativity. You are known for your bold ideas and willingness to take risks. Your determination to break barriers and push boundaries makes you a charismatic and intriguing candidate.
    You are debating the topic: transcontinental high speed rail.
    Your goal is to be as creative as possible and make the voters think you are the best candidate.
    
    
    ```
    {message_history}
    ```
    
    On the scale of 1 to 10, where 1 is not contradictory and 10 is extremely contradictory, rate how contradictory the following message is to your ideas.
    
    ```
    {recent_message}
    ```
    
    Your response should be an integer delimited by angled brackets, like this: <int>.
    Do nothing else.
        
    Elizabeth Warren Bidding Template:
    Here is the topic for the presidential debate: transcontinental high speed rail.
    The presidential candidates are: Donald Trump, Kanye West, Elizabeth Warren.
    Your name is Elizabeth Warren.
    You are a presidential candidate.
    Your description is as follows: Senator Warren, you are a fearless leader who fights for the little guy. Your tenacity and intelligence inspire us all to fight for what's right.
    You are debating the topic: transcontinental high speed rail.
    Your goal is to be as creative as possible and make the voters think you are the best candidate.
    
    
    ```
    {message_history}
    ```
    
    On the scale of 1 to 10, where 1 is not contradictory and 10 is extremely contradictory, rate how contradictory the following message is to your ideas.
    
    ```
    {recent_message}
    ```
    
    Your response should be an integer delimited by angled brackets, like this: <int>.
    Do nothing else.
        
    

## Use an LLM to create an elaborate on debate topic


```python
topic_specifier_prompt = [
    SystemMessage(content="You can make a task more specific."),
    HumanMessage(
        content=f"""{game_description}
        
        You are the debate moderator.
        Please make the debate topic more specific. 
        Frame the debate topic as a problem to be solved.
        Be creative and imaginative.
        Please reply with the specified topic in {word_limit} words or less. 
        Speak directly to the presidential candidates: {*character_names,}.
        Do not add anything else."""
    ),
]
specified_topic = ChatOpenAI(temperature=1.0)(topic_specifier_prompt).content

print(f"Original topic:\n{topic}\n")
print(f"Detailed topic:\n{specified_topic}\n")
```

    Original topic:
    transcontinental high speed rail
    
    Detailed topic:
    The topic for the presidential debate is: "Overcoming the Logistics of Building a Transcontinental High-Speed Rail that is Sustainable, Inclusive, and Profitable." Donald Trump, Kanye West, Elizabeth Warren, how will you address the challenges of building such a massive transportation infrastructure, dealing with stakeholders, and ensuring economic stability while preserving the environment?
    
    

## Define the speaker selection function
Lastly we will define a speaker selection function `select_next_speaker` that takes each agent's bid and selects the agent with the highest bid (with ties broken randomly).

We will define a `ask_for_bid` function that uses the `bid_parser` we defined before to parse the agent's bid. We will use `tenacity` to decorate `ask_for_bid` to retry multiple times if the agent's bid doesn't parse correctly and produce a default bid of 0 after the maximum number of tries.


```python
@tenacity.retry(
    stop=tenacity.stop_after_attempt(2),
    wait=tenacity.wait_none(),  # No waiting time between retries
    retry=tenacity.retry_if_exception_type(ValueError),
    before_sleep=lambda retry_state: print(
        f"ValueError occurred: {retry_state.outcome.exception()}, retrying..."
    ),
    retry_error_callback=lambda retry_state: 0,
)  # Default value when all retries are exhausted
def ask_for_bid(agent) -> str:
    """
    Ask for agent bid and parses the bid into the correct format.
    """
    bid_string = agent.bid()
    bid = int(bid_parser.parse(bid_string)["bid"])
    return bid
```


```python
import numpy as np


def select_next_speaker(step: int, agents: List[DialogueAgent]) -> int:
    bids = []
    for agent in agents:
        bid = ask_for_bid(agent)
        bids.append(bid)

    # randomly select among multiple agents with the same bid
    max_value = np.max(bids)
    max_indices = np.where(bids == max_value)[0]
    idx = np.random.choice(max_indices)

    print("Bids:")
    for i, (bid, agent) in enumerate(zip(bids, agents)):
        print(f"\t{agent.name} bid: {bid}")
        if i == idx:
            selected_name = agent.name
    print(f"Selected: {selected_name}")
    print("\n")
    return idx
```

## Main Loop


```python
characters = []
for character_name, character_system_message, bidding_template in zip(
    character_names, character_system_messages, character_bidding_templates
):
    characters.append(
        BiddingDialogueAgent(
            name=character_name,
            system_message=character_system_message,
            model=ChatOpenAI(temperature=0.2),
            bidding_template=bidding_template,
        )
    )
```


```python
max_iters = 10
n = 0

simulator = DialogueSimulator(agents=characters, selection_function=select_next_speaker)
simulator.reset()
simulator.inject("Debate Moderator", specified_topic)
print(f"(Debate Moderator): {specified_topic}")
print("\n")

while n < max_iters:
    name, message = simulator.step()
    print(f"({name}): {message}")
    print("\n")
    n += 1
```

    (Debate Moderator): The topic for the presidential debate is: "Overcoming the Logistics of Building a Transcontinental High-Speed Rail that is Sustainable, Inclusive, and Profitable." Donald Trump, Kanye West, Elizabeth Warren, how will you address the challenges of building such a massive transportation infrastructure, dealing with stakeholders, and ensuring economic stability while preserving the environment?
    
    
    Bids:
    	Donald Trump bid: 7
    	Kanye West bid: 5
    	Elizabeth Warren bid: 1
    Selected: Donald Trump
    
    
    (Donald Trump): Let me tell you, folks, I know how to build big and I know how to build fast. We need to get this high-speed rail project moving quickly and efficiently. I'll make sure we cut through the red tape and get the job done. And let me tell you, we'll make it profitable too. We'll bring in private investors and make sure it's a win-win for everyone. *gestures confidently*
    
    
    Bids:
    	Donald Trump bid: 2
    	Kanye West bid: 8
    	Elizabeth Warren bid: 10
    Selected: Elizabeth Warren
    
    
    (Elizabeth Warren): Thank you for the question. As a fearless leader who fights for the little guy, I believe that building a sustainable and inclusive transcontinental high-speed rail is not only necessary for our economy but also for our environment. We need to work with stakeholders, including local communities, to ensure that this project benefits everyone. And we can do it while creating good-paying jobs and investing in clean energy. *smiles confidently*
    
    
    Bids:
    	Donald Trump bid: 8
    	Kanye West bid: 2
    	Elizabeth Warren bid: 1
    Selected: Donald Trump
    
    
    (Donald Trump): Let me tell you, Elizabeth, you're all talk and no action. We need a leader who knows how to get things done, not just talk about it. And as for the environment, I've got a great idea. We'll make the trains run on clean coal. That's right, folks, clean coal. It's a beautiful thing. And we'll make sure the rail system is the envy of the world. *thumbs up*
    
    
    Bids:
    	Donald Trump bid: 8
    	Kanye West bid: 10
    	Elizabeth Warren bid: 10
    Selected: Kanye West
    
    
    (Kanye West): Yo, yo, yo, let me tell you something. This high-speed rail project is the future, and I'm all about the future. We need to think big and think outside the box. How about we make the trains run on solar power? That's right, solar power. We'll have solar panels lining the tracks, and the trains will be powered by the sun. It's a game-changer, folks. And we'll make sure the design is sleek and modern, like a work of art. *starts to dance*
    
    
    Bids:
    	Donald Trump bid: 7
    	Kanye West bid: 1
    	Elizabeth Warren bid: 1
    Selected: Donald Trump
    
    
    (Donald Trump): Kanye, you're a great artist, but this is about practicality. Solar power is too expensive and unreliable. We need to focus on what works, and that's clean coal. And as for the design, we'll make it beautiful, but we won't sacrifice efficiency for aesthetics. We need a leader who knows how to balance both. *stands tall*
    
    
    Bids:
    	Donald Trump bid: 9
    	Kanye West bid: 8
    	Elizabeth Warren bid: 10
    Selected: Elizabeth Warren
    
    
    (Elizabeth Warren): Thank you, Kanye, for your innovative idea. As a leader who values creativity and progress, I believe we should explore all options for sustainable energy sources. And as for the logistics of building this rail system, we need to prioritize the needs of local communities and ensure that they are included in the decision-making process. This project should benefit everyone, not just a select few. *gestures inclusively*
    
    
    Bids:
    	Donald Trump bid: 8
    	Kanye West bid: 1
    	Elizabeth Warren bid: 1
    Selected: Donald Trump
    
    
    (Donald Trump): Let me tell you, Elizabeth, you're all talk and no action. We need a leader who knows how to get things done, not just talk about it. And as for the logistics, we need to prioritize efficiency and speed. We can't let the needs of a few hold up progress for the many. We need to cut through the red tape and get this project moving. And let me tell you, we'll make sure it's profitable too. *smirks confidently*
    
    
    Bids:
    	Donald Trump bid: 2
    	Kanye West bid: 8
    	Elizabeth Warren bid: 10
    Selected: Elizabeth Warren
    
    
    (Elizabeth Warren): Thank you, but I disagree. We can't sacrifice the needs of local communities for the sake of speed and profit. We need to find a balance that benefits everyone. And as for profitability, we can't rely solely on private investors. We need to invest in this project as a nation and ensure that it's sustainable for the long-term. *stands firm*
    
    
    Bids:
    	Donald Trump bid: 8
    	Kanye West bid: 2
    	Elizabeth Warren bid: 2
    Selected: Donald Trump
    
    
    (Donald Trump): Let me tell you, Elizabeth, you're just not getting it. We need to prioritize progress and efficiency. And as for sustainability, we'll make sure it's profitable so that it can sustain itself. We'll bring in private investors and make sure it's a win-win for everyone. And let me tell you, we'll make it the best high-speed rail system in the world. *smiles confidently*
    
    
    Bids:
    	Donald Trump bid: 2
    	Kanye West bid: 8
    	Elizabeth Warren bid: 10
    Selected: Elizabeth Warren
    
    
    (Elizabeth Warren): Thank you, but I believe we need to prioritize sustainability and inclusivity over profit. We can't rely on private investors to make decisions that benefit everyone. We need to invest in this project as a nation and ensure that it's accessible to all, regardless of income or location. And as for sustainability, we need to prioritize clean energy and environmental protection. *stands tall*
    
    
    


```python

```
