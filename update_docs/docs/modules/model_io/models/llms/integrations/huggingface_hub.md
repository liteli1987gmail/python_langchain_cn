# Hugging Face Hub

The [Hugging Face Hub](https://huggingface.co/docs/hub/index) is a platform with over 120k models, 20k datasets, and 50k demo apps (Spaces), all open source and publicly available, in an online platform where people can easily collaborate and build ML together.

This example showcases how to connect to the Hugging Face Hub.

To use, you should have the ``huggingface_hub`` python [package installed](https://huggingface.co/docs/huggingface_hub/installation).


```python
!pip install huggingface_hub > /dev/null
```


```python
# get a token: https://huggingface.co/docs/api-inference/quicktour#get-your-api-token

from getpass import getpass

HUGGINGFACEHUB_API_TOKEN = getpass()
```


```python
import os

os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACEHUB_API_TOKEN
```

**Select a Model**


```python
from langchain import HuggingFaceHub

repo_id = "google/flan-t5-xl"  # See https://huggingface.co/models?pipeline_tag=text-generation&sort=downloads for some other options

llm = HuggingFaceHub(repo_id=repo_id, model_kwargs={"temperature": 0, "max_length": 64})
```


```python
from langchain import PromptTemplate, LLMChain

template = """Question: {question}

Answer: Let's think step by step."""
prompt = PromptTemplate(template=template, input_variables=["question"])
llm_chain = LLMChain(prompt=prompt, llm=llm)

question = "Who won the FIFA World Cup in the year 1994? "

print(llm_chain.run(question))
```

## Examples

Below are some examples of models you can access through the Hugging Face Hub integration.

### StableLM, by Stability AI

See [Stability AI's](https://huggingface.co/stabilityai) organization page for a list of available models.


```python
repo_id = "stabilityai/stablelm-tuned-alpha-3b"
# Others include stabilityai/stablelm-base-alpha-3b
# as well as 7B parameter versions
```


```python
llm = HuggingFaceHub(repo_id=repo_id, model_kwargs={"temperature": 0, "max_length": 64})
```


```python
# Reuse the prompt and question from above.
llm_chain = LLMChain(prompt=prompt, llm=llm)
print(llm_chain.run(question))
```

### Dolly, by Databricks

See [Databricks](https://huggingface.co/databricks) organization page for a list of available models.


```python
from langchain import HuggingFaceHub

repo_id = "databricks/dolly-v2-3b"

llm = HuggingFaceHub(repo_id=repo_id, model_kwargs={"temperature": 0, "max_length": 64})
```


```python
# Reuse the prompt and question from above.
llm_chain = LLMChain(prompt=prompt, llm=llm)
print(llm_chain.run(question))
```

### Camel, by Writer

See [Writer's](https://huggingface.co/Writer) organization page for a list of available models.


```python
from langchain import HuggingFaceHub

repo_id = "Writer/camel-5b-hf"  # See https://huggingface.co/Writer for other options
llm = HuggingFaceHub(repo_id=repo_id, model_kwargs={"temperature": 0, "max_length": 64})
```


```python
# Reuse the prompt and question from above.
llm_chain = LLMChain(prompt=prompt, llm=llm)
print(llm_chain.run(question))
```

**And many more!**


```python

```
