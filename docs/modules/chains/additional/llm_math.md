# 数学链

本笔记本展示了使用LLMs和Python REPL解决复杂的数学问题。

```python
from langchain import OpenAI, LLMMathChain

llm = OpenAI(temperature=0)
llm_math = LLMMathChain.from_llm(llm, verbose=True)

llm_math.run("13的0.3432次方")
```


    [1m> 进入新的LLMMathChain链...[0m
    What is 13 raised to the .3432 power?
    ```text
    13 ** 0.3432
    ```
    
    ...numexpr.evaluate("13 ** 0.3432")...
    [0m
    Answer: [33;1m2.4116004626599237[0m
    [1m> 完成链。[0m





    'Answer: 2.4116004626599237'




```python
```