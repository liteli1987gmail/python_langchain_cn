# DocArrayHnswSearch

>[DocArrayHnswSearch](https://docs.docarray.org/user_guide/storing/index_hnswlib/) 是由[Docarray](https://docs.docarray.org/)提供的轻量级文档索引实现，完全在本地运行，最适合中小型数据集。它将向量存储在[hnswlib](https://github.com/nmslib/hnswlib)中的磁盘上，并将所有其他数据存储在[SQLite](https://www.sqlite.org/index.html)中。

这个笔记本展示了与`DocArrayHnswSearch`相关的功能的使用方法。

## 设置

取消下面的单元格的注释以安装docarray并获取/设置您的OpenAI API密钥（如果您尚未这样做）。

```python
# !pip install "docarray[hnswlib]"
```

```python
# 获取OpenAI令牌：https://platform.openai.com/account/api-keys
# import os
# from getpass import getpass

# OPENAI_API_KEY = getpass()
# os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
```

## 使用DocArrayHnswSearch

```python
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import DocArrayHnswSearch
from langchain.document_loaders import TextLoader
```

```python
documents = TextLoader("../../../state_of_the_union.txt").load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()

db = DocArrayHnswSearch.from_documents(
    docs, embeddings, work_dir="hnswlib_store/", n_dim=1536
)
```

### 相似性搜索

```python
query = "What did the president say about Ketanji Brown Jackson"
docs = db.similarity_search(query)
```

```python
print(docs[0].page_content)
```

    今晚。我呼吁参议院：通过《自由投票法案》。通过约翰·路易斯投票权法案。同时，通过公开法案，以便美国人民可以知道谁在为我们的选举提供资金。

    今晚，我想向一个致力于为这个国家服务的人致以敬意：史蒂芬·布雷耶法官——一位退伍军人、宪法学者和美国最高法院的离任法官。布雷耶法官，感谢您的服务。

    作为总统，最重要的宪法责任之一是提名某人担任美国最高法院的职位。

    4天前，我提名了上诉法院法官凯坦吉·布朗·杰克逊。他是我们国家顶级的法律智慧之一，将继续布雷耶法官的卓越传统。

### 带有分数的相似性搜索

返回的距离分数是余弦距离。因此，得分越低越好。

```python
docs = db.similarity_search_with_score(query)
```

```python
docs[0]
```




    (Document(page_content='Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections. \n\nTonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. \n\nOne of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. \n\nAnd I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.', metadata={}),
     0.36962226)




```python
import shutil

# 删除目录
shutil.rmtree("hnswlib_store")
```
