# Manifest

This notebook goes over how to use Manifest and LangChain.

For more detailed information on `manifest`, and how to use it with local hugginface models like in this example, see https://github.com/HazyResearch/manifest

Another example of [using Manifest with Langchain](https://github.com/HazyResearch/manifest/blob/main/examples/langchain_chatgpt.html).


```python
!pip install manifest-ml
```


```python
from manifest import Manifest
from langchain.llms.manifest import ManifestWrapper
```


```python
manifest = Manifest(
    client_name="huggingface", client_connection="http://127.0.0.1:5000"
)
print(manifest.client.get_model_params())
```


```python
llm = ManifestWrapper(
    client=manifest, llm_kwargs={"temperature": 0.001, "max_tokens": 256}
)
```


```python
# Map reduce example
from langchain import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.mapreduce import MapReduceChain


_prompt = """Write a concise summary of the following:


{text}


CONCISE SUMMARY:"""
prompt = PromptTemplate(template=_prompt, input_variables=["text"])

text_splitter = CharacterTextSplitter()

mp_chain = MapReduceChain.from_params(llm, prompt, text_splitter)
```


```python
with open("../../../state_of_the_union.txt") as f:
    state_of_the_union = f.read()
mp_chain.run(state_of_the_union)
```




    'President Obama delivered his annual State of the Union address on Tuesday night, laying out his priorities for the coming year. Obama said the government will provide free flu vaccines to all Americans, ending the government shutdown and allowing businesses to reopen. The president also said that the government will continue to send vaccines to 112 countries, more than any other nation. "We have lost so much to COVID-19," Trump said. "Time with one another. And worst of all, so much loss of life." He said the CDC is working on a vaccine for kids under 5, and that the government will be ready with plenty of vaccines when they are available. Obama says the new guidelines are a "great step forward" and that the virus is no longer a threat. He says the government is launching a "Test to Treat" initiative that will allow people to get tested at a pharmacy and get antiviral pills on the spot at no cost. Obama says the new guidelines are a "great step forward" and that the virus is no longer a threat. He says the government will continue to send vaccines to 112 countries, more than any other nation. "We are coming for your'



## Compare HF Models


```python
from langchain.model_laboratory import ModelLaboratory

manifest1 = ManifestWrapper(
    client=Manifest(
        client_name="huggingface", client_connection="http://127.0.0.1:5000"
    ),
    llm_kwargs={"temperature": 0.01},
)
manifest2 = ManifestWrapper(
    client=Manifest(
        client_name="huggingface", client_connection="http://127.0.0.1:5001"
    ),
    llm_kwargs={"temperature": 0.01},
)
manifest3 = ManifestWrapper(
    client=Manifest(
        client_name="huggingface", client_connection="http://127.0.0.1:5002"
    ),
    llm_kwargs={"temperature": 0.01},
)
llms = [manifest1, manifest2, manifest3]
model_lab = ModelLaboratory(llms)
```


```python
model_lab.compare("What color is a flamingo?")
```

    [1mInput:[0m
    What color is a flamingo?
    
    [1mManifestWrapper[0m
    Params: {'model_name': 'bigscience/T0_3B', 'model_path': 'bigscience/T0_3B', 'temperature': 0.01}
    [104mpink[0m
    
    [1mManifestWrapper[0m
    Params: {'model_name': 'EleutherAI/gpt-neo-125M', 'model_path': 'EleutherAI/gpt-neo-125M', 'temperature': 0.01}
    [103mA flamingo is a small, round[0m
    
    [1mManifestWrapper[0m
    Params: {'model_name': 'google/flan-t5-xl', 'model_path': 'google/flan-t5-xl', 'temperature': 0.01}
    [101mpink[0m
    
    
