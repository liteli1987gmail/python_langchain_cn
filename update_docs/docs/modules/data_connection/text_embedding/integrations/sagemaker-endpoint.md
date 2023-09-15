# SageMaker Endpoint Embeddings

Let's load the SageMaker Endpoints Embeddings class. The class can be used if you host, e.g. your own Hugging Face model on SageMaker.

For instructions on how to do this, please see [here](https://www.philschmid.de/custom-inference-huggingface-sagemaker). **Note**: In order to handle batched requests, you will need to adjust the return line in the `predict_fn()` function within the custom `inference.py` script:

Change from

`return {"vectors": sentence_embeddings[0].tolist()}`

to:

`return {"vectors": sentence_embeddings.tolist()}`.


```python
!pip3 install langchain boto3
```


```python
from typing import Dict, List
from langchain.embeddings import SagemakerEndpointEmbeddings
from langchain.llms.sagemaker_endpoint import ContentHandlerBase
import json


class ContentHandler(ContentHandlerBase):
    content_type = "application/json"
    accepts = "application/json"

    def transform_input(self, inputs: list[str], model_kwargs: Dict) -> bytes:
        input_str = json.dumps({"inputs": inputs, **model_kwargs})
        return input_str.encode("utf-8")

    def transform_output(self, output: bytes) -> List[List[float]]:
        response_json = json.loads(output.read().decode("utf-8"))
        return response_json["vectors"]


content_handler = ContentHandler()


embeddings = SagemakerEndpointEmbeddings(
    # endpoint_name="endpoint-name",
    # credentials_profile_name="credentials-profile-name",
    endpoint_name="huggingface-pytorch-inference-2023-03-21-16-14-03-834",
    region_name="us-east-1",
    content_handler=content_handler,
)
```


```python
query_result = embeddings.embed_query("foo")
```


```python
doc_results = embeddings.embed_documents(["foo"])
```


```python
doc_results
```


```python

```
