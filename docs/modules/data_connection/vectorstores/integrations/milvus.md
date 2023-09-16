# Milvus

>[Milvus](https://milvus.io/docs/overview.md) 是一个存储、索引和管理由深度神经网络和其他机器学习(ML)模型生成的大规模嵌入向量的数据库。

本笔记本展示了与Milvus向量数据库相关的功能的使用方法。

要运行，您应该有一个[运行中的Milvus实例](https://milvus.io/docs/install_standalone-docker.md)。


```python
!pip install pymilvus
```

我们想要使用OpenAIEmbeddings，所以我们必须获取OpenAI API密钥。


```python
import os
import getpass

os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API密钥:")
```

    OpenAI API密钥:········
    


```python
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Milvus
from langchain.document_loaders import TextLoader
```


```python
from langchain.document_loaders import TextLoader

loader = TextLoader("../../../state_of_the_union.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
```


```python
vector_db = Milvus.from_documents(
    docs,
    embeddings,
    connection_args={"host": "127.0.0.1", "port": "19530"},
)
```


```python
query = "总统对Ketanji Brown Jackson说了什么"
docs = vector_db.similarity_search(query)
```


```python
docs[0].page_content
```




    '今晚。我呼吁参议院:通过"自由投票法案"。通过"约翰·刘易斯选举权法案"。而且你们在这方面时，通过"公开法案"，以便美国人民可以知道谁资助了我们的选举。 \n\n今晚，我想向一个致力于为这个国家服务的人表示敬意:司法部长斯蒂芬·布雷耶——一位陆军退伍军人、宪法学者和即将退休的美国最高法院法官。布雷耶法官，感谢您的服务。 \n\n总统最重要的宪法责任之一是提名人担任美国最高法院法官。 \n\n而我在4天前就这样做了，当我提名上诉法院法官Ketanji Brown Jackson时。她是我们国家最优秀的法律智慧之一，将继续布雷耶法官的卓越传统。'




```python

```
