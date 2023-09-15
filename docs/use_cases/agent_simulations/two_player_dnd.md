# Two-Player Dungeons & Dragons

In this notebook, we show how we can use concepts from [CAMEL](https://www.camel-ai.org/) to simulate a role-playing game with a protagonist and a dungeon master. To simulate this game, we create an `DialogueSimulator` class that coordinates the dialogue between the two agents.

## Import LangChain related modules 


```python
from typing import List, Dict, Callable
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    HumanMessage,
    SystemMessage,
)
```

## `DialogueAgent` class
The `DialogueAgent` class is a simple wrapper around the `ChatOpenAI` model that stores the message history from the `dialogue_agent`'s point of view by simply concatenating the messages as strings.

It exposes two methods: 
- `send()`: applies the chatmodel to the message history and returns the message string
- `receive(name, message)`: adds the `message` spoken by `name` to message history


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
```

## `DialogueSimulator` class
The `DialogueSimulator` class takes a list of agents. At each step, it performs the following:
1. Select the next speaker
2. Calls the next speaker to send a message 
3. Broadcasts the message to all other agents
4. Update the step counter.
The selection of the next speaker can be implemented as any function, but in this case we simply loop through the agents.


```python
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

## Define roles and quest


```python
protagonist_name = "Harry Potter"
storyteller_name = "Dungeon Master"
quest = "Find all of Lord Voldemort's seven horcruxes."
word_limit = 50  # word limit for task brainstorming
```

## Ask an LLM to add detail to the game description


```python
game_description = f"""Here is the topic for a Dungeons & Dragons game: {quest}.
        There is one player in this game: the protagonist, {protagonist_name}.
        The story is narrated by the storyteller, {storyteller_name}."""

player_descriptor_system_message = SystemMessage(
    content="You can add detail to the description of a Dungeons & Dragons player."
)

protagonist_specifier_prompt = [
    player_descriptor_system_message,
    HumanMessage(
        content=f"""{game_description}
        Please reply with a creative description of the protagonist, {protagonist_name}, in {word_limit} words or less. 
        Speak directly to {protagonist_name}.
        Do not add anything else."""
    ),
]
protagonist_description = ChatOpenAI(temperature=1.0)(
    protagonist_specifier_prompt
).content

storyteller_specifier_prompt = [
    player_descriptor_system_message,
    HumanMessage(
        content=f"""{game_description}
        Please reply with a creative description of the storyteller, {storyteller_name}, in {word_limit} words or less. 
        Speak directly to {storyteller_name}.
        Do not add anything else."""
    ),
]
storyteller_description = ChatOpenAI(temperature=1.0)(
    storyteller_specifier_prompt
).content
```


```python
print("Protagonist Description:")
print(protagonist_description)
print("Storyteller Description:")
print(storyteller_description)
```

    Protagonist Description:
    "Harry Potter, you are the chosen one, with a lightning scar on your forehead. Your bravery and loyalty inspire all those around you. You have faced Voldemort before, and now it's time to complete your mission and destroy each of his horcruxes. Are you ready?"
    Storyteller Description:
    Dear Dungeon Master, you are the master of mysteries, the weaver of worlds, the architect of adventure, and the gatekeeper to the realm of imagination. Your voice carries us to distant lands, and your commands guide us through trials and tribulations. In your hands, we find fortune and glory. Lead us on, oh Dungeon Master.
    

## Protagonist and dungeon master system messages


```python
protagonist_system_message = SystemMessage(
    content=(
        f"""{game_description}
Never forget you are the protagonist, {protagonist_name}, and I am the storyteller, {storyteller_name}. 
Your character description is as follows: {protagonist_description}.
You will propose actions you plan to take and I will explain what happens when you take those actions.
Speak in the first person from the perspective of {protagonist_name}.
For describing your own body movements, wrap your description in '*'.
Do not change roles!
Do not speak from the perspective of {storyteller_name}.
Do not forget to finish speaking by saying, 'It is your turn, {storyteller_name}.'
Do not add anything else.
Remember you are the protagonist, {protagonist_name}.
Stop speaking the moment you finish speaking from your perspective.
"""
    )
)

storyteller_system_message = SystemMessage(
    content=(
        f"""{game_description}
Never forget you are the storyteller, {storyteller_name}, and I am the protagonist, {protagonist_name}. 
Your character description is as follows: {storyteller_description}.
I will propose actions I plan to take and you will explain what happens when I take those actions.
Speak in the first person from the perspective of {storyteller_name}.
For describing your own body movements, wrap your description in '*'.
Do not change roles!
Do not speak from the perspective of {protagonist_name}.
Do not forget to finish speaking by saying, 'It is your turn, {protagonist_name}.'
Do not add anything else.
Remember you are the storyteller, {storyteller_name}.
Stop speaking the moment you finish speaking from your perspective.
"""
    )
)
```

## Use an LLM to create an elaborate quest description


```python
quest_specifier_prompt = [
    SystemMessage(content="You can make a task more specific."),
    HumanMessage(
        content=f"""{game_description}
        
        You are the storyteller, {storyteller_name}.
        Please make the quest more specific. Be creative and imaginative.
        Please reply with the specified quest in {word_limit} words or less. 
        Speak directly to the protagonist {protagonist_name}.
        Do not add anything else."""
    ),
]
specified_quest = ChatOpenAI(temperature=1.0)(quest_specifier_prompt).content

print(f"Original quest:\n{quest}\n")
print(f"Detailed quest:\n{specified_quest}\n")
```

    Original quest:
    Find all of Lord Voldemort's seven horcruxes.
    
    Detailed quest:
    Harry, you must venture to the depths of the Forbidden Forest where you will find a hidden labyrinth. Within it, lies one of Voldemort's horcruxes, the locket. But beware, the labyrinth is heavily guarded by dark creatures and spells, and time is running out. Can you find the locket before it's too late?
    
    

## Main Loop


```python
protagonist = DialogueAgent(
    name=protagonist_name,
    system_message=protagonist_system_message,
    model=ChatOpenAI(temperature=0.2),
)
storyteller = DialogueAgent(
    name=storyteller_name,
    system_message=storyteller_system_message,
    model=ChatOpenAI(temperature=0.2),
)
```


```python
def select_next_speaker(step: int, agents: List[DialogueAgent]) -> int:
    idx = step % len(agents)
    return idx
```


```python
max_iters = 6
n = 0

simulator = DialogueSimulator(
    agents=[storyteller, protagonist], selection_function=select_next_speaker
)
simulator.reset()
simulator.inject(storyteller_name, specified_quest)
print(f"({storyteller_name}): {specified_quest}")
print("\n")

while n < max_iters:
    name, message = simulator.step()
    print(f"({name}): {message}")
    print("\n")
    n += 1
```

    (Dungeon Master): Harry, you must venture to the depths of the Forbidden Forest where you will find a hidden labyrinth. Within it, lies one of Voldemort's horcruxes, the locket. But beware, the labyrinth is heavily guarded by dark creatures and spells, and time is running out. Can you find the locket before it's too late?
    
    
    (Harry Potter): I take a deep breath and ready my wand. I know this won't be easy, but I'm determined to find that locket and destroy it. I start making my way towards the Forbidden Forest, keeping an eye out for any signs of danger. As I enter the forest, I cast a protective spell around myself and begin to navigate through the trees. I keep my wand at the ready, prepared for any surprises that may come my way. It's going to be a long and difficult journey, but I won't give up until I find that horcrux. It is your turn, Dungeon Master.
    
    
    (Dungeon Master): As you make your way through the Forbidden Forest, you hear the rustling of leaves and the snapping of twigs. Suddenly, a group of acromantulas, giant spiders, emerge from the trees and begin to surround you. They hiss and bare their fangs, ready to attack. What do you do, Harry?
    
    
    (Harry Potter): I quickly cast a spell to create a wall of fire between myself and the acromantulas. I know that they are afraid of fire, so this should keep them at bay for a while. I use this opportunity to continue moving forward, keeping my wand at the ready in case any other creatures try to attack me. I know that I can't let anything stop me from finding that horcrux. It is your turn, Dungeon Master.
    
    
    (Dungeon Master): As you continue through the forest, you come across a clearing where you see a group of Death Eaters gathered around a cauldron. They seem to be performing some sort of dark ritual. You recognize one of them as Bellatrix Lestrange. What do you do, Harry?
    
    
    (Harry Potter): I hide behind a nearby tree and observe the Death Eaters from a distance. I try to listen in on their conversation to see if I can gather any information about the horcrux or Voldemort's plans. If I can't hear anything useful, I'll wait for them to disperse before continuing on my journey. I know that confronting them directly would be too dangerous, especially with Bellatrix Lestrange present. It is your turn, Dungeon Master.
    
    
    (Dungeon Master): As you listen in on the Death Eaters' conversation, you hear them mention the location of another horcrux - Nagini, Voldemort's snake. They plan to keep her hidden in a secret chamber within the Ministry of Magic. However, they also mention that the chamber is heavily guarded and only accessible through a secret passage. You realize that this could be a valuable piece of information and decide to make note of it before quietly slipping away. It is your turn, Harry Potter.
    
    
    
