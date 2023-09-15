# Generative Agents in LangChain

This notebook implements a generative agent based on the paper [Generative Agents: Interactive Simulacra of Human Behavior](https://arxiv.org/abs/2304.03442) by Park, et. al.

In it, we leverage a time-weighted Memory object backed by a LangChain Retriever.


```python
# Use termcolor to make it easy to colorize the outputs.
!pip install termcolor > /dev/null
```


```python
import logging

logging.basicConfig(level=logging.ERROR)
```


```python
from datetime import datetime, timedelta
from typing import List
from termcolor import colored


from langchain.chat_models import ChatOpenAI
from langchain.docstore import InMemoryDocstore
from langchain.embeddings import OpenAIEmbeddings
from langchain.retrievers import TimeWeightedVectorStoreRetriever
from langchain.vectorstores import FAISS
```


```python
USER_NAME = "Person A"  # The name you want to use when interviewing the agent.
LLM = ChatOpenAI(max_tokens=1500)  # Can be any LLM you want.
```

### Generative Agent Memory Components

This tutorial highlights the memory of generative agents and its impact on their behavior. The memory varies from standard LangChain Chat memory in two aspects:

1. **Memory Formation**

   Generative Agents have extended memories, stored in a single stream:
      1. Observations - from dialogues or interactions with the virtual world, about self or others
      2. Reflections - resurfaced and summarized core memories


2. **Memory Recall**

   Memories are retrieved using a weighted sum of salience, recency, and importance.

You can review the definitions of the `GenerativeAgent` and `GenerativeAgentMemory` in the [reference documentation]("../../reference/modules/experimental") for the following imports, focusing on `add_memory` and `summarize_related_memories` methods.


```python
from langchain.experimental.generative_agents import (
    GenerativeAgent,
    GenerativeAgentMemory,
)
```

## Memory Lifecycle

Summarizing the key methods in the above: `add_memory` and `summarize_related_memories`.

When an agent makes an observation, it stores the memory:
    
1. Language model scores the memory's importance (1 for mundane, 10 for poignant)
2. Observation and importance are stored within a document by TimeWeightedVectorStoreRetriever, with a `last_accessed_time`.

When an agent responds to an observation:

1. Generates query(s) for retriever, which fetches documents based on salience, recency, and importance.
2. Summarizes the retrieved information
3. Updates the `last_accessed_time` for the used documents.


## Create a Generative Character



Now that we've walked through the definition, we will create two characters named "Tommie" and "Eve".


```python
import math
import faiss


def relevance_score_fn(score: float) -> float:
    """Return a similarity score on a scale [0, 1]."""
    # This will differ depending on a few things:
    # - the distance / similarity metric used by the VectorStore
    # - the scale of your embeddings (OpenAI's are unit norm. Many others are not!)
    # This function converts the euclidean norm of normalized embeddings
    # (0 is most similar, sqrt(2) most dissimilar)
    # to a similarity function (0 to 1)
    return 1.0 - score / math.sqrt(2)


def create_new_memory_retriever():
    """Create a new vector store retriever unique to the agent."""
    # Define your embedding model
    embeddings_model = OpenAIEmbeddings()
    # Initialize the vectorstore as empty
    embedding_size = 1536
    index = faiss.IndexFlatL2(embedding_size)
    vectorstore = FAISS(
        embeddings_model.embed_query,
        index,
        InMemoryDocstore({}),
        {},
        relevance_score_fn=relevance_score_fn,
    )
    return TimeWeightedVectorStoreRetriever(
        vectorstore=vectorstore, other_score_keys=["importance"], k=15
    )
```


```python
tommies_memory = GenerativeAgentMemory(
    llm=LLM,
    memory_retriever=create_new_memory_retriever(),
    verbose=False,
    reflection_threshold=8,  # we will give this a relatively low number to show how reflection works
)

tommie = GenerativeAgent(
    name="Tommie",
    age=25,
    traits="anxious, likes design, talkative",  # You can add more persistent traits here
    status="looking for a job",  # When connected to a virtual world, we can have the characters update their status
    memory_retriever=create_new_memory_retriever(),
    llm=LLM,
    memory=tommies_memory,
)
```


```python
# The current "Summary" of a character can't be made because the agent hasn't made
# any observations yet.
print(tommie.get_summary())
```

    Name: Tommie (age: 25)
    Innate traits: anxious, likes design, talkative
    No information about Tommie's core characteristics is provided in the given statements.
    


```python
# We can add memories directly to the memory object
tommie_observations = [
    "Tommie remembers his dog, Bruno, from when he was a kid",
    "Tommie feels tired from driving so far",
    "Tommie sees the new home",
    "The new neighbors have a cat",
    "The road is noisy at night",
    "Tommie is hungry",
    "Tommie tries to get some rest.",
]
for observation in tommie_observations:
    tommie.memory.add_memory(observation)
```


```python
# Now that Tommie has 'memories', their self-summary is more descriptive, though still rudimentary.
# We will see how this summary updates after more observations to create a more rich description.
print(tommie.get_summary(force_refresh=True))
```

    Name: Tommie (age: 25)
    Innate traits: anxious, likes design, talkative
    Tommie is a person who is observant of his surroundings, has a sentimental side, and experiences basic human needs such as hunger and the need for rest. He also tends to get tired easily and is affected by external factors such as noise from the road or a neighbor's pet.
    

## Pre-Interview with Character

Before sending our character on their way, let's ask them a few questions.


```python
def interview_agent(agent: GenerativeAgent, message: str) -> str:
    """Help the notebook user interact with the agent."""
    new_message = f"{USER_NAME} says {message}"
    return agent.generate_dialogue_response(new_message)[1]
```


```python
interview_agent(tommie, "What do you like to do?")
```




    'Tommie said "I really enjoy design and being creative. I\'ve been working on some personal projects lately. What about you, Person A? What do you like to do?"'




```python
interview_agent(tommie, "What are you looking forward to doing today?")
```




    'Tommie said "Well, I\'m actually looking for a job right now, so hopefully I can find some job postings online and start applying. How about you, Person A? What\'s on your schedule for today?"'




```python
interview_agent(tommie, "What are you most worried about today?")
```




    'Tommie said "Honestly, I\'m feeling pretty anxious about finding a job. It\'s been a bit of a struggle lately, but I\'m trying to stay positive and keep searching. How about you, Person A? What worries you?"'



## Step through the day's observations.


```python
# Let's have Tommie start going through a day in the life.
observations = [
    "Tommie wakes up to the sound of a noisy construction site outside his window.",
    "Tommie gets out of bed and heads to the kitchen to make himself some coffee.",
    "Tommie realizes he forgot to buy coffee filters and starts rummaging through his moving boxes to find some.",
    "Tommie finally finds the filters and makes himself a cup of coffee.",
    "The coffee tastes bitter, and Tommie regrets not buying a better brand.",
    "Tommie checks his email and sees that he has no job offers yet.",
    "Tommie spends some time updating his resume and cover letter.",
    "Tommie heads out to explore the city and look for job openings.",
    "Tommie sees a sign for a job fair and decides to attend.",
    "The line to get in is long, and Tommie has to wait for an hour.",
    "Tommie meets several potential employers at the job fair but doesn't receive any offers.",
    "Tommie leaves the job fair feeling disappointed.",
    "Tommie stops by a local diner to grab some lunch.",
    "The service is slow, and Tommie has to wait for 30 minutes to get his food.",
    "Tommie overhears a conversation at the next table about a job opening.",
    "Tommie asks the diners about the job opening and gets some information about the company.",
    "Tommie decides to apply for the job and sends his resume and cover letter.",
    "Tommie continues his search for job openings and drops off his resume at several local businesses.",
    "Tommie takes a break from his job search to go for a walk in a nearby park.",
    "A dog approaches and licks Tommie's feet, and he pets it for a few minutes.",
    "Tommie sees a group of people playing frisbee and decides to join in.",
    "Tommie has fun playing frisbee but gets hit in the face with the frisbee and hurts his nose.",
    "Tommie goes back to his apartment to rest for a bit.",
    "A raccoon tore open the trash bag outside his apartment, and the garbage is all over the floor.",
    "Tommie starts to feel frustrated with his job search.",
    "Tommie calls his best friend to vent about his struggles.",
    "Tommie's friend offers some words of encouragement and tells him to keep trying.",
    "Tommie feels slightly better after talking to his friend.",
]
```


```python
# Let's send Tommie on their way. We'll check in on their summary every few observations to watch it evolve
for i, observation in enumerate(observations):
    _, reaction = tommie.generate_reaction(observation)
    print(colored(observation, "green"), reaction)
    if ((i + 1) % 20) == 0:
        print("*" * 40)
        print(
            colored(
                f"After {i+1} observations, Tommie's summary is:\n{tommie.get_summary(force_refresh=True)}",
                "blue",
            )
        )
        print("*" * 40)
```

    [32mTommie wakes up to the sound of a noisy construction site outside his window.[0m Tommie groans and covers his head with a pillow, trying to block out the noise.
    [32mTommie gets out of bed and heads to the kitchen to make himself some coffee.[0m Tommie stretches his arms and yawns before starting to make the coffee.
    [32mTommie realizes he forgot to buy coffee filters and starts rummaging through his moving boxes to find some.[0m Tommie sighs in frustration and continues searching through the boxes.
    [32mTommie finally finds the filters and makes himself a cup of coffee.[0m Tommie takes a deep breath and enjoys the aroma of the fresh coffee.
    [32mThe coffee tastes bitter, and Tommie regrets not buying a better brand.[0m Tommie grimaces and sets the coffee mug aside.
    [32mTommie checks his email and sees that he has no job offers yet.[0m Tommie sighs and closes his laptop, feeling discouraged.
    [32mTommie spends some time updating his resume and cover letter.[0m Tommie nods, feeling satisfied with his progress.
    [32mTommie heads out to explore the city and look for job openings.[0m Tommie feels a surge of excitement and anticipation as he steps out into the city.
    [32mTommie sees a sign for a job fair and decides to attend.[0m Tommie feels hopeful and excited about the possibility of finding job opportunities at the job fair.
    [32mThe line to get in is long, and Tommie has to wait for an hour.[0m Tommie taps his foot impatiently and checks his phone for the time.
    [32mTommie meets several potential employers at the job fair but doesn't receive any offers.[0m Tommie feels disappointed and discouraged, but he remains determined to keep searching for job opportunities.
    [32mTommie leaves the job fair feeling disappointed.[0m Tommie feels disappointed and discouraged, but he remains determined to keep searching for job opportunities.
    [32mTommie stops by a local diner to grab some lunch.[0m Tommie feels relieved to take a break and satisfy his hunger.
    [32mThe service is slow, and Tommie has to wait for 30 minutes to get his food.[0m Tommie feels frustrated and impatient due to the slow service.
    [32mTommie overhears a conversation at the next table about a job opening.[0m Tommie feels a surge of hope and excitement at the possibility of a job opportunity but decides not to interfere with the conversation at the next table.
    [32mTommie asks the diners about the job opening and gets some information about the company.[0m Tommie said "Excuse me, I couldn't help but overhear your conversation about the job opening. Could you give me some more information about the company?"
    [32mTommie decides to apply for the job and sends his resume and cover letter.[0m Tommie feels hopeful and proud of himself for taking action towards finding a job.
    [32mTommie continues his search for job openings and drops off his resume at several local businesses.[0m Tommie feels hopeful and determined to keep searching for job opportunities.
    [32mTommie takes a break from his job search to go for a walk in a nearby park.[0m Tommie feels refreshed and rejuvenated after taking a break in the park.
    [32mA dog approaches and licks Tommie's feet, and he pets it for a few minutes.[0m Tommie feels happy and enjoys the brief interaction with the dog.
    ****************************************
    [34mAfter 20 observations, Tommie's summary is:
    Name: Tommie (age: 25)
    Innate traits: anxious, likes design, talkative
    Tommie is determined and hopeful in his search for job opportunities, despite encountering setbacks and disappointments. He is also able to take breaks and care for his physical needs, such as getting rest and satisfying his hunger. Tommie is nostalgic towards his past, as shown by his memory of his childhood dog. Overall, Tommie is a hardworking and resilient individual who remains focused on his goals.[0m
    ****************************************
    [32mTommie sees a group of people playing frisbee and decides to join in.[0m Do nothing.
    [32mTommie has fun playing frisbee but gets hit in the face with the frisbee and hurts his nose.[0m Tommie feels pain and puts a hand to his nose to check for any injury.
    [32mTommie goes back to his apartment to rest for a bit.[0m Tommie feels relieved to take a break and rest for a bit.
    [32mA raccoon tore open the trash bag outside his apartment, and the garbage is all over the floor.[0m Tommie feels annoyed and frustrated at the mess caused by the raccoon.
    [32mTommie starts to feel frustrated with his job search.[0m Tommie feels discouraged but remains determined to keep searching for job opportunities.
    [32mTommie calls his best friend to vent about his struggles.[0m Tommie said "Hey, can I talk to you for a bit? I'm feeling really frustrated with my job search."
    [32mTommie's friend offers some words of encouragement and tells him to keep trying.[0m Tommie said "Thank you, I really appreciate your support and encouragement."
    [32mTommie feels slightly better after talking to his friend.[0m Tommie feels grateful for his friend's support.
    

## Interview after the day


```python
interview_agent(tommie, "Tell me about how your day has been going")
```




    'Tommie said "It\'s been a bit of a rollercoaster, to be honest. I\'ve had some setbacks in my job search, but I also had some good moments today, like sending out a few resumes and meeting some potential employers at a job fair. How about you?"'




```python
interview_agent(tommie, "How do you feel about coffee?")
```




    'Tommie said "I really enjoy coffee, but sometimes I regret not buying a better brand. How about you?"'




```python
interview_agent(tommie, "Tell me about your childhood dog!")
```




    'Tommie said "Oh, I had a dog named Bruno when I was a kid. He was a golden retriever and my best friend. I have so many fond memories of him."'



## Adding Multiple Characters

Let's add a second character to have a conversation with Tommie. Feel free to configure different traits.


```python
eves_memory = GenerativeAgentMemory(
    llm=LLM,
    memory_retriever=create_new_memory_retriever(),
    verbose=False,
    reflection_threshold=5,
)


eve = GenerativeAgent(
    name="Eve",
    age=34,
    traits="curious, helpful",  # You can add more persistent traits here
    status="N/A",  # When connected to a virtual world, we can have the characters update their status
    llm=LLM,
    daily_summaries=[
        (
            "Eve started her new job as a career counselor last week and received her first assignment, a client named Tommie."
        )
    ],
    memory=eves_memory,
    verbose=False,
)
```


```python
yesterday = (datetime.now() - timedelta(days=1)).strftime("%A %B %d")
eve_observations = [
    "Eve wakes up and hear's the alarm",
    "Eve eats a boal of porridge",
    "Eve helps a coworker on a task",
    "Eve plays tennis with her friend Xu before going to work",
    "Eve overhears her colleague say something about Tommie being hard to work with",
]
for observation in eve_observations:
    eve.memory.add_memory(observation)
```


```python
print(eve.get_summary())
```

    Name: Eve (age: 34)
    Innate traits: curious, helpful
    Eve is a helpful and active person who enjoys sports and takes care of her physical health. She is attentive to her surroundings, including her colleagues, and has good time management skills.
    

## Pre-conversation interviews


Let's "Interview" Eve before she speaks with Tommie.


```python
interview_agent(eve, "How are you feeling about today?")
```




    'Eve said "I\'m feeling pretty good, thanks for asking! Just trying to stay productive and make the most of the day. How about you?"'




```python
interview_agent(eve, "What do you know about Tommie?")
```




    'Eve said "I don\'t know much about Tommie, but I heard someone mention that they find them difficult to work with. Have you had any experiences working with Tommie?"'




```python
interview_agent(
    eve,
    "Tommie is looking to find a job. What are are some things you'd like to ask him?",
)
```




    'Eve said "That\'s interesting. I don\'t know much about Tommie\'s work experience, but I would probably ask about his strengths and areas for improvement. What about you?"'




```python
interview_agent(
    eve,
    "You'll have to ask him. He may be a bit anxious, so I'd appreciate it if you keep the conversation going and ask as many questions as possible.",
)
```




    'Eve said "Sure, I can keep the conversation going and ask plenty of questions. I want to make sure Tommie feels comfortable and supported. Thanks for letting me know."'



## Dialogue between Generative Agents

Generative agents are much more complex when they interact with a virtual environment or with each other. Below, we run a simple conversation between Tommie and Eve.


```python
def run_conversation(agents: List[GenerativeAgent], initial_observation: str) -> None:
    """Runs a conversation between agents."""
    _, observation = agents[1].generate_reaction(initial_observation)
    print(observation)
    turns = 0
    while True:
        break_dialogue = False
        for agent in agents:
            stay_in_dialogue, observation = agent.generate_dialogue_response(
                observation
            )
            print(observation)
            # observation = f"{agent.name} said {reaction}"
            if not stay_in_dialogue:
                break_dialogue = True
        if break_dialogue:
            break
        turns += 1
```


```python
agents = [tommie, eve]
run_conversation(
    agents,
    "Tommie said: Hi, Eve. Thanks for agreeing to meet with me today. I have a bunch of questions and am not sure where to start. Maybe you could first share about your experience?",
)
```

    Eve said "Sure, Tommie. I'd be happy to share about my experience. Where would you like me to start?"
    Tommie said "That's great, thank you! How about you start by telling me about your previous work experience?"
    Eve said "Sure, I'd be happy to share my previous work experience with you. I've worked in a few different industries, including marketing and event planning. What specific questions do you have for me?"
    Tommie said "That's great to hear. Can you tell me more about your experience in event planning? I've always been interested in that field."
    Eve said "Sure, I'd be happy to share about my experience in event planning. I've worked on a variety of events, from corporate conferences to weddings. One of the biggest challenges I faced was managing multiple vendors and ensuring everything ran smoothly on the day of the event. What specific questions do you have?"
    Tommie said "That sounds like a lot of responsibility! Can you tell me more about how you handled the challenges that came up during those events?"
    Eve said "Sure, Tommie. I'd be happy to share with you how I handled those challenges. One approach that worked well for me was to stay organized and create a detailed timeline for the event. This helped me keep track of all the different tasks that needed to be done and when they needed to be completed. I also made sure to communicate clearly with all the vendors and team members involved in the event to ensure everyone was on the same page. Would you like me to go into more detail?"
    Tommie said "Thank you for sharing that with me, Eve. That sounds like a great approach to managing events. Can you tell me more about how you handled any unexpected issues that came up during the events?"
    Eve said "Of course, Tommie. One example of an unexpected issue I faced was when one of the vendors didn't show up on time. To handle this, I quickly contacted a backup vendor and was able to get everything back on track. It's always important to have a backup plan in case things don't go as planned. Do you have any other questions about event planning?"
    Tommie said "Thank you for sharing that with me, Eve. It's really helpful to hear how you handled unexpected issues like that. Can you give me an example of how you communicated with your team to ensure everyone was on the same page during an event?"
    Eve said "Sure, Tommie. One thing I did to ensure everyone was on the same page was to have regular check-ins and meetings with the team leading up to the event. This helped us address any issues or concerns early on and make sure everyone was clear on their roles and responsibilities. Have you ever had to manage a team for an event before?"
    Tommie said "That's a great idea, Eve. I haven't had the opportunity to manage a team for an event yet, but I'll definitely keep that in mind for the future. Thank you for sharing your experience with me."
    Eve said "Thanks for the opportunity to share my experience, Tommie. It was great meeting with you today."
    

## Let's interview our agents after their conversation

Since the generative agents retain their memories from the day, we can ask them about their plans, conversations, and other memoreis.


```python
# We can see a current "Summary" of a character based on their own perception of self
# has changed
print(tommie.get_summary(force_refresh=True))
```

    Name: Tommie (age: 25)
    Innate traits: anxious, likes design, talkative
    Tommie is determined and hopeful in his job search, but can also feel discouraged and frustrated at times. He has a strong connection to his childhood dog, Bruno. Tommie seeks support from his friends when feeling overwhelmed and is grateful for their help. He also enjoys exploring his new city.
    


```python
print(eve.get_summary(force_refresh=True))
```

    Name: Eve (age: 34)
    Innate traits: curious, helpful
    Eve is a helpful and friendly person who enjoys playing sports and staying productive. She is attentive and responsive to others' needs, actively listening and asking questions to understand their perspectives. Eve has experience in event planning and communication, and is willing to share her knowledge and expertise with others. She values teamwork and collaboration, and strives to create a comfortable and supportive environment for everyone.
    


```python
interview_agent(tommie, "How was your conversation with Eve?")
```




    'Tommie said "It was really helpful actually. Eve shared some great tips on managing events and handling unexpected issues. I feel like I learned a lot from her experience."'




```python
interview_agent(eve, "How was your conversation with Tommie?")
```




    'Eve said "It was great, thanks for asking. Tommie was very receptive and had some great questions about event planning. How about you, have you had any interactions with Tommie?"'




```python
interview_agent(eve, "What do you wish you would have said to Tommie?")
```




    'Eve said "It was great meeting with you, Tommie. If you have any more questions or need any help in the future, don\'t hesitate to reach out to me. Have a great day!"'


