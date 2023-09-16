# 自检链
这个笔记本展示了如何使用LLMCheckerChain。

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
    




    '没有哺乳动物能够产下最大的蛋。大象鸟是一种巨鸟，它的蛋是所有鸟类中最大的。'




```python
```