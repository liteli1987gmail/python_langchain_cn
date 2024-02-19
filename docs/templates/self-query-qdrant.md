# self-query-qdrant

这个模板使用Qdrant和OpenAI进行[自查询](https://python.langchain.com/docs/modules/data_connection/retrievers/self_query/)。默认情况下，它使用一个包含10个文档的人工数据集，但你可以用自己的数据集替换它。

## 环境设置

设置`OPENAI_API_KEY`环境变量以访问OpenAI模型。

将`QDRANT_URL`设置为你的Qdrant实例的URL。如果你使用[Qdrant Cloud](https://cloud.qdrant.io)，你还需要设置`QDRANT_API_KEY`环境变量。如果你没有设置它们中的任何一个，模板将尝试连接到本地的Qdrant实例`http://localhost:6333`。

```shell
export QDRANT_URL=
export QDRANT_API_KEY=

export OPENAI_API_KEY=
```

## 使用方法

要使用这个包，首先安装LangChain CLI：

```shell
pip install -U "langchain-cli[serve]"
```

创建一个新的LangChain项目，并将这个包作为唯一的包安装：

```shell
langchain app new my-app --package self-query-qdrant
```

要将其添加到现有项目中，请运行：

```shell
langchain app add self-query-qdrant
```

### 默认值

在启动服务器之前，你需要创建一个Qdrant集合并对文档进行索引。可以通过运行以下命令来完成：

```python
from self_query_qdrant.chain import initialize

initialize()
```

将以下代码添加到你的`app/server.py`文件中：

```python
from self_query_qdrant.chain import chain

add_routes(app, chain, path="/self-query-qdrant")
```

默认数据集包含10个关于菜肴的文档，以及它们的价格和餐厅信息。你可以在`packages/self-query-qdrant/self_query_qdrant/defaults.py`文件中找到这些文档。下面是其中一个文档的示例：

```python
from langchain.schema import Document

Document(
    page_content="Spaghetti with meatballs and tomato sauce",
    metadata={
        "price": 12.99,
        "restaurant": {
            "name": "Olive Garden",
            "location": ["New York", "Chicago", "Los Angeles"],
        },
    },
)
```

自查询允许对文档进行语义搜索，并根据元数据进行一些附加过滤。例如，你可以搜索价格低于15美元并在纽约提供的菜肴。

### 自定义

上面的所有示例都假设你只想使用默认值启动模板。如果你想自定义模板，可以通过在`app/server.py`文件中向`create_chain`函数传递参数来实现：

```python
from langchain_community.llms import Cohere
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains.query_constructor.schema import AttributeInfo

from self_query_qdrant.chain import create_chain

chain = create_chain(
    llm=Cohere(),
    embeddings=HuggingFaceEmbeddings(),
    document_contents="Descriptions of cats, along with their names and breeds.",
    metadata_field_info=[
        AttributeInfo(name="name", description="Name of the cat", type="string"),
        AttributeInfo(name="breed", description="Cat's breed", type="string"),
    ],
    collection_name="cats",
)
```

对于创建Qdrant集合并对文档进行索引的`initialize`函数，也是一样的：

```python
from langchain.schema import Document
from langchain_community.embeddings import HuggingFaceEmbeddings

from self_query_qdrant.chain import initialize

initialize(
    embeddings=HuggingFaceEmbeddings(),
    collection_name="cats",
    documents=[
        Document(
            page_content="A mean lazy old cat who destroys furniture and eats lasagna",
            metadata={"name": "Garfield", "breed": "Tabby"},
        ),
        ...
    ]
)
```

该模板灵活且易于用于不同的文档集。

### LangSmith

（可选）如果你可以访问LangSmith，请配置它以帮助跟踪、监视和调试LangChain应用程序。如果你没有访问权限，请跳过此部分。

```shell
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=<your-api-key>
export LANGCHAIN_PROJECT=<your-project>  # 如果未指定，默认为"default"
```

如果你在这个目录中，你可以直接启动一个LangServe实例：

```shell
langchain serve
```

### 本地服务器

这将启动一个在本地运行的FastAPI服务器，地址为[http://localhost:8000](http://localhost:8000)。

你可以在[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)上查看所有模板，在[http://127.0.0.1:8000/self-query-qdrant/playground](http://127.0.0.1:8000/self-query-qdrant/playground)上访问playground。

从代码中访问模板：

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/self-query-qdrant")
```
