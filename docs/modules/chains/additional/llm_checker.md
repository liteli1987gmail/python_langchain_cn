# Self-checking chain
This notebook showcases how to use LLMCheckerChain.


```python
from langchain.chains import LLMCheckerChain
from langchain.llms import OpenAI

llm = OpenAI(temperature=0.7)

text = "What type of mammal lays the biggest eggs?"

checker_chain = LLMCheckerChain.from_llm(llm, verbose=True)

checker_chain.run(text)
```

    
    
    [1m> Entering new LLMCheckerChain chain...[0m
    
    
    [1m> Entering new SequentialChain chain...[0m
    
    [1m> Finished chain.[0m
    
    [1m> Finished chain.[0m
    




    ' No mammal lays the biggest eggs. The Elephant Bird, which was a species of giant bird, laid the largest eggs of any bird.'




```python

```
