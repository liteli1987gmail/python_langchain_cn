# Azure Blob Storage Container
>[Azure Blob Storage](https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blobs-introduction)是微软的云端对象存储解决方案。Blob Storage专为存储大量非结构化数据进行了优化。非结构化数据是不符合特定数据模型或定义的数据，例如文本或二进制数据。

Azure Blob Storage设计用于：
- 直接向浏览器提供图像或文档。
- 存储用于分布式访问的文件。
- 流式传输视频和音频。
- 写入日志文件。
- 存储用于备份和还原、灾难恢复和归档的数据。
- 存储用于本地或Azure托管服务的分析数据。

本篇笔记本介绍了如何从Azure Blob Storage的容器中加载文档对象。


```python
#!pip install azure-storage-blob
```


```python
from langchain.document_loaders import AzureBlobStorageContainerLoader
```


```python
loader = AzureBlobStorageContainerLoader(conn_str="<conn_str>", container="<container>")
```


```python
loader.load()
```


[Document(page_content='Lorem ipsum dolor sit amet.', lookup_str='', metadata={'source': '/var/folders/y6/8_bzdg295ld6s1_97_12m4lr0000gn/T/tmpaa9xl6ch/fake.docx'}, lookup_index=0)]



## Specifying a prefix
You can also specify a prefix for more finegrained control over what files to load.


```python
loader = AzureBlobStorageContainerLoader(
    conn_str="<conn_str>", container="<container>", prefix="<prefix>"
)
```


```python
loader.load()
```


[Document(page_content='Lorem ipsum dolor sit amet.', lookup_str='', metadata={'source': '/var/folders/y6/8_bzdg295ld6s1_97_12m4lr0000gn/T/tmpujbkzf_l/fake.docx'}, lookup_index=0)]



```python

```