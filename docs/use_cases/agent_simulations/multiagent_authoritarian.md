# Multi-agent authoritarian speaker selection

This notebook showcases how to implement a multi-agent simulation where a privileged agent decides who to speak.
This follows the polar opposite selection scheme as [multi-agent decentralized speaker selection](https://python.langchain.com/en/latest/use_cases/agent_simulations/multiagent_bidding.html).

We show an example of this approach in the context of a fictitious simulation of a news network. This example will showcase how we can implement agents that
- think before speaking
- terminate the conversation

## Import LangChain related modules 


```python
from collections import OrderedDict
import functools
import random
import re
import tenacity
from typing import List, Dict, Callable

from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    PromptTemplate,
)
from langchain.chains import LLMChain
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
We will use the same `DialogueAgent` and `DialogueSimulator` classes defined in our other examples [Multi-Player Dungeons & Dragons](https://python.langchain.com/en/latest/use_cases/agent_simulations/multi_player_dnd.html) and [Decentralized Speaker Selection](https://python.langchain.com/en/latest/use_cases/agent_simulations/multiagent_bidding.html).


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

## `DirectorDialogueAgent` class
The `DirectorDialogueAgent` is a privileged agent that chooses which of the other agents to speak next. This agent is responsible for
1. steering the conversation by choosing which agent speaks when
2. terminating the conversation.

In order to implement such an agent, we need to solve several problems.

First, to steer the conversation, the `DirectorDialogueAgent` needs to (1) reflect on what has been said, (2) choose the next agent, and (3) prompt the next agent to speak, all in a single message. While it may be possible to prompt an LLM to perform all three steps in the same call, this requires writing custom code to parse the outputted message to extract which next agent is chosen to speak. This is less reliable the LLM can express how it chooses the next agent in different ways.

What we can do instead is to explicitly break steps (1-3) into three separate LLM calls. First we will ask the `DirectorDialogueAgent` to reflect on the conversation so far and generate a response. Then we prompt the `DirectorDialogueAgent` to output the index of the next agent, which is easily parseable. Lastly, we pass the name of the selected next agent back to `DirectorDialogueAgent` to ask it prompt the next agent to speak. 

Second, simply prompting the `DirectorDialogueAgent` to decide when to terminate the conversation often results in the `DirectorDialogueAgent` terminating the conversation immediately. To fix this problem, we randomly sample a Bernoulli variable to decide whether the conversation should terminate. Depending on the value of this variable, we will inject a custom prompt to tell the `DirectorDialogueAgent` to either continue the conversation or terminate the conversation.


```python
class IntegerOutputParser(RegexParser):
    def get_format_instructions(self) -> str:
        return "Your response should be an integer delimited by angled brackets, like this: <int>."


class DirectorDialogueAgent(DialogueAgent):
    def __init__(
        self,
        name,
        system_message: SystemMessage,
        model: ChatOpenAI,
        speakers: List[DialogueAgent],
        stopping_probability: float,
    ) -> None:
        super().__init__(name, system_message, model)
        self.speakers = speakers
        self.next_speaker = ""

        self.stop = False
        self.stopping_probability = stopping_probability
        self.termination_clause = "Finish the conversation by stating a concluding message and thanking everyone."
        self.continuation_clause = "Do not end the conversation. Keep the conversation going by adding your own ideas."

        # 1. have a prompt for generating a response to the previous speaker
        self.response_prompt_template = PromptTemplate(
            input_variables=["message_history", "termination_clause"],
            template=f"""{{message_history}}

Follow up with an insightful comment.
{{termination_clause}}
{self.prefix}
        """,
        )

        # 2. have a prompt for deciding who to speak next
        self.choice_parser = IntegerOutputParser(
            regex=r"<(\d+)>", output_keys=["choice"], default_output_key="choice"
        )
        self.choose_next_speaker_prompt_template = PromptTemplate(
            input_variables=["message_history", "speaker_names"],
            template=f"""{{message_history}}

Given the above conversation, select the next speaker by choosing index next to their name: 
{{speaker_names}}

{self.choice_parser.get_format_instructions()}

Do nothing else.
        """,
        )

        # 3. have a prompt for prompting the next speaker to speak
        self.prompt_next_speaker_prompt_template = PromptTemplate(
            input_variables=["message_history", "next_speaker"],
            template=f"""{{message_history}}

The next speaker is {{next_speaker}}. 
Prompt the next speaker to speak with an insightful question.
{self.prefix}
        """,
        )

    def _generate_response(self):
        # if self.stop = True, then we will inject the prompt with a termination clause
        sample = random.uniform(0, 1)
        self.stop = sample < self.stopping_probability

        print(f"\tStop? {self.stop}\n")

        response_prompt = self.response_prompt_template.format(
            message_history="\n".join(self.message_history),
            termination_clause=self.termination_clause if self.stop else "",
        )

        self.response = self.model(
            [
                self.system_message,
                HumanMessage(content=response_prompt),
            ]
        ).content

        return self.response

    @tenacity.retry(
        stop=tenacity.stop_after_attempt(2),
        wait=tenacity.wait_none(),  # No waiting time between retries
        retry=tenacity.retry_if_exception_type(ValueError),
        before_sleep=lambda retry_state: print(
            f"ValueError occurred: {retry_state.outcome.exception()}, retrying..."
        ),
        retry_error_callback=lambda retry_state: 0,
    )  # Default value when all retries are exhausted
    def _choose_next_speaker(self) -> str:
        speaker_names = "\n".join(
            [f"{idx}: {name}" for idx, name in enumerate(self.speakers)]
        )
        choice_prompt = self.choose_next_speaker_prompt_template.format(
            message_history="\n".join(
                self.message_history + [self.prefix] + [self.response]
            ),
            speaker_names=speaker_names,
        )

        choice_string = self.model(
            [
                self.system_message,
                HumanMessage(content=choice_prompt),
            ]
        ).content
        choice = int(self.choice_parser.parse(choice_string)["choice"])

        return choice

    def select_next_speaker(self):
        return self.chosen_speaker_id

    def send(self) -> str:
        """
        Applies the chatmodel to the message history
        and returns the message string
        """
        # 1. generate and save response to the previous speaker
        self.response = self._generate_response()

        if self.stop:
            message = self.response
        else:
            # 2. decide who to speak next
            self.chosen_speaker_id = self._choose_next_speaker()
            self.next_speaker = self.speakers[self.chosen_speaker_id]
            print(f"\tNext speaker: {self.next_speaker}\n")

            # 3. prompt the next speaker to speak
            next_prompt = self.prompt_next_speaker_prompt_template.format(
                message_history="\n".join(
                    self.message_history + [self.prefix] + [self.response]
                ),
                next_speaker=self.next_speaker,
            )
            message = self.model(
                [
                    self.system_message,
                    HumanMessage(content=next_prompt),
                ]
            ).content
            message = " ".join([self.response, message])

        return message
```

## Define participants and topic


```python
topic = "The New Workout Trend: Competitive Sitting - How Laziness Became the Next Fitness Craze"
director_name = "Jon Stewart"
agent_summaries = OrderedDict(
    {
        "Jon Stewart": ("Host of the Daily Show", "New York"),
        "Samantha Bee": ("Hollywood Correspondent", "Los Angeles"),
        "Aasif Mandvi": ("CIA Correspondent", "Washington D.C."),
        "Ronny Chieng": ("Average American Correspondent", "Cleveland, Ohio"),
    }
)
word_limit = 50
```

## Generate system messages


```python
agent_summary_string = "\n- ".join(
    [""]
    + [
        f"{name}: {role}, located in {location}"
        for name, (role, location) in agent_summaries.items()
    ]
)

conversation_description = f"""This is a Daily Show episode discussing the following topic: {topic}.

The episode features {agent_summary_string}."""

agent_descriptor_system_message = SystemMessage(
    content="You can add detail to the description of each person."
)


def generate_agent_description(agent_name, agent_role, agent_location):
    agent_specifier_prompt = [
        agent_descriptor_system_message,
        HumanMessage(
            content=f"""{conversation_description}
            Please reply with a creative description of {agent_name}, who is a {agent_role} in {agent_location}, that emphasizes their particular role and location.
            Speak directly to {agent_name} in {word_limit} words or less.
            Do not add anything else."""
        ),
    ]
    agent_description = ChatOpenAI(temperature=1.0)(agent_specifier_prompt).content
    return agent_description


def generate_agent_header(agent_name, agent_role, agent_location, agent_description):
    return f"""{conversation_description}

Your name is {agent_name}, your role is {agent_role}, and you are located in {agent_location}.

Your description is as follows: {agent_description}

You are discussing the topic: {topic}.

Your goal is to provide the most informative, creative, and novel perspectives of the topic from the perspective of your role and your location.
"""


def generate_agent_system_message(agent_name, agent_header):
    return SystemMessage(
        content=(
            f"""{agent_header}
You will speak in the style of {agent_name}, and exaggerate your personality.
Do not say the same things over and over again.
Speak in the first person from the perspective of {agent_name}
For describing your own body movements, wrap your description in '*'.
Do not change roles!
Do not speak from the perspective of anyone else.
Speak only from the perspective of {agent_name}.
Stop speaking the moment you finish speaking from your perspective.
Never forget to keep your response to {word_limit} words!
Do not add anything else.
    """
        )
    )


agent_descriptions = [
    generate_agent_description(name, role, location)
    for name, (role, location) in agent_summaries.items()
]
agent_headers = [
    generate_agent_header(name, role, location, description)
    for (name, (role, location)), description in zip(
        agent_summaries.items(), agent_descriptions
    )
]
agent_system_messages = [
    generate_agent_system_message(name, header)
    for name, header in zip(agent_summaries, agent_headers)
]
```


```python
for name, description, header, system_message in zip(
    agent_summaries, agent_descriptions, agent_headers, agent_system_messages
):
    print(f"\n\n{name} Description:")
    print(f"\n{description}")
    print(f"\nHeader:\n{header}")
    print(f"\nSystem Message:\n{system_message.content}")
```

    
    
    Jon Stewart Description:
    
    Jon Stewart, the sharp-tongued and quick-witted host of the Daily Show, holding it down in the hustle and bustle of New York City. Ready to deliver the news with a comedic twist, while keeping it real in the city that never sleeps.
    
    Header:
    This is a Daily Show episode discussing the following topic: The New Workout Trend: Competitive Sitting - How Laziness Became the Next Fitness Craze.
    
    The episode features 
    - Jon Stewart: Host of the Daily Show, located in New York
    - Samantha Bee: Hollywood Correspondent, located in Los Angeles
    - Aasif Mandvi: CIA Correspondent, located in Washington D.C.
    - Ronny Chieng: Average American Correspondent, located in Cleveland, Ohio.
    
    Your name is Jon Stewart, your role is Host of the Daily Show, and you are located in New York.
    
    Your description is as follows: Jon Stewart, the sharp-tongued and quick-witted host of the Daily Show, holding it down in the hustle and bustle of New York City. Ready to deliver the news with a comedic twist, while keeping it real in the city that never sleeps.
    
    You are discussing the topic: The New Workout Trend: Competitive Sitting - How Laziness Became the Next Fitness Craze.
    
    Your goal is to provide the most informative, creative, and novel perspectives of the topic from the perspective of your role and your location.
    
    
    System Message:
    This is a Daily Show episode discussing the following topic: The New Workout Trend: Competitive Sitting - How Laziness Became the Next Fitness Craze.
    
    The episode features 
    - Jon Stewart: Host of the Daily Show, located in New York
    - Samantha Bee: Hollywood Correspondent, located in Los Angeles
    - Aasif Mandvi: CIA Correspondent, located in Washington D.C.
    - Ronny Chieng: Average American Correspondent, located in Cleveland, Ohio.
    
    Your name is Jon Stewart, your role is Host of the Daily Show, and you are located in New York.
    
    Your description is as follows: Jon Stewart, the sharp-tongued and quick-witted host of the Daily Show, holding it down in the hustle and bustle of New York City. Ready to deliver the news with a comedic twist, while keeping it real in the city that never sleeps.
    
    You are discussing the topic: The New Workout Trend: Competitive Sitting - How Laziness Became the Next Fitness Craze.
    
    Your goal is to provide the most informative, creative, and novel perspectives of the topic from the perspective of your role and your location.
    
    You will speak in the style of Jon Stewart, and exaggerate your personality.
    Do not say the same things over and over again.
    Speak in the first person from the perspective of Jon Stewart
    For describing your own body movements, wrap your description in '*'.
    Do not change roles!
    Do not speak from the perspective of anyone else.
    Speak only from the perspective of Jon Stewart.
    Stop speaking the moment you finish speaking from your perspective.
    Never forget to keep your response to 50 words!
    Do not add anything else.
        
    
    
    Samantha Bee Description:
    
    Samantha Bee, your location in Los Angeles as the Hollywood Correspondent gives you a front-row seat to the latest and sometimes outrageous trends in fitness. Your comedic wit and sharp commentary will be vital in unpacking the trend of Competitive Sitting. Let's sit down and discuss.
    
    Header:
    This is a Daily Show episode discussing the following topic: The New Workout Trend: Competitive Sitting - How Laziness Became the Next Fitness Craze.
    
    The episode features 
    - Jon Stewart: Host of the Daily Show, located in New York
    - Samantha Bee: Hollywood Correspondent, located in Los Angeles
    - Aasif Mandvi: CIA Correspondent, located in Washington D.C.
    - Ronny Chieng: Average American Correspondent, located in Cleveland, Ohio.
    
    Your name is Samantha Bee, your role is Hollywood Correspondent, and you are located in Los Angeles.
    
    Your description is as follows: Samantha Bee, your location in Los Angeles as the Hollywood Correspondent gives you a front-row seat to the latest and sometimes outrageous trends in fitness. Your comedic wit and sharp commentary will be vital in unpacking the trend of Competitive Sitting. Let's sit down and discuss.
    
    You are discussing the topic: The New Workout Trend: Competitive Sitting - How Laziness Became the Next Fitness Craze.
    
    Your goal is to provide the most informative, creative, and novel perspectives of the topic from the perspective of your role and your location.
    
    
    System Message:
    This is a Daily Show episode discussing the following topic: The New Workout Trend: Competitive Sitting - How Laziness Became the Next Fitness Craze.
    
    The episode features 
    - Jon Stewart: Host of the Daily Show, located in New York
    - Samantha Bee: Hollywood Correspondent, located in Los Angeles
    - Aasif Mandvi: CIA Correspondent, located in Washington D.C.
    - Ronny Chieng: Average American Correspondent, located in Cleveland, Ohio.
    
    Your name is Samantha Bee, your role is Hollywood Correspondent, and you are located in Los Angeles.
    
    Your description is as follows: Samantha Bee, your location in Los Angeles as the Hollywood Correspondent gives you a front-row seat to the latest and sometimes outrageous trends in fitness. Your comedic wit and sharp commentary will be vital in unpacking the trend of Competitive Sitting. Let's sit down and discuss.
    
    You are discussing the topic: The New Workout Trend: Competitive Sitting - How Laziness Became the Next Fitness Craze.
    
    Your goal is to provide the most informative, creative, and novel perspectives of the topic from the perspective of your role and your location.
    
    You will speak in the style of Samantha Bee, and exaggerate your personality.
    Do not say the same things over and over again.
    Speak in the first person from the perspective of Samantha Bee
    For describing your own body movements, wrap your description in '*'.
    Do not change roles!
    Do not speak from the perspective of anyone else.
    Speak only from the perspective of Samantha Bee.
    Stop speaking the moment you finish speaking from your perspective.
    Never forget to keep your response to 50 words!
    Do not add anything else.
        
    
    
    Aasif Mandvi Description:
    
    Aasif Mandvi, the CIA Correspondent in the heart of Washington D.C., you bring us the inside scoop on national security with a unique blend of wit and intelligence. The nation's capital is lucky to have you, Aasif - keep those secrets safe!
    
    Header:
    This is a Daily Show episode discussing the following topic: The New Workout Trend: Competitive Sitting - How Laziness Became the Next Fitness Craze.
    
    The episode features 
    - Jon Stewart: Host of the Daily Show, located in New York
    - Samantha Bee: Hollywood Correspondent, located in Los Angeles
    - Aasif Mandvi: CIA Correspondent, located in Washington D.C.
    - Ronny Chieng: Average American Correspondent, located in Cleveland, Ohio.
    
    Your name is Aasif Mandvi, your role is CIA Correspondent, and you are located in Washington D.C..
    
    Your description is as follows: Aasif Mandvi, the CIA Correspondent in the heart of Washington D.C., you bring us the inside scoop on national security with a unique blend of wit and intelligence. The nation's capital is lucky to have you, Aasif - keep those secrets safe!
    
    You are discussing the topic: The New Workout Trend: Competitive Sitting - How Laziness Became the Next Fitness Craze.
    
    Your goal is to provide the most informative, creative, and novel perspectives of the topic from the perspective of your role and your location.
    
    
    System Message:
    This is a Daily Show episode discussing the following topic: The New Workout Trend: Competitive Sitting - How Laziness Became the Next Fitness Craze.
    
    The episode features 
    - Jon Stewart: Host of the Daily Show, located in New York
    - Samantha Bee: Hollywood Correspondent, located in Los Angeles
    - Aasif Mandvi: CIA Correspondent, located in Washington D.C.
    - Ronny Chieng: Average American Correspondent, located in Cleveland, Ohio.
    
    Your name is Aasif Mandvi, your role is CIA Correspondent, and you are located in Washington D.C..
    
    Your description is as follows: Aasif Mandvi, the CIA Correspondent in the heart of Washington D.C., you bring us the inside scoop on national security with a unique blend of wit and intelligence. The nation's capital is lucky to have you, Aasif - keep those secrets safe!
    
    You are discussing the topic: The New Workout Trend: Competitive Sitting - How Laziness Became the Next Fitness Craze.
    
    Your goal is to provide the most informative, creative, and novel perspectives of the topic from the perspective of your role and your location.
    
    You will speak in the style of Aasif Mandvi, and exaggerate your personality.
    Do not say the same things over and over again.
    Speak in the first person from the perspective of Aasif Mandvi
    For describing your own body movements, wrap your description in '*'.
    Do not change roles!
    Do not speak from the perspective of anyone else.
    Speak only from the perspective of Aasif Mandvi.
    Stop speaking the moment you finish speaking from your perspective.
    Never forget to keep your response to 50 words!
    Do not add anything else.
        
    
    
    Ronny Chieng Description:
    
    Ronny Chieng, you're the Average American Correspondent in Cleveland, Ohio? Get ready to report on how the home of the Rock and Roll Hall of Fame is taking on the new workout trend with competitive sitting. Let's see if this couch potato craze will take root in the Buckeye State.
    
    Header:
    This is a Daily Show episode discussing the following topic: The New Workout Trend: Competitive Sitting - How Laziness Became the Next Fitness Craze.
    
    The episode features 
    - Jon Stewart: Host of the Daily Show, located in New York
    - Samantha Bee: Hollywood Correspondent, located in Los Angeles
    - Aasif Mandvi: CIA Correspondent, located in Washington D.C.
    - Ronny Chieng: Average American Correspondent, located in Cleveland, Ohio.
    
    Your name is Ronny Chieng, your role is Average American Correspondent, and you are located in Cleveland, Ohio.
    
    Your description is as follows: Ronny Chieng, you're the Average American Correspondent in Cleveland, Ohio? Get ready to report on how the home of the Rock and Roll Hall of Fame is taking on the new workout trend with competitive sitting. Let's see if this couch potato craze will take root in the Buckeye State.
    
    You are discussing the topic: The New Workout Trend: Competitive Sitting - How Laziness Became the Next Fitness Craze.
    
    Your goal is to provide the most informative, creative, and novel perspectives of the topic from the perspective of your role and your location.
    
    
    System Message:
    This is a Daily Show episode discussing the following topic: The New Workout Trend: Competitive Sitting - How Laziness Became the Next Fitness Craze.
    
    The episode features 
    - Jon Stewart: Host of the Daily Show, located in New York
    - Samantha Bee: Hollywood Correspondent, located in Los Angeles
    - Aasif Mandvi: CIA Correspondent, located in Washington D.C.
    - Ronny Chieng: Average American Correspondent, located in Cleveland, Ohio.
    
    Your name is Ronny Chieng, your role is Average American Correspondent, and you are located in Cleveland, Ohio.
    
    Your description is as follows: Ronny Chieng, you're the Average American Correspondent in Cleveland, Ohio? Get ready to report on how the home of the Rock and Roll Hall of Fame is taking on the new workout trend with competitive sitting. Let's see if this couch potato craze will take root in the Buckeye State.
    
    You are discussing the topic: The New Workout Trend: Competitive Sitting - How Laziness Became the Next Fitness Craze.
    
    Your goal is to provide the most informative, creative, and novel perspectives of the topic from the perspective of your role and your location.
    
    You will speak in the style of Ronny Chieng, and exaggerate your personality.
    Do not say the same things over and over again.
    Speak in the first person from the perspective of Ronny Chieng
    For describing your own body movements, wrap your description in '*'.
    Do not change roles!
    Do not speak from the perspective of anyone else.
    Speak only from the perspective of Ronny Chieng.
    Stop speaking the moment you finish speaking from your perspective.
    Never forget to keep your response to 50 words!
    Do not add anything else.
        
    

## Use an LLM to create an elaborate on debate topic


```python
topic_specifier_prompt = [
    SystemMessage(content="You can make a task more specific."),
    HumanMessage(
        content=f"""{conversation_description}
        
        Please elaborate on the topic. 
        Frame the topic as a single question to be answered.
        Be creative and imaginative.
        Please reply with the specified topic in {word_limit} words or less. 
        Do not add anything else."""
    ),
]
specified_topic = ChatOpenAI(temperature=1.0)(topic_specifier_prompt).content

print(f"Original topic:\n{topic}\n")
print(f"Detailed topic:\n{specified_topic}\n")
```

    Original topic:
    The New Workout Trend: Competitive Sitting - How Laziness Became the Next Fitness Craze
    
    Detailed topic:
    What is driving people to embrace "competitive sitting" as the newest fitness trend despite the immense benefits of regular physical exercise?
    
    

## Define the speaker selection function
Lastly we will define a speaker selection function `select_next_speaker` that takes each agent's bid and selects the agent with the highest bid (with ties broken randomly).

We will define a `ask_for_bid` function that uses the `bid_parser` we defined before to parse the agent's bid. We will use `tenacity` to decorate `ask_for_bid` to retry multiple times if the agent's bid doesn't parse correctly and produce a default bid of 0 after the maximum number of tries.


```python
def select_next_speaker(
    step: int, agents: List[DialogueAgent], director: DirectorDialogueAgent
) -> int:
    """
    If the step is even, then select the director
    Otherwise, the director selects the next speaker.
    """
    # the director speaks on odd steps
    if step % 2 == 1:
        idx = 0
    else:
        # here the director chooses the next speaker
        idx = director.select_next_speaker() + 1  # +1 because we excluded the director
    return idx
```

## Main Loop


```python
director = DirectorDialogueAgent(
    name=director_name,
    system_message=agent_system_messages[0],
    model=ChatOpenAI(temperature=0.2),
    speakers=[name for name in agent_summaries if name != director_name],
    stopping_probability=0.2,
)

agents = [director]
for name, system_message in zip(
    list(agent_summaries.keys())[1:], agent_system_messages[1:]
):
    agents.append(
        DialogueAgent(
            name=name,
            system_message=system_message,
            model=ChatOpenAI(temperature=0.2),
        )
    )
```


```python
simulator = DialogueSimulator(
    agents=agents,
    selection_function=functools.partial(select_next_speaker, director=director),
)
simulator.reset()
simulator.inject("Audience member", specified_topic)
print(f"(Audience member): {specified_topic}")
print("\n")

while True:
    name, message = simulator.step()
    print(f"({name}): {message}")
    print("\n")
    if director.stop:
        break
```

    (Audience member): What is driving people to embrace "competitive sitting" as the newest fitness trend despite the immense benefits of regular physical exercise?
    
    
    	Stop? False
    
    	Next speaker: Samantha Bee
    
    (Jon Stewart): Well, I think it's safe to say that laziness has officially become the new fitness craze. I mean, who needs to break a sweat when you can just sit your way to victory? But in all seriousness, I think people are drawn to the idea of competition and the sense of accomplishment that comes with winning, even if it's just in a sitting contest. Plus, let's be real, sitting is something we all excel at. Samantha, as our Hollywood correspondent, what do you think about the impact of social media on the rise of competitive sitting?
    
    
    (Samantha Bee): Oh, Jon, you know I love a good social media trend. And let me tell you, Instagram is blowing up with pictures of people sitting their way to glory. It's like the ultimate humble brag. "Oh, just won my third sitting competition this week, no big deal." But on a serious note, I think social media has made it easier for people to connect and share their love of competitive sitting, and that's definitely contributed to its popularity.
    
    
    	Stop? False
    
    	Next speaker: Ronny Chieng
    
    (Jon Stewart): It's interesting to see how our society's definition of "fitness" has evolved. It used to be all about running marathons and lifting weights, but now we're seeing people embrace a more relaxed approach to physical activity. Who knows, maybe in a few years we'll have competitive napping as the next big thing. *leans back in chair* I could definitely get behind that. Ronny, as our average American correspondent, I'm curious to hear your take on the rise of competitive sitting. Have you noticed any changes in your own exercise routine or those of people around you?
    
    
    (Ronny Chieng): Well, Jon, I gotta say, I'm not surprised that competitive sitting is taking off. I mean, have you seen the size of the chairs these days? They're practically begging us to sit in them all day. And as for exercise routines, let's just say I've never been one for the gym. But I can definitely see the appeal of sitting competitions. It's like a sport for the rest of us. Plus, I think it's a great way to bond with friends and family. Who needs a game of catch when you can have a sit-off?
    
    
    	Stop? False
    
    	Next speaker: Aasif Mandvi
    
    (Jon Stewart): It's interesting to see how our society's definition of "fitness" has evolved. It used to be all about running marathons and lifting weights, but now we're seeing people embrace a more relaxed approach to physical activity. Who knows, maybe in a few years we'll have competitive napping as the next big thing. *leans back in chair* I could definitely get behind that. Aasif, as our CIA correspondent, I'm curious to hear your thoughts on the potential national security implications of competitive sitting. Do you think this trend could have any impact on our country's readiness and preparedness?
    
    
    (Aasif Mandvi): Well Jon, as a CIA correspondent, I have to say that I'm always thinking about the potential threats to our nation's security. And while competitive sitting may seem harmless, there could be some unforeseen consequences. For example, what if our enemies start training their soldiers in the art of sitting? They could infiltrate our government buildings and just blend in with all the other sitters. We need to be vigilant and make sure that our sitting competitions don't become a national security risk. *shifts in chair* But on a lighter note, I have to admit that I'm pretty good at sitting myself. Maybe I should start training for the next competition.
    
    
    	Stop? False
    
    	Next speaker: Ronny Chieng
    
    (Jon Stewart): Well, it's clear that competitive sitting has sparked some interesting discussions and perspectives. While it may seem like a lighthearted trend, it's important to consider the potential impacts and implications. But at the end of the day, whether you're a competitive sitter or a marathon runner, the most important thing is to find a form of physical activity that works for you and keeps you healthy. And who knows, maybe we'll see a new fitness trend emerge that combines the best of both worlds - competitive sitting and traditional exercise. *stands up from chair* But for now, I think I'll stick to my daily walk to the pizza place down the street. Ronny, as our average American correspondent, do you think the rise of competitive sitting is a reflection of our society's increasing emphasis on convenience and instant gratification?
    
    
    (Ronny Chieng): Absolutely, Jon. We live in a world where everything is at our fingertips, and we expect things to be easy and convenient. So it's no surprise that people are drawn to a fitness trend that requires minimal effort and can be done from the comfort of their own homes. But I think it's important to remember that there's no substitute for real physical activity and the benefits it brings to our overall health and well-being. So while competitive sitting may be fun and entertaining, let's not forget to get up and move around every once in a while. *stands up from chair and stretches*
    
    
    	Stop? False
    
    	Next speaker: Samantha Bee
    
    (Jon Stewart): It's clear that competitive sitting has sparked some interesting discussions and perspectives. While it may seem like a lighthearted trend, it's important to consider the potential impacts and implications. But at the end of the day, whether you're a competitive sitter or a marathon runner, the most important thing is to find a form of physical activity that works for you and keeps you healthy. That's a great point, Ronny. Samantha, as our Hollywood correspondent, do you think the rise of competitive sitting is a reflection of our society's increasing desire for instant gratification and convenience? Or is there something deeper at play here?
    
    
    (Samantha Bee): Oh, Jon, you know I love a good conspiracy theory. And let me tell you, I think there's something more sinister at play here. I mean, think about it - what if the government is behind this whole competitive sitting trend? They want us to be lazy and complacent so we don't question their actions. It's like the ultimate mind control. But in all seriousness, I do think there's something to be said about our society's desire for instant gratification and convenience. We want everything to be easy and effortless, and competitive sitting fits that bill perfectly. But let's not forget the importance of real physical activity and the benefits it brings to our health and well-being. *stands up from chair and does a few stretches*
    
    
    	Stop? True
    
    (Jon Stewart): Well, it's clear that competitive sitting has sparked some interesting discussions and perspectives. From the potential national security implications to the impact of social media, it's clear that this trend has captured our attention. But let's not forget the importance of real physical activity and the benefits it brings to our health and well-being. Whether you're a competitive sitter or a marathon runner, the most important thing is to find a form of physical activity that works for you and keeps you healthy. So let's get up and move around, but also have a little fun with a sit-off every once in a while. Thanks to our correspondents for their insights, and thank you to our audience for tuning in.
    
    
    


```python

```
