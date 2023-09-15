# Bedrock

[Amazon Bedrock](https://aws.amazon.com/bedrock/) is a fully managed service that makes FMs from leading AI startups and Amazon available via an API, so you can choose from a wide range of FMs to find the model that is best suited for your use case


```python
%pip install boto3
```


```python
from langchain.llms.bedrock import Bedrock

llm = Bedrock(
    credentials_profile_name="bedrock-admin", model_id="amazon.titan-tg1-large"
)
```

### Using in a conversation chain


```python
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

conversation = ConversationChain(
    llm=llm, verbose=True, memory=ConversationBufferMemory()
)

conversation.predict(input="Hi there!")
```
