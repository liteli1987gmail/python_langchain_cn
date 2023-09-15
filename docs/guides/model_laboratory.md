# Model Comparison

Constructing your language model application will likely involved choosing between many different options of prompts, models, and even chains to use. When doing so, you will want to compare these different options on different inputs in an easy, flexible, and intuitive way. 

LangChain provides the concept of a ModelLaboratory to test out and try different models.


```python
from langchain import LLMChain, OpenAI, Cohere, HuggingFaceHub, PromptTemplate
from langchain.model_laboratory import ModelLaboratory
```


```python
llms = [
    OpenAI(temperature=0),
    Cohere(model="command-xlarge-20221108", max_tokens=20, temperature=0),
    HuggingFaceHub(repo_id="google/flan-t5-xl", model_kwargs={"temperature": 1}),
]
```


```python
model_lab = ModelLaboratory.from_llms(llms)
```


```python
model_lab.compare("What color is a flamingo?")
```

    [1mInput:[0m
    What color is a flamingo?
    
    [1mOpenAI[0m
    Params: {'model': 'text-davinci-002', 'temperature': 0.0, 'max_tokens': 256, 'top_p': 1, 'frequency_penalty': 0, 'presence_penalty': 0, 'n': 1, 'best_of': 1}
    [36;1m[1;3m
    
    Flamingos are pink.[0m
    
    [1mCohere[0m
    Params: {'model': 'command-xlarge-20221108', 'max_tokens': 20, 'temperature': 0.0, 'k': 0, 'p': 1, 'frequency_penalty': 0, 'presence_penalty': 0}
    [33;1m[1;3m
    
    Pink[0m
    
    [1mHuggingFaceHub[0m
    Params: {'repo_id': 'google/flan-t5-xl', 'temperature': 1}
    [38;5;200m[1;3mpink[0m
    
    


```python
prompt = PromptTemplate(
    template="What is the capital of {state}?", input_variables=["state"]
)
model_lab_with_prompt = ModelLaboratory.from_llms(llms, prompt=prompt)
```


```python
model_lab_with_prompt.compare("New York")
```

    [1mInput:[0m
    New York
    
    [1mOpenAI[0m
    Params: {'model': 'text-davinci-002', 'temperature': 0.0, 'max_tokens': 256, 'top_p': 1, 'frequency_penalty': 0, 'presence_penalty': 0, 'n': 1, 'best_of': 1}
    [36;1m[1;3m
    
    The capital of New York is Albany.[0m
    
    [1mCohere[0m
    Params: {'model': 'command-xlarge-20221108', 'max_tokens': 20, 'temperature': 0.0, 'k': 0, 'p': 1, 'frequency_penalty': 0, 'presence_penalty': 0}
    [33;1m[1;3m
    
    The capital of New York is Albany.[0m
    
    [1mHuggingFaceHub[0m
    Params: {'repo_id': 'google/flan-t5-xl', 'temperature': 1}
    [38;5;200m[1;3mst john s[0m
    
    


```python
from langchain import SelfAskWithSearchChain, SerpAPIWrapper

open_ai_llm = OpenAI(temperature=0)
search = SerpAPIWrapper()
self_ask_with_search_openai = SelfAskWithSearchChain(
    llm=open_ai_llm, search_chain=search, verbose=True
)

cohere_llm = Cohere(temperature=0, model="command-xlarge-20221108")
search = SerpAPIWrapper()
self_ask_with_search_cohere = SelfAskWithSearchChain(
    llm=cohere_llm, search_chain=search, verbose=True
)
```


```python
chains = [self_ask_with_search_openai, self_ask_with_search_cohere]
names = [str(open_ai_llm), str(cohere_llm)]
```


```python
model_lab = ModelLaboratory(chains, names=names)
```


```python
model_lab.compare("What is the hometown of the reigning men's U.S. Open champion?")
```

    [1mInput:[0m
    What is the hometown of the reigning men's U.S. Open champion?
    
    [1mOpenAI[0m
    Params: {'model': 'text-davinci-002', 'temperature': 0.0, 'max_tokens': 256, 'top_p': 1, 'frequency_penalty': 0, 'presence_penalty': 0, 'n': 1, 'best_of': 1}
    
    
    [1m> Entering new chain...[0m
    What is the hometown of the reigning men's U.S. Open champion?
    Are follow up questions needed here:[32;1m[1;3m Yes.
    Follow up: Who is the reigning men's U.S. Open champion?[0m
    Intermediate answer: [33;1m[1;3mCarlos Alcaraz.[0m[32;1m[1;3m
    Follow up: Where is Carlos Alcaraz from?[0m
    Intermediate answer: [33;1m[1;3mEl Palmar, Spain.[0m[32;1m[1;3m
    So the final answer is: El Palmar, Spain[0m
    [1m> Finished chain.[0m
    [36;1m[1;3m
    So the final answer is: El Palmar, Spain[0m
    
    [1mCohere[0m
    Params: {'model': 'command-xlarge-20221108', 'max_tokens': 256, 'temperature': 0.0, 'k': 0, 'p': 1, 'frequency_penalty': 0, 'presence_penalty': 0}
    
    
    [1m> Entering new chain...[0m
    What is the hometown of the reigning men's U.S. Open champion?
    Are follow up questions needed here:[32;1m[1;3m Yes.
    Follow up: Who is the reigning men's U.S. Open champion?[0m
    Intermediate answer: [33;1m[1;3mCarlos Alcaraz.[0m[32;1m[1;3m
    So the final answer is:
    
    Carlos Alcaraz[0m
    [1m> Finished chain.[0m
    [33;1m[1;3m
    So the final answer is:
    
    Carlos Alcaraz[0m
    
    


```python

```
