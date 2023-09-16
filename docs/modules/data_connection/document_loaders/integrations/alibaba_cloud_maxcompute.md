# 阿里巴巴云MaxCompute

> [阿里巴巴云MaxCompute](https://www.alibabacloud.com/product/maxcompute)（以前称为ODPS）是一个通用的、完全托管的、多租户的大规模数据存储和处理平台。MaxCompute支持各种数据导入解决方案和分布式计算模型，使用用户能够有效地查询海量数据，降低生产成本，确保数据安全。

`MaxComputeLoader`允许您执行MaxCompute SQL查询并将结果加载为每行一个文档。

```python
!pip install pyodps
```

    Collecting pyodps
      Downloading pyodps-0.11.4.post0-cp39-cp39-macosx_10_9_universal2.whl (2.0 MB)
    [2K     [90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m2.0/2.0 MB[0m [31m1.7 MB/s[0m eta [36m0:00:00[0m00:01[0m00:01[0m0m
    [?25hRequirement already satisfied: charset-normalizer>=2 in /Users/newboy/anaconda3/envs/langchain/lib/python3.9/site-packages (from pyodps) (3.1.0)
    Requirement already satisfied: urllib3<2.0,>=1.26.0 in /Users/newboy/anaconda3/envs/langchain/lib/python3.9/site-packages (from pyodps) (1.26.15)
    Requirement already satisfied: idna>=2.5 in /Users/newboy/anaconda3/envs/langchain/lib/python3.9/site-packages (from pyodps) (3.4)
    Requirement already satisfied: certifi>=2017.4.17 in /Users/newboy/anaconda3/envs/langchain/lib/python3.9/site-packages (from pyodps) (2023.5.7)
    Installing collected packages: pyodps
    Successfully installed pyodps-0.11.4.post0

## 基本方法
要实例化加载器，您需要一个要执行的SQL查询、MaxCompute的终端节点和项目名称，以及您的访问ID和秘密访问密钥。访问ID和秘密访问密钥可以直接通过`access_id`和`secret_access_key`参数传递，也可以设置为环境变量`MAX_COMPUTE_ACCESS_ID`和`MAX_COMPUTE_SECRET_ACCESS_KEY`。

```python
from langchain.document_loaders import MaxComputeLoader
```

```python
base_query = """
SELECT *
FROM (
    SELECT 1 AS id, 'content1' AS content, 'meta_info1' AS meta_info
    UNION ALL
    SELECT 2 AS id, 'content2' AS content, 'meta_info2' AS meta_info
    UNION ALL
    SELECT 3 AS id, 'content3' AS content, 'meta_info3' AS meta_info
) mydata;
"""
```

```python
endpoint = "<ENDPOINT>"
project = "<PROJECT>"
ACCESS_ID = "<ACCESS ID>"
SECRET_ACCESS_KEY = "<SECRET ACCESS KEY>"
```

```python
loader = MaxComputeLoader.from_params(
    base_query,
    endpoint,
    project,
    access_id=ACCESS_ID,
    secret_access_key=SECRET_ACCESS_KEY,
)
data = loader.load()
```

```python
print(data)
```

    [Document(page_content='id: 1\ncontent: content1\nmeta_info: meta_info1', metadata={}), Document(page_content='id: 2\ncontent: content2\nmeta_info: meta_info2', metadata={}), Document(page_content='id: 3\ncontent: content3\nmeta_info: meta_info3', metadata={})]

```python
print(data[0].page_content)
```

    id: 1
    content: content1
    meta_info: meta_info1

```python
print(data[0].metadata)
```

    {}

## 指定哪些列是内容，哪些列是元数据
您可以使用`page_content_columns`和`metadata_columns`参数配置将哪个子列加载为文档的内容，哪个子列加载为元数据。

```python
loader = MaxComputeLoader.from_params(
    base_query,
    endpoint,
    project,
    page_content_columns=["content"],  # 指定文档页内容
    metadata_columns=["id", "meta_info"],  # 指定文档元数据
    access_id=ACCESS_ID,
    secret_access_key=SECRET_ACCESS_KEY,
)
data = loader.load()
```

```python
print(data[0].page_content)
```

    content: content1
    


```python
print(data[0].metadata)
```

    {'id': 1, 'meta_info': 'meta_info1'}
    
