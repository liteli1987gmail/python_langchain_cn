# 如何创建自定义的记忆类

尽管在LangChain中提供了几种预定义的记忆类型，但您很可能会想要添加自己的记忆类型，以便优化您的应用。本笔记本将介绍如何实现这一点。

对于本笔记本，我们将向`ConversationChain`添加一个自定义的记忆类型。为了添加一个自定义的记忆类，我们需要导入基本的记忆类并派生它。

```python
from langchain import OpenAI, ConversationChain
from langchain.schema import BaseMemory
from pydantic import BaseModel
from typing import List, Dict, Any
```

在这个例子中，我们将编写一个自定义的记忆类，它使用spacy来提取实体，并将有关这些实体的信息保存在一个简单的哈希表中。然后，在对话期间，我们将查看输入文本，提取任何实体，并将实体的任何信息放入上下文中。

* 请注意，这个实现非常简单且容易出错，可能在实际生产场景中没有用处。它的目的是展示您可以添加自定义的记忆实现。

为此，我们需要安装spacy。


```python
# !pip install spacy
# !python -m spacy download en_core_web_lg
```


```python
import spacy

nlp = spacy.load("en_core_web_lg")
```


```python
class SpacyEntityMemory(BaseMemory, BaseModel):
    """Memory class for storing information about entities."""

    # Define dictionary to store information about entities.
    entities: dict = {}
    # Define key to pass information about entities into prompt.
    memory_key: str = "entities"

    def clear(self):
        self.entities = {}

    @property
    def memory_variables(self) -> List[str]:
        """Define the variables we are providing to the prompt."""
        return [self.memory_key]

    def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, str]:
        """Load the memory variables, in this case the entity key."""
        # Get the input text and run through spacy
        doc = nlp(inputs[list(inputs.keys())[0]])
        # Extract known information about entities, if they exist.
        entities = [
            self.entities[str(ent)] for ent in doc.ents if str(ent) in self.entities
        ]
        # Return combined information about entities to put into context.
        return {self.memory_key: "\n".join(entities)}

    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, str]) -> None:
        """Save context from this conversation to buffer."""
        # Get the input text and run through spacy
        text = inputs[list(inputs.keys())[0]]
        doc = nlp(text)
        # For each entity that was mentioned, save this information to the dictionary.
        for ent in doc.ents:
            ent_str = str(ent)
            if ent_str in self.entities:
                self.entities[ent_str] += f"\n{text}"
            else:
                self.entities[ent_str] = text
```

We now define a prompt that takes in information about entities as well as user input


```python
from langchain.prompts.prompt import PromptTemplate

template = """The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know. You are provided with information about entities the Human mentions, if relevant.

Relevant entity information:
{entities}

Conversation:
Human: {input}
AI:"""
prompt = PromptTemplate(input_variables=["entities", "input"], template=template)
```

And now we put it all together!


```python
llm = OpenAI(temperature=0)
conversation = ConversationChain(
    llm=llm, prompt=prompt, verbose=True, memory=SpacyEntityMemory()
)
```

In the first example, with no prior knowledge about Harrison, the "Relevant entity information" section is empty.


```python
conversation.predict(input="Harrison likes machine learning")
```

    
    
    [1m> Entering new ConversationChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mThe following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know. You are provided with information about entities the Human mentions, if relevant.
    
    Relevant entity information:
    
    
    Conversation:
    Human: Harrison likes machine learning
    AI:[0m
    
    [1m> Finished ConversationChain chain.[0m
    




    " That's great to hear! Machine learning is a fascinating field of study. It involves using algorithms to analyze data and make predictions. Have you ever studied machine learning, Harrison?"



Now in the second example, we can see that it pulls in information about Harrison.


```python
conversation.predict(
    input="What do you think Harrison's favorite subject in college was?"
)
```

    
    
    [1m> Entering new ConversationChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mThe following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know. You are provided with information about entities the Human mentions, if relevant.
    
    Relevant entity information:
    Harrison likes machine learning
    
    Conversation:
    Human: What do you think Harrison's favorite subject in college was?
    AI:[0m
    
    [1m> Finished ConversationChain chain.[0m
    




    ' From what I know about Harrison, I believe his favorite subject in college was machine learning. He has expressed a strong interest in the subject and has mentioned it often.'



Again, please note that this implementation is pretty simple and brittle and probably not useful in a production setting. Its purpose is to showcase that you can add custom memory implementations.


```python

```
