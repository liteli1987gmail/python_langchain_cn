# Use LangChain, GPT and Deep Lake to work with code base
In this tutorial, we are going to use Langchain + Deep Lake with GPT to analyze the code base of the LangChain itself. 

## Design

1. Prepare data:
   1. Upload all python project files using the `langchain.document_loaders.TextLoader`. We will call these files the **documents**.
   2. Split all documents to chunks using the `langchain.text_splitter.CharacterTextSplitter`.
   3. Embed chunks and upload them into the DeepLake using `langchain.embeddings.openai.OpenAIEmbeddings` and `langchain.vectorstores.DeepLake`
2. Question-Answering:
   1. Build a chain from `langchain.chat_models.ChatOpenAI` and `langchain.chains.ConversationalRetrievalChain`
   2. Prepare questions.
   3. Get answers running the chain.


## Implementation

### Integration preparations

We need to set up keys for external services and install necessary python libraries.


```python
#!python3 -m pip install --upgrade langchain deeplake openai
```

Set up OpenAI embeddings, Deep Lake multi-modal vector store api and authenticate. 

For full documentation of Deep Lake please follow https://docs.activeloop.ai/ and API reference https://docs.deeplake.ai/en/latest/


```python
import os
from getpass import getpass

os.environ["OPENAI_API_KEY"] = getpass()
# Please manually enter OpenAI Key
```

     ········
    

Authenticate into Deep Lake if you want to create your own dataset and publish it. You can get an API key from the platform at [app.activeloop.ai](https://app.activeloop.ai)


```python
os.environ["ACTIVELOOP_TOKEN"] = getpass.getpass("Activeloop Token:")
```

     ········
    

### Prepare data 

Load all repository files. Here we assume this notebook is downloaded as the part of the langchain fork and we work with the python files of the `langchain` repo.

If you want to use files from different repo, change `root_dir` to the root dir of your repo.


```python
from langchain.document_loaders import TextLoader

root_dir = "../../../.."

docs = []
for dirpath, dirnames, filenames in os.walk(root_dir):
    for file in filenames:
        if file.endswith(".py") and "/.venv/" not in dirpath:
            try:
                loader = TextLoader(os.path.join(dirpath, file), encoding="utf-8")
                docs.extend(loader.load_and_split())
            except Exception as e:
                pass
print(f"{len(docs)}")
```

    1147
    

Then, chunk the files


```python
from langchain.text_splitter import CharacterTextSplitter

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(docs)
print(f"{len(texts)}")
```

    Created a chunk of size 1620, which is longer than the specified 1000
    Created a chunk of size 1213, which is longer than the specified 1000
    Created a chunk of size 1263, which is longer than the specified 1000
    Created a chunk of size 1448, which is longer than the specified 1000
    Created a chunk of size 1120, which is longer than the specified 1000
    Created a chunk of size 1148, which is longer than the specified 1000
    Created a chunk of size 1826, which is longer than the specified 1000
    Created a chunk of size 1260, which is longer than the specified 1000
    Created a chunk of size 1195, which is longer than the specified 1000
    Created a chunk of size 2147, which is longer than the specified 1000
    Created a chunk of size 1410, which is longer than the specified 1000
    Created a chunk of size 1269, which is longer than the specified 1000
    Created a chunk of size 1030, which is longer than the specified 1000
    Created a chunk of size 1046, which is longer than the specified 1000
    Created a chunk of size 1024, which is longer than the specified 1000
    Created a chunk of size 1026, which is longer than the specified 1000
    Created a chunk of size 1285, which is longer than the specified 1000
    Created a chunk of size 1370, which is longer than the specified 1000
    Created a chunk of size 1031, which is longer than the specified 1000
    Created a chunk of size 1999, which is longer than the specified 1000
    Created a chunk of size 1029, which is longer than the specified 1000
    Created a chunk of size 1120, which is longer than the specified 1000
    Created a chunk of size 1033, which is longer than the specified 1000
    Created a chunk of size 1143, which is longer than the specified 1000
    Created a chunk of size 1416, which is longer than the specified 1000
    Created a chunk of size 2482, which is longer than the specified 1000
    Created a chunk of size 1890, which is longer than the specified 1000
    Created a chunk of size 1418, which is longer than the specified 1000
    Created a chunk of size 1848, which is longer than the specified 1000
    Created a chunk of size 1069, which is longer than the specified 1000
    Created a chunk of size 2369, which is longer than the specified 1000
    Created a chunk of size 1045, which is longer than the specified 1000
    Created a chunk of size 1501, which is longer than the specified 1000
    Created a chunk of size 1208, which is longer than the specified 1000
    Created a chunk of size 1950, which is longer than the specified 1000
    Created a chunk of size 1283, which is longer than the specified 1000
    Created a chunk of size 1414, which is longer than the specified 1000
    Created a chunk of size 1304, which is longer than the specified 1000
    Created a chunk of size 1224, which is longer than the specified 1000
    Created a chunk of size 1060, which is longer than the specified 1000
    Created a chunk of size 2461, which is longer than the specified 1000
    Created a chunk of size 1099, which is longer than the specified 1000
    Created a chunk of size 1178, which is longer than the specified 1000
    Created a chunk of size 1449, which is longer than the specified 1000
    Created a chunk of size 1345, which is longer than the specified 1000
    Created a chunk of size 3359, which is longer than the specified 1000
    Created a chunk of size 2248, which is longer than the specified 1000
    Created a chunk of size 1589, which is longer than the specified 1000
    Created a chunk of size 2104, which is longer than the specified 1000
    Created a chunk of size 1505, which is longer than the specified 1000
    Created a chunk of size 1387, which is longer than the specified 1000
    Created a chunk of size 1215, which is longer than the specified 1000
    Created a chunk of size 1240, which is longer than the specified 1000
    Created a chunk of size 1635, which is longer than the specified 1000
    Created a chunk of size 1075, which is longer than the specified 1000
    Created a chunk of size 2180, which is longer than the specified 1000
    Created a chunk of size 1791, which is longer than the specified 1000
    Created a chunk of size 1555, which is longer than the specified 1000
    Created a chunk of size 1082, which is longer than the specified 1000
    Created a chunk of size 1225, which is longer than the specified 1000
    Created a chunk of size 1287, which is longer than the specified 1000
    Created a chunk of size 1085, which is longer than the specified 1000
    Created a chunk of size 1117, which is longer than the specified 1000
    Created a chunk of size 1966, which is longer than the specified 1000
    Created a chunk of size 1150, which is longer than the specified 1000
    Created a chunk of size 1285, which is longer than the specified 1000
    Created a chunk of size 1150, which is longer than the specified 1000
    Created a chunk of size 1585, which is longer than the specified 1000
    Created a chunk of size 1208, which is longer than the specified 1000
    Created a chunk of size 1267, which is longer than the specified 1000
    Created a chunk of size 1542, which is longer than the specified 1000
    Created a chunk of size 1183, which is longer than the specified 1000
    Created a chunk of size 2424, which is longer than the specified 1000
    Created a chunk of size 1017, which is longer than the specified 1000
    Created a chunk of size 1304, which is longer than the specified 1000
    Created a chunk of size 1379, which is longer than the specified 1000
    Created a chunk of size 1324, which is longer than the specified 1000
    Created a chunk of size 1205, which is longer than the specified 1000
    Created a chunk of size 1056, which is longer than the specified 1000
    Created a chunk of size 1195, which is longer than the specified 1000
    Created a chunk of size 3608, which is longer than the specified 1000
    Created a chunk of size 1058, which is longer than the specified 1000
    Created a chunk of size 1075, which is longer than the specified 1000
    Created a chunk of size 1217, which is longer than the specified 1000
    Created a chunk of size 1109, which is longer than the specified 1000
    Created a chunk of size 1440, which is longer than the specified 1000
    Created a chunk of size 1046, which is longer than the specified 1000
    Created a chunk of size 1220, which is longer than the specified 1000
    Created a chunk of size 1403, which is longer than the specified 1000
    Created a chunk of size 1241, which is longer than the specified 1000
    Created a chunk of size 1427, which is longer than the specified 1000
    Created a chunk of size 1049, which is longer than the specified 1000
    Created a chunk of size 1580, which is longer than the specified 1000
    Created a chunk of size 1565, which is longer than the specified 1000
    Created a chunk of size 1131, which is longer than the specified 1000
    Created a chunk of size 1425, which is longer than the specified 1000
    Created a chunk of size 1054, which is longer than the specified 1000
    Created a chunk of size 1027, which is longer than the specified 1000
    Created a chunk of size 2559, which is longer than the specified 1000
    Created a chunk of size 1028, which is longer than the specified 1000
    Created a chunk of size 1382, which is longer than the specified 1000
    Created a chunk of size 1888, which is longer than the specified 1000
    Created a chunk of size 1475, which is longer than the specified 1000
    Created a chunk of size 1652, which is longer than the specified 1000
    Created a chunk of size 1891, which is longer than the specified 1000
    Created a chunk of size 1899, which is longer than the specified 1000
    Created a chunk of size 1021, which is longer than the specified 1000
    Created a chunk of size 1085, which is longer than the specified 1000
    Created a chunk of size 1854, which is longer than the specified 1000
    Created a chunk of size 1672, which is longer than the specified 1000
    Created a chunk of size 2537, which is longer than the specified 1000
    Created a chunk of size 1251, which is longer than the specified 1000
    Created a chunk of size 1734, which is longer than the specified 1000
    Created a chunk of size 1642, which is longer than the specified 1000
    Created a chunk of size 1376, which is longer than the specified 1000
    Created a chunk of size 1253, which is longer than the specified 1000
    Created a chunk of size 1642, which is longer than the specified 1000
    Created a chunk of size 1419, which is longer than the specified 1000
    Created a chunk of size 1438, which is longer than the specified 1000
    Created a chunk of size 1427, which is longer than the specified 1000
    Created a chunk of size 1684, which is longer than the specified 1000
    Created a chunk of size 1760, which is longer than the specified 1000
    Created a chunk of size 1157, which is longer than the specified 1000
    Created a chunk of size 2504, which is longer than the specified 1000
    Created a chunk of size 1082, which is longer than the specified 1000
    Created a chunk of size 2268, which is longer than the specified 1000
    Created a chunk of size 1784, which is longer than the specified 1000
    Created a chunk of size 1311, which is longer than the specified 1000
    Created a chunk of size 2972, which is longer than the specified 1000
    Created a chunk of size 1144, which is longer than the specified 1000
    Created a chunk of size 1825, which is longer than the specified 1000
    Created a chunk of size 1508, which is longer than the specified 1000
    Created a chunk of size 2901, which is longer than the specified 1000
    Created a chunk of size 1715, which is longer than the specified 1000
    Created a chunk of size 1062, which is longer than the specified 1000
    Created a chunk of size 1206, which is longer than the specified 1000
    Created a chunk of size 1102, which is longer than the specified 1000
    Created a chunk of size 1184, which is longer than the specified 1000
    Created a chunk of size 1002, which is longer than the specified 1000
    Created a chunk of size 1065, which is longer than the specified 1000
    Created a chunk of size 1871, which is longer than the specified 1000
    Created a chunk of size 1754, which is longer than the specified 1000
    Created a chunk of size 2413, which is longer than the specified 1000
    Created a chunk of size 1771, which is longer than the specified 1000
    Created a chunk of size 2054, which is longer than the specified 1000
    Created a chunk of size 2000, which is longer than the specified 1000
    Created a chunk of size 2061, which is longer than the specified 1000
    Created a chunk of size 1066, which is longer than the specified 1000
    Created a chunk of size 1419, which is longer than the specified 1000
    Created a chunk of size 1368, which is longer than the specified 1000
    Created a chunk of size 1008, which is longer than the specified 1000
    Created a chunk of size 1227, which is longer than the specified 1000
    Created a chunk of size 1745, which is longer than the specified 1000
    Created a chunk of size 2296, which is longer than the specified 1000
    Created a chunk of size 1083, which is longer than the specified 1000
    

    3477
    

Then embed chunks and upload them to the DeepLake.

This can take several minutes. 


```python
from langchain.embeddings.openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()
embeddings
```




    OpenAIEmbeddings(client=<class 'openai.api_resources.embedding.Embedding'>, model='text-embedding-ada-002', document_model_name='text-embedding-ada-002', query_model_name='text-embedding-ada-002', embedding_ctx_length=8191, openai_api_key=None, openai_organization=None, allowed_special=set(), disallowed_special='all', chunk_size=1000, max_retries=6)




```python
from langchain.vectorstores import DeepLake

db = DeepLake.from_documents(
    texts, embeddings, dataset_path=f"hub://{DEEPLAKE_ACCOUNT_NAME}/langchain-code"
)
db
```

### Question Answering
First load the dataset, construct the retriever, then construct the Conversational Chain


```python
db = DeepLake(
    dataset_path=f"hub://{DEEPLAKE_ACCOUNT_NAME}/langchain-code",
    read_only=True,
    embedding_function=embeddings,
)
```

    -

    This dataset can be visualized in Jupyter Notebook by ds.visualize() or at https://app.activeloop.ai/user_name/langchain-code
    
    

    /

    hub://user_name/langchain-code loaded successfully.
    
    

    Deep Lake Dataset in hub://user_name/langchain-code already exists, loading from the storage
    

    Dataset(path='hub://user_name/langchain-code', read_only=True, tensors=['embedding', 'ids', 'metadata', 'text'])
    
      tensor     htype      shape       dtype  compression
      -------   -------    -------     -------  ------- 
     embedding  generic  (3477, 1536)  float32   None   
        ids      text     (3477, 1)      str     None   
     metadata    json     (3477, 1)      str     None   
       text      text     (3477, 1)      str     None   
    


```python
retriever = db.as_retriever()
retriever.search_kwargs["distance_metric"] = "cos"
retriever.search_kwargs["fetch_k"] = 20
retriever.search_kwargs["maximal_marginal_relevance"] = True
retriever.search_kwargs["k"] = 20
```

You can also specify user defined functions using [Deep Lake filters](https://docs.deeplake.ai/en/latest/deeplake.core.dataset.html#deeplake.core.dataset.Dataset.filter)


```python
def filter(x):
    # filter based on source code
    if "something" in x["text"].data()["value"]:
        return False

    # filter based on path e.g. extension
    metadata = x["metadata"].data()["value"]
    return "only_this" in metadata["source"] or "also_that" in metadata["source"]


### turn on below for custom filtering
# retriever.search_kwargs['filter'] = filter
```


```python
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain

model = ChatOpenAI(model_name="gpt-3.5-turbo")  # 'ada' 'gpt-3.5-turbo' 'gpt-4',
qa = ConversationalRetrievalChain.from_llm(model, retriever=retriever)
```


```python
questions = [
    "What is the class hierarchy?",
    # "What classes are derived from the Chain class?",
    # "What classes and functions in the ./langchain/utilities/ forlder are not covered by unit tests?",
    # "What one improvement do you propose in code in relation to the class herarchy for the Chain class?",
]
chat_history = []

for question in questions:
    result = qa({"question": question, "chat_history": chat_history})
    chat_history.append((question, result["answer"]))
    print(f"-> **Question**: {question} \n")
    print(f"**Answer**: {result['answer']} \n")
```

-> **Question**: What is the class hierarchy? 

**Answer**: There are several class hierarchies in the provided code, so I'll list a few:

1. `BaseModel` -> `ConstitutionalPrinciple`: `ConstitutionalPrinciple` is a subclass of `BaseModel`.
2. `BasePromptTemplate` -> `StringPromptTemplate`, `AIMessagePromptTemplate`, `BaseChatPromptTemplate`, `ChatMessagePromptTemplate`, `ChatPromptTemplate`, `HumanMessagePromptTemplate`, `MessagesPlaceholder`, `SystemMessagePromptTemplate`, `FewShotPromptTemplate`, `FewShotPromptWithTemplates`, `Prompt`, `PromptTemplate`: All of these classes are subclasses of `BasePromptTemplate`.
3. `APIChain`, `Chain`, `MapReduceDocumentsChain`, `MapRerankDocumentsChain`, `RefineDocumentsChain`, `StuffDocumentsChain`, `HypotheticalDocumentEmbedder`, `LLMChain`, `LLMBashChain`, `LLMCheckerChain`, `LLMMathChain`, `LLMRequestsChain`, `PALChain`, `QAWithSourcesChain`, `VectorDBQAWithSourcesChain`, `VectorDBQA`, `SQLDatabaseChain`: All of these classes are subclasses of `Chain`.
4. `BaseLoader`: `BaseLoader` is a subclass of `ABC`.
5. `BaseTracer` -> `ChainRun`, `LLMRun`, `SharedTracer`, `ToolRun`, `Tracer`, `TracerException`, `TracerSession`: All of these classes are subclasses of `BaseTracer`.
6. `OpenAIEmbeddings`, `HuggingFaceEmbeddings`, `CohereEmbeddings`, `JinaEmbeddings`, `LlamaCppEmbeddings`, `HuggingFaceHubEmbeddings`, `TensorflowHubEmbeddings`, `SagemakerEndpointEmbeddings`, `HuggingFaceInstructEmbeddings`, `SelfHostedEmbeddings`, `SelfHostedHuggingFaceEmbeddings`, `SelfHostedHuggingFaceInstructEmbeddings`, `FakeEmbeddings`, `AlephAlphaAsymmetricSemanticEmbedding`, `AlephAlphaSymmetricSemanticEmbedding`: All of these classes are subclasses of `BaseLLM`. 


-> **Question**: What classes are derived from the Chain class? 

**Answer**: There are multiple classes that are derived from the Chain class. Some of them are:
- APIChain
- AnalyzeDocumentChain
- ChatVectorDBChain
- CombineDocumentsChain
- ConstitutionalChain
- ConversationChain
- GraphQAChain
- HypotheticalDocumentEmbedder
- LLMChain
- LLMCheckerChain
- LLMRequestsChain
- LLMSummarizationCheckerChain
- MapReduceChain
- OpenAPIEndpointChain
- PALChain
- QAWithSourcesChain
- RetrievalQA
- RetrievalQAWithSourcesChain
- SequentialChain
- SQLDatabaseChain
- TransformChain
- VectorDBQA
- VectorDBQAWithSourcesChain

There might be more classes that are derived from the Chain class as it is possible to create custom classes that extend the Chain class.


-> **Question**: What classes and functions in the ./langchain/utilities/ forlder are not covered by unit tests? 

**Answer**: All classes and functions in the `./langchain/utilities/` folder seem to have unit tests written for them. 



