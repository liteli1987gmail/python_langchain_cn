# Hologres

>[Hologres](https://www.alibabacloud.com/help/en/hologres/latest/introduction) 是由阿里云开发的统一实时数据仓库服务。您可以使用Hologres实时写入、更新、处理和分析大量数据。
>Hologres支持标准SQL语法，与PostgreSQL兼容，并支持大多数PostgreSQL函数。Hologres支持高达PB级的数据的联机分析处理（OLAP）和即席分析，并提供高并发和低延迟的在线数据服务。

>Hologres通过采用[Proxima](https://www.alibabacloud.com/help/en/hologres/latest/vector-processing)提供**矢量数据库**功能。
>Proxima是阿里巴巴达摩院开发的高性能软件库，允许您搜索矢量的最近邻居。 Proxima提供了比Faiss等类似开源软件更高的稳定性和性能。 Proxima允许您以高吞吐量和低延迟搜索相似的文本或图像嵌入。 Hologres与Proxima深度集成，提供高性能的矢量搜索服务。

本笔记本展示了使用与`Hologres Proxima`矢量数据库相关的功能。
单击[此处](https://www.alibabacloud.com/zh/product/hologres)快速部署Hologres云实例。


```python
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Hologres
```

通过调用OpenAI API拆分文档并获取嵌入


```python
from langchain.document_loaders import TextLoader

loader = TextLoader("../../../state_of_the_union.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
```

通过设置相关环境变量连接到Hologres
```
export PG_HOST={host}
export PG_PORT={port} # 可选，默认为80
export PG_DATABASE={db_name} # 可选，默认为postgres
export PG_USER={username}
export PG_PASSWORD={password}
```

然后将您的嵌入和文档存储到Hologres中


```python
import os

connection_string = Hologres.connection_string_from_db_params(
    host=os.environ.get("PGHOST", "localhost"),
    port=int(os.environ.get("PGPORT", "80")),
    database=os.environ.get("PGDATABASE", "postgres"),
    user=os.environ.get("PGUSER", "postgres"),
    password=os.environ.get("PGPASSWORD", "postgres"),
)

vector_db = Hologres.from_documents(
    docs,
    embeddings,
    connection_string=connection_string,
    table_name="langchain_example_embeddings",
)
```

查询并检索数据


```python
query = "What did the president say about Ketanji Brown Jackson"
docs = vector_db.similarity_search(query)
```


```python
print(docs[0].page_content)
```

    Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections. 
    
    Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. 
    
    One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. 
    
    And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.
    
