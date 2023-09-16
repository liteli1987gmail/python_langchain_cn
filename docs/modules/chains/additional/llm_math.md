# Math chain

本笔记本展示了使用LLMs和Python REPL解决复杂的数学问题。

```python
from langchain import OpenAI, LLMMathChain

llm = OpenAI(temperature=0)
llm_math = LLMMathChain.from_llm(llm, verbose=True)

llm_math.run("求13的0.3432次方")
```

    
    
    [1m> Entering new LLMMathChain chain...[0m
    What is 13 raised to the .3432 power?[32;1m[1;3m
    ```text
    13 ** 0.3432
    ```
    
    ...numexpr.evaluate("13 ** 0.3432")...
    [0m
    Answer: [33;1m[1;3m2.4116004626599237[0m
    [1m> Finished chain.[0m
    




    'Answer: 2.4116004626599237'




```python

```