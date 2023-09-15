# MatchingEngine

This notebook shows how to use functionality related to the GCP Vertex AI `MatchingEngine` vector database.

> Vertex AI [Matching Engine](https://cloud.google.com/vertex-ai/docs/matching-engine/overview) provides the industry's leading high-scale low latency vector database. These vector databases are commonly referred to as vector similarity-matching or an approximate nearest neighbor (ANN) service.

**Note**: This module expects an endpoint and deployed index already created as the creation time takes close to one hour. To see how to create an index refer to the section [Create Index and deploy it to an Endpoint](#create-index-and-deploy-it-to-an-endpoint)

## Create VectorStore from texts


```python
from langchain.vectorstores import MatchingEngine
```


```python
texts = [
    "The cat sat on",
    "the mat.",
    "I like to",
    "eat pizza for",
    "dinner.",
    "The sun sets",
    "in the west.",
]


vector_store = MatchingEngine.from_components(
    texts=texts,
    project_id="<my_project_id>",
    region="<my_region>",
    gcs_bucket_uri="<my_gcs_bucket>",
    index_id="<my_matching_engine_index_id>",
    endpoint_id="<my_matching_engine_endpoint_id>",
)

vector_store.add_texts(texts=texts)

vector_store.similarity_search("lunch", k=2)
```

## Create Index and deploy it to an Endpoint

### Imports, Constants and Configs


```python
# Installing dependencies.
!pip install tensorflow \
            google-cloud-aiplatform \
            tensorflow-hub \
            tensorflow-text 
```


```python
import os
import json

from google.cloud import aiplatform
import tensorflow_hub as hub
import tensorflow_text
```


```python
PROJECT_ID = "<my_project_id>"
REGION = "<my_region>"
VPC_NETWORK = "<my_vpc_network_name>"
PEERING_RANGE_NAME = "ann-langchain-me-range"  # Name for creating the VPC peering.
BUCKET_URI = "gs://<bucket_uri>"
# The number of dimensions for the tensorflow universal sentence encoder.
# If other embedder is used, the dimensions would probably need to change.
DIMENSIONS = 512
DISPLAY_NAME = "index-test-name"
EMBEDDING_DIR = f"{BUCKET_URI}/banana"
DEPLOYED_INDEX_ID = "endpoint-test-name"

PROJECT_NUMBER = !gcloud projects list --filter="PROJECT_ID:'{PROJECT_ID}'" --format='value(PROJECT_NUMBER)'
PROJECT_NUMBER = PROJECT_NUMBER[0]
VPC_NETWORK_FULL = f"projects/{PROJECT_NUMBER}/global/networks/{VPC_NETWORK}"

# Change this if you need the VPC to be created.
CREATE_VPC = False
```


```python
# Set the project id
! gcloud config set project {PROJECT_ID}
```


```python
# Remove the if condition to run the encapsulated code
if CREATE_VPC:
    # Create a VPC network
    ! gcloud compute networks create {VPC_NETWORK} --bgp-routing-mode=regional --subnet-mode=auto --project={PROJECT_ID}

    # Add necessary firewall rules
    ! gcloud compute firewall-rules create {VPC_NETWORK}-allow-icmp --network {VPC_NETWORK} --priority 65534 --project {PROJECT_ID} --allow icmp

    ! gcloud compute firewall-rules create {VPC_NETWORK}-allow-internal --network {VPC_NETWORK} --priority 65534 --project {PROJECT_ID} --allow all --source-ranges 10.128.0.0/9

    ! gcloud compute firewall-rules create {VPC_NETWORK}-allow-rdp --network {VPC_NETWORK} --priority 65534 --project {PROJECT_ID} --allow tcp:3389

    ! gcloud compute firewall-rules create {VPC_NETWORK}-allow-ssh --network {VPC_NETWORK} --priority 65534 --project {PROJECT_ID} --allow tcp:22

    # Reserve IP range
    ! gcloud compute addresses create {PEERING_RANGE_NAME} --global --prefix-length=16 --network={VPC_NETWORK} --purpose=VPC_PEERING --project={PROJECT_ID} --description="peering range"

    # Set up peering with service networking
    # Your account must have the "Compute Network Admin" role to run the following.
    ! gcloud services vpc-peerings connect --service=servicenetworking.googleapis.com --network={VPC_NETWORK} --ranges={PEERING_RANGE_NAME} --project={PROJECT_ID}
```


```python
# Creating bucket.
! gsutil mb -l $REGION -p $PROJECT_ID $BUCKET_URI
```

### Using Tensorflow Universal Sentence Encoder as an Embedder


```python
# Load the Universal Sentence Encoder module
module_url = "https://tfhub.dev/google/universal-sentence-encoder-multilingual/3"
model = hub.load(module_url)
```


```python
# Generate embeddings for each word
embeddings = model(["banana"])
```

### Inserting a test embedding


```python
initial_config = {
    "id": "banana_id",
    "embedding": [float(x) for x in list(embeddings.numpy()[0])],
}

with open("data.json", "w") as f:
    json.dump(initial_config, f)

!gsutil cp data.json {EMBEDDING_DIR}/file.json
```


```python
aiplatform.init(project=PROJECT_ID, location=REGION, staging_bucket=BUCKET_URI)
```

### Creating Index


```python
my_index = aiplatform.MatchingEngineIndex.create_tree_ah_index(
    display_name=DISPLAY_NAME,
    contents_delta_uri=EMBEDDING_DIR,
    dimensions=DIMENSIONS,
    approximate_neighbors_count=150,
    distance_measure_type="DOT_PRODUCT_DISTANCE",
)
```

### Creating Endpoint


```python
my_index_endpoint = aiplatform.MatchingEngineIndexEndpoint.create(
    display_name=f"{DISPLAY_NAME}-endpoint",
    network=VPC_NETWORK_FULL,
)
```

### Deploy Index


```python
my_index_endpoint = my_index_endpoint.deploy_index(
    index=my_index, deployed_index_id=DEPLOYED_INDEX_ID
)

my_index_endpoint.deployed_indexes
```
