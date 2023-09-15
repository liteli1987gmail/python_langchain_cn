# OpenLM
[OpenLM](https://github.com/r2d4/openlm) is a zero-dependency OpenAI-compatible LLM provider that can call different inference endpoints directly via HTTP. 


It implements the OpenAI Completion class so that it can be used as a drop-in replacement for the OpenAI API. This changeset utilizes BaseOpenAI for minimal added code.

This examples goes over how to use LangChain to interact with both OpenAI and HuggingFace. You'll need API keys from both.

### Setup
Install dependencies and set API keys.


```python
# Uncomment to install openlm and openai if you haven't already

# !pip install openlm
# !pip install openai
```


```python
from getpass import getpass
import os
import subprocess


# Check if OPENAI_API_KEY environment variable is set
if "OPENAI_API_KEY" not in os.environ:
    print("Enter your OpenAI API key:")
    os.environ["OPENAI_API_KEY"] = getpass()

# Check if HF_API_TOKEN environment variable is set
if "HF_API_TOKEN" not in os.environ:
    print("Enter your HuggingFace Hub API key:")
    os.environ["HF_API_TOKEN"] = getpass()
```

### Using LangChain with OpenLM

Here we're going to call two models in an LLMChain, `text-davinci-003` from OpenAI and `gpt2` on HuggingFace.


```python
from langchain.llms import OpenLM
from langchain import PromptTemplate, LLMChain
```


```python
question = "What is the capital of France?"
template = """Question: {question}

Answer: Let's think step by step."""

prompt = PromptTemplate(template=template, input_variables=["question"])

for model in ["text-davinci-003", "huggingface.co/gpt2"]:
    llm = OpenLM(model=model)
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    result = llm_chain.run(question)
    print(
        """Model: {}
Result: {}""".format(
            model, result
        )
    )
```

    Model: text-davinci-003
    Result:  France is a country in Europe. The capital of France is Paris.
    Model: huggingface.co/gpt2
    Result: Question: What is the capital of France?
    
    Answer: Let's think step by step. I am not going to lie, this is a complicated issue, and I don't see any solutions to all this, but it is still far more
    
