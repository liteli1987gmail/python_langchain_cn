# Azure Cognitive Search

# 安装 Azure Cognitive Search SDK


```python
!pip install --index-url=https://pkgs.dev.azure.com/azure-sdk/public/_packaging/azure-sdk-for-python/pypi/simple/ azure-search-documents==11.4.0a20230509004
!pip install azure-identity
```

## 导入所需库


```python
import os, json
import openai
from dotenv import load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.schema import BaseRetriever
from langchain.vectorstores.azuresearch import AzureSearch
```

## 配置 OpenAI 设置
配置 OpenAI 设置以使用 Azure OpenAI 或 OpenAI


```python
# 从 .env 文件中加载环境变量使用 load_dotenv():
load_dotenv()

openai.api_type = "azure"
openai.api_base = "YOUR_OPENAI_ENDPOINT"
openai.api_version = "2023-05-15"
openai.api_key = "YOUR_OPENAI_API_KEY"
model: str = "text-embedding-ada-002"
```

## 配置向量存储设置
 
使用环境变量设置向量存储设置:


```python
vector_store_address: str = "YOUR_AZURE_SEARCH_ENDPOINT"
vector_store_password: str = "YOUR_AZURE_SEARCH_ADMIN_KEY"
index_name: str = "langchain-vector-demo"
```

## 创建嵌入和向量存储实例
 
创建 OpenAIEmbeddings 和 AzureSearch 类的实例:


```python
embeddings: OpenAIEmbeddings = OpenAIEmbeddings(model=model, chunk_size=1)
vector_store: AzureSearch = AzureSearch(
    azure_search_endpoint=vector_store_address,
    azure_search_key=vector_store_password,
    index_name=index_name,
    embedding_function=embeddings.embed_query,
)
```

## 将文本和嵌入插入向量存储
 
将 JSON 数据中的文本和元数据添加到向量存储:


```python
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter

loader = TextLoader("../../../state_of_the_union.txt", encoding="utf-8")

documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

vector_store.add_documents(documents=docs)
```

## 执行向量相似性搜索
 
使用 similarity_search() 方法执行纯向量相似性搜索:


```python
# 执行相似性搜索
docs = vector_store.similarity_search(
    query="总统对 Ketanji Brown Jackson 说了什么",
    k=3,
    search_type="similarity",
)
print(docs[0].page_content)
```

    Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections. 
    
    Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. 
    
    One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. 
    
    And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.
    
## 执行混合搜索

使用 hybrid_search() 方法执行混合搜索:


```python
# 执行混合搜索
docs = vector_store.similarity_search(
    query="总统对Ketanji Brown Jackson 说了什么", k=3
)
print(docs[0].page_content)
```

    Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections. 
    
    Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. 
    
    One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. 
    
    And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.
    
