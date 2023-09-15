# Modal

The [Modal Python Library](https://modal.com/docs/guide) provides convenient, on-demand access to serverless cloud compute from Python scripts on your local computer. 
The `Modal` itself does not provide any LLMs but only the infrastructure.

This example goes over how to use LangChain to interact with `Modal`.

[Here](https://modal.com/docs/guide/ex/potus_speech_qanda) is another example how to use LangChain to interact with `Modal`.


```python
!pip install modal-client
```


```python
# register and get a new token

!modal token new
```

    [?25lLaunching login page in your browser window[33m...[0m
    [2KIf this is not showing up, please copy this URL into your web browser manually:
    [2Km⠙[0m Waiting for authentication in the web browser...
    ]8;id=417802;https://modal.com/token-flow/tf-ptEuGecm7T1T5YQe42kwM1\[4;94mhttps://modal.com/token-flow/tf-ptEuGecm7T1T5YQe42kwM1[0m]8;;\
    
    [2K[32m⠙[0m Waiting for authentication in the web browser...
    [1A[2K^C
    
    [31mAborted.[0m
    

Follow [these instructions](https://modal.com/docs/guide/secrets) to deal with secrets.


```python
from langchain.llms import Modal
from langchain import PromptTemplate, LLMChain
```


```python
template = """Question: {question}

Answer: Let's think step by step."""

prompt = PromptTemplate(template=template, input_variables=["question"])
```


```python
llm = Modal(endpoint_url="YOUR_ENDPOINT_URL")
```


```python
llm_chain = LLMChain(prompt=prompt, llm=llm)
```


```python
question = "What NFL team won the Super Bowl in the year Justin Beiber was born?"

llm_chain.run(question)
```
