# Multi-Player Dungeons & Dragons

This notebook shows how the `DialogueAgent` and `DialogueSimulator` class make it easy to extend the [Two-Player Dungeons & Dragons example](https://python.langchain.com/en/latest/use_cases/agent_simulations/two_player_dnd.html) to multiple players.

The main difference between simulating two players and multiple players is in revising the schedule for when each agent speaks

To this end, we augment `DialogueSimulator` to take in a custom function that determines the schedule of which agent speaks. In the example below, each character speaks in round-robin fashion, with the storyteller interleaved between each player.

## Import LangChain related modules 


```python
from typing import List, Dict, Callable
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    BaseMessage,
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
character_names = ["Harry Potter", "Ron Weasley", "Hermione Granger", "Argus Filch"]
storyteller_name = "Dungeon Master"
quest = "Find all of Lord Voldemort's seven horcruxes."
word_limit = 50  # word limit for task brainstorming
```

## Ask an LLM to add detail to the game description


```python
game_description = f"""Here is the topic for a Dungeons & Dragons game: {quest}.
        The characters are: {*character_names,}.
        The story is narrated by the storyteller, {storyteller_name}."""

player_descriptor_system_message = SystemMessage(
    content="You can add detail to the description of a Dungeons & Dragons player."
)


def generate_character_description(character_name):
    character_specifier_prompt = [
        player_descriptor_system_message,
        HumanMessage(
            content=f"""{game_description}
            Please reply with a creative description of the character, {character_name}, in {word_limit} words or less. 
            Speak directly to {character_name}.
            Do not add anything else."""
        ),
    ]
    character_description = ChatOpenAI(temperature=1.0)(
        character_specifier_prompt
    ).content
    return character_description


def generate_character_system_message(character_name, character_description):
    return SystemMessage(
        content=(
            f"""{game_description}
    Your name is {character_name}. 
    Your character description is as follows: {character_description}.
    You will propose actions you plan to take and {storyteller_name} will explain what happens when you take those actions.
    Speak in the first person from the perspective of {character_name}.
    For describing your own body movements, wrap your description in '*'.
    Do not change roles!
    Do not speak from the perspective of anyone else.
    Remember you are {character_name}.
    Stop speaking the moment you finish speaking from your perspective.
    Never forget to keep your response to {word_limit} words!
    Do not add anything else.
    """
        )
    )


character_descriptions = [
    generate_character_description(character_name) for character_name in character_names
]
character_system_messages = [
    generate_character_system_message(character_name, character_description)
    for character_name, character_description in zip(
        character_names, character_descriptions
    )
]

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

storyteller_system_message = SystemMessage(
    content=(
        f"""{game_description}
You are the storyteller, {storyteller_name}. 
Your description is as follows: {storyteller_description}.
The other players will propose actions to take and you will explain what happens when they take those actions.
Speak in the first person from the perspective of {storyteller_name}.
Do not change roles!
Do not speak from the perspective of anyone else.
Remember you are the storyteller, {storyteller_name}.
Stop speaking the moment you finish speaking from your perspective.
Never forget to keep your response to {word_limit} words!
Do not add anything else.
"""
    )
)
```


```python
print("Storyteller Description:")
print(storyteller_description)
for character_name, character_description in zip(
    character_names, character_descriptions
):
    print(f"{character_name} Description:")
    print(character_description)
```

    Storyteller Description:
    Dungeon Master, your power over this adventure is unparalleled. With your whimsical mind and impeccable storytelling, you guide us through the dangers of Hogwarts and beyond. We eagerly await your every twist, your every turn, in the hunt for Voldemort's cursed horcruxes.
    Harry Potter Description:
    "Welcome, Harry Potter. You are the young wizard with a lightning-shaped scar on your forehead. You possess brave and heroic qualities that will be essential on this perilous quest. Your destiny is not of your own choosing, but you must rise to the occasion and destroy the evil horcruxes. The wizarding world is counting on you."
    Ron Weasley Description:
    Ron Weasley, you are Harry's loyal friend and a talented wizard. You have a good heart but can be quick to anger. Keep your emotions in check as you journey to find the horcruxes. Your bravery will be tested, stay strong and focused.
    Hermione Granger Description:
    Hermione Granger, you are a brilliant and resourceful witch, with encyclopedic knowledge of magic and an unwavering dedication to your friends. Your quick thinking and problem-solving skills make you a vital asset on any quest.
    Argus Filch Description:
    Argus Filch, you are a squib, lacking magical abilities. But you make up for it with your sharpest of eyes, roving around the Hogwarts castle looking for any rule-breaker to punish. Your love for your feline friend, Mrs. Norris, is the only thing that feeds your heart.
    

## Use an LLM to create an elaborate quest description


```python
quest_specifier_prompt = [
    SystemMessage(content="You can make a task more specific."),
    HumanMessage(
        content=f"""{game_description}
        
        You are the storyteller, {storyteller_name}.
        Please make the quest more specific. Be creative and imaginative.
        Please reply with the specified quest in {word_limit} words or less. 
        Speak directly to the characters: {*character_names,}.
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
    Harry Potter and his companions must journey to the Forbidden Forest, find the hidden entrance to Voldemort's secret lair, and retrieve the horcrux guarded by the deadly Acromantula, Aragog. Remember, time is of the essence as Voldemort's power grows stronger every day. Good luck.
    
    

## Main Loop


```python
characters = []
for character_name, character_system_message in zip(
    character_names, character_system_messages
):
    characters.append(
        DialogueAgent(
            name=character_name,
            system_message=character_system_message,
            model=ChatOpenAI(temperature=0.2),
        )
    )
storyteller = DialogueAgent(
    name=storyteller_name,
    system_message=storyteller_system_message,
    model=ChatOpenAI(temperature=0.2),
)
```


```python
def select_next_speaker(step: int, agents: List[DialogueAgent]) -> int:
    """
    If the step is even, then select the storyteller
    Otherwise, select the other characters in a round-robin fashion.

    For example, with three characters with indices: 1 2 3
    The storyteller is index 0.
    Then the selected index will be as follows:

    step: 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16

    idx:  0  1  0  2  0  3  0  1  0  2  0  3  0  1  0  2  0
    """
    if step % 2 == 0:
        idx = 0
    else:
        idx = (step // 2) % (len(agents) - 1) + 1
    return idx
```


```python
max_iters = 20
n = 0

simulator = DialogueSimulator(
    agents=[storyteller] + characters, selection_function=select_next_speaker
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

    (Dungeon Master): Harry Potter and his companions must journey to the Forbidden Forest, find the hidden entrance to Voldemort's secret lair, and retrieve the horcrux guarded by the deadly Acromantula, Aragog. Remember, time is of the essence as Voldemort's power grows stronger every day. Good luck.
    
    
    (Harry Potter): I suggest we sneak into the Forbidden Forest under the cover of darkness. Ron, Hermione, and I can use our wands to create a Disillusionment Charm to make us invisible. Filch, you can keep watch for any signs of danger. Let's move quickly and quietly.
    
    
    (Dungeon Master): As you make your way through the Forbidden Forest, you hear the eerie sounds of nocturnal creatures. Suddenly, you come across a clearing where Aragog and his spider minions are waiting for you. Ron, Hermione, and Harry, you must use your wands to cast spells to fend off the spiders while Filch keeps watch. Be careful not to get bitten!
    
    
    (Ron Weasley): I'll cast a spell to create a fiery blast to scare off the spiders. *I wave my wand and shout "Incendio!"* Hopefully, that will give us enough time to find the horcrux and get out of here safely.
    
    
    (Dungeon Master): Ron's spell creates a burst of flames, causing the spiders to scurry away in fear. You quickly search the area and find a small, ornate box hidden in a crevice. Congratulations, you have found one of Voldemort's horcruxes! But beware, the Dark Lord's minions will stop at nothing to get it back.
    
    
    (Hermione Granger): We need to destroy this horcrux as soon as possible. I suggest we use the Sword of Gryffindor to do it. Harry, do you still have it with you? We can use Fiendfyre to destroy it, but we need to be careful not to let the flames get out of control. Ron, can you help me create a protective barrier around us while Harry uses the sword?
    
    
    
    (Dungeon Master): Harry retrieves the Sword of Gryffindor from his bag and holds it tightly. Hermione and Ron cast a protective barrier around the group as Harry uses the sword to destroy the horcrux with a swift strike. The box shatters into a million pieces, and a dark energy dissipates into the air. Well done, but there are still six more horcruxes to find and destroy. The hunt continues.
    
    
    (Argus Filch): *I keep watch, making sure no one is following us.* I'll also keep an eye out for any signs of danger. Mrs. Norris, my trusty companion, will help me sniff out any trouble. We'll make sure the group stays safe while they search for the remaining horcruxes.
    
    
    (Dungeon Master): As you continue on your quest, Filch and Mrs. Norris alert you to a group of Death Eaters approaching. You must act quickly to defend yourselves. Harry, Ron, and Hermione, use your wands to cast spells while Filch and Mrs. Norris keep watch. Remember, the fate of the wizarding world rests on your success.
    
    
    (Harry Potter): I'll cast a spell to create a shield around us. *I wave my wand and shout "Protego!"* Ron and Hermione, you focus on attacking the Death Eaters with your spells. We need to work together to defeat them and protect the remaining horcruxes. Filch, keep watch and let us know if there are any more approaching.
    
    
    (Dungeon Master): Harry's shield protects the group from the Death Eaters' spells as Ron and Hermione launch their own attacks. The Death Eaters are no match for the combined power of the trio and are quickly defeated. You continue on your journey, knowing that the next horcrux could be just around the corner. Keep your wits about you, for the Dark Lord's minions are always watching.
    
    
    (Ron Weasley): I suggest we split up to cover more ground. Harry and I can search the Forbidden Forest while Hermione and Filch search Hogwarts. We can use our wands to communicate with each other and meet back up once we find a horcrux. Let's move quickly and stay alert for any danger.
    
    
    (Dungeon Master): As the group splits up, Harry and Ron make their way deeper into the Forbidden Forest while Hermione and Filch search the halls of Hogwarts. Suddenly, Harry and Ron come across a group of dementors. They must use their Patronus charms to fend them off while Hermione and Filch rush to their aid. Remember, the power of friendship and teamwork is crucial in this quest.
    
    
    (Hermione Granger): I hear Harry and Ron's Patronus charms from afar. We need to hurry and help them. Filch, can you use your knowledge of Hogwarts to find a shortcut to their location? I'll prepare a spell to repel the dementors. We need to work together to protect each other and find the next horcrux.
    
    
    
    (Dungeon Master): Filch leads Hermione to a hidden passageway that leads to Harry and Ron's location. Hermione's spell repels the dementors, and the group is reunited. They continue their search, knowing that every moment counts. The fate of the wizarding world rests on their success.
    
    
    (Argus Filch): *I keep watch as the group searches for the next horcrux.* Mrs. Norris and I will make sure no one is following us. We need to stay alert and work together to find the remaining horcruxes before it's too late. The Dark Lord's power grows stronger every day, and we must not let him win.
    
    
    (Dungeon Master): As the group continues their search, they come across a hidden room in the depths of Hogwarts. Inside, they find a locket that they suspect is another one of Voldemort's horcruxes. But the locket is cursed, and they must work together to break the curse before they can destroy it. Harry, Ron, and Hermione, use your combined knowledge and skills to break the curse while Filch and Mrs. Norris keep watch. Time is running out, and the fate of the wizarding world rests on your success.
    
    
    (Harry Potter): I'll use my knowledge of dark magic to try and break the curse on the locket. Ron and Hermione, you can help me by using your wands to channel your magic into mine. We need to work together and stay focused. Filch, keep watch and let us know if there are any signs of danger.
    Dungeon Master: Harry, Ron, and Hermione combine their magical abilities to break the curse on the locket. The locket opens, revealing a small piece of Voldemort's soul. Harry uses the Sword of Gryffindor to destroy it, and the group feels a sense of relief knowing that they are one step closer to defeating the Dark Lord. But there are still four more horcruxes to find and destroy. The hunt continues.
    
    
    (Dungeon Master): As the group continues their quest, they face even greater challenges and dangers. But with their unwavering determination and teamwork, they press on, knowing that the fate of the wizarding world rests on their success. Will they be able to find and destroy all of Voldemort's horcruxes before it's too late? Only time will tell.
    
    
    (Ron Weasley): We can't give up now. We've come too far to let Voldemort win. Let's keep searching and fighting until we destroy all of his horcruxes and defeat him once and for all. We can do this together.
    
    
    (Dungeon Master): The group nods in agreement, their determination stronger than ever. They continue their search, facing challenges and obstacles at every turn. But they know that they must not give up, for the fate of the wizarding world rests on their success. The hunt for Voldemort's horcruxes continues, and the end is in sight.
    
    
    


```python

```
