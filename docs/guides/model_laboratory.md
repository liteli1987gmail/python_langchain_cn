# 模型比较

构建语言模型应用程序很可能涉及选择许多不同的提示、模型甚至链条。在这样做时，您将希望以一种简单、灵活和直观的方式比较这些不同的选项在不同的输入上。

LangChain提供了一个ModelLaboratory的概念，用于测试和尝试不同的模型。


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
model_lab.compare("火烈鸟是什么颜色？")
```
    [1m输入:[0m
    火烈鸟是什么颜色？
    
    [1mOpenAI[0m
    参数: {'model': 'text-davinci-002', 'temperature': 0.0, 'max_tokens': 256, 'top_p': 1, 'frequency_penalty': 0, 'presence_penalty': 0, 'n': 1, 'best_of': 1}
    [36;1m[1;3m
    
    火烈鸟是粉色的。[0m
    
    [1mCohere[0m
    参数: {'model': 'command-xlarge-20221108', 'max_tokens': 20, 'temperature': 0.0, 'k': 0, 'p': 1, 'frequency_penalty': 0, 'presence_penalty': 0}
    [33;1m[1;3m
    
    粉色[0m
    
    [1mHuggingFaceHub[0m
    参数: {'repo_id': 'google/flan-t5-xl', 'temperature': 1}
    [38;5;200m[1;3m粉色[0m
    
    


```python
prompt = PromptTemplate(
    template="{state}的首都是什么？", input_variables=["state"]
)
model_lab_with_prompt = ModelLaboratory.from_llms(llms, prompt=prompt)
```


```python
model_lab_with_prompt.compare("纽约")
```

    [1mInput:[0m
    New York
    
    [1mOpenAI[0m
    Params: {'model': 'text-davinci-002', 'temperature': 0.0, 'max_tokens': 256, 'top_p': 1, 'frequency_penalty': 0, 'presence_penalty': 0, 'n': 1, 'best_of': 1}
    [36;1m[1;3m
    
    纽约的首都是奥尔巴尼。[0m
    
    [1mCohere[0m
    Params: {'model': 'command-xlarge-20221108', 'max_tokens': 20, 'temperature': 0.0, 'k': 0, 'p': 1, 'frequency_penalty': 0, 'presence_penalty': 0}
    [33;1m[1;3m
    
    纽约的首都是奥尔巴尼。[0m
    
    [1mHuggingFaceHub[0m
    参数: {'repo_id': 'google/flan-t5-xl', 'temperature': 1}
    [38;5;200m[1;3m圣约翰斯[0m
    
    


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
model_lab.compare("现任男子美国公开赛冠军的家乡在哪里？")
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
    
    
    [1m> 进入新的链条...[0m
    现任男子美国公开赛冠军的家乡在哪里？
    这里是否需要后续问题:[32;1m[1;3m 是的。
    后续问题: 现任男子美国公开赛冠军是谁？[0m
    中间答案: [33;1m[1;3m卡洛斯·阿尔卡拉斯。[0m[32;1m[1;3m
    所以最终答案是:
    
    卡洛斯·阿尔卡拉斯[0m
    [1m> 完成链条。[0m
    [33;1m[1;3m
    所以最终答案是:
    
    卡洛斯·阿尔卡拉斯[0m
    
    


```python

```
