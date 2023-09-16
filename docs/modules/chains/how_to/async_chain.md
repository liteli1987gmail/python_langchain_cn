# 异步 API

LangChain通过利用 [asyncio](https://docs.python.org/3/library/asyncio.html) 库为链提供了异步支持。

目前在 `LLMChain`（通过 `arun`、`apredict`、`acall`）和 `LLMMathChain`（通过 `arun` 和 `acall`）、`ChatVectorDBChain` 和 [QA chains](../index_examples/question_answering.html) 中支持异步方法。其他链的异步支持正在路上。


```python
import asyncio
import time

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


def generate_serially():
    llm = OpenAI(temperature=0.9)
    prompt = PromptTemplate(
        input_variables=["product"],
        template="What is a good name for a company that makes {product}?",
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    for _ in range(5):
        resp = chain.run(product="toothpaste")
        print(resp)


async def async_generate(chain):
    resp = await chain.arun(product="toothpaste")
    print(resp)


async def generate_concurrently():
    llm = OpenAI(temperature=0.9)
    prompt = PromptTemplate(
        input_variables=["product"],
        template="What is a good name for a company that makes {product}?",
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    tasks = [async_generate(chain) for _ in range(5)]
    await asyncio.gather(*tasks)


s = time.perf_counter()
# 如果在 Jupyter 之外运行，请使用 asyncio.run(generate_concurrently())
await generate_concurrently()
elapsed = time.perf_counter() - s
print("\033[1m" + f"并发执行花费了 {elapsed:0.2f} 秒." + "\033[0m")

s = time.perf_counter()
generate_serially()
elapsed = time.perf_counter() - s
print("\033[1m" + f"串行执行花费了 {elapsed:0.2f} 秒." + "\033[0m")
```

    
    
    BrightSmile Toothpaste Company
    
    
    BrightSmile Toothpaste Co.
    
    
    BrightSmile Toothpaste
    
    
    Gleaming Smile Inc.
    
    
    SparkleSmile Toothpaste
    [1m并发执行花费了 1.54 秒.[0m
    
    
    BrightSmile Toothpaste Co.
    
    
    MintyFresh Toothpaste Co.
    
    
    SparkleSmile Toothpaste.
    
    
    Pearly Whites Toothpaste Co.
    
    
    BrightSmile Toothpaste.
    [1m串行执行花费了 6.38 秒.[0m
    
