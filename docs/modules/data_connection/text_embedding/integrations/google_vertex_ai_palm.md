# Google Cloud Platform Vertex AI PaLM 

Note: This is seperate from the Google PaLM integration. Google has chosen to offer an enterprise version of PaLM through GCP, and this supports the models made available through there. 

PaLM API on Vertex AI is a Preview offering, subject to the Pre-GA Offerings Terms of the [GCP Service Specific Terms](https://cloud.google.com/terms/service-terms). 

Pre-GA products and features may have limited support, and changes to pre-GA products and features may not be compatible with other pre-GA versions. For more information, see the [launch stage descriptions](https://cloud.google.com/products#product-launch-stages). Further, by using PaLM API on Vertex AI, you agree to the Generative AI Preview [terms and conditions](https://cloud.google.com/trustedtester/aitos) (Preview Terms).

For PaLM API on Vertex AI, you can process personal data as outlined in the Cloud Data Processing Addendum, subject to applicable restrictions and obligations in the Agreement (as defined in the Preview Terms).

To use Vertex AI PaLM you must have the `google-cloud-aiplatform` Python package installed and either:
- Have credentials configured for your environment (gcloud, workload identity, etc...)
- Store the path to a service account JSON file as the GOOGLE_APPLICATION_CREDENTIALS environment variable

This codebase uses the `google.auth` library which first looks for the application credentials variable mentioned above, and then looks for system-level auth.

For more information, see: 
- https://cloud.google.com/docs/authentication/application-default-credentials#GAC
- https://googleapis.dev/python/google-auth/latest/reference/google.auth.html#module-google.auth




```python
#!pip install google-cloud-aiplatform
```


```python
from langchain.embeddings import VertexAIEmbeddings
```


```python
embeddings = VertexAIEmbeddings()
```


```python
text = "This is a test document."
```


```python
query_result = embeddings.embed_query(text)
```


```python
doc_result = embeddings.embed_documents([text])
```
