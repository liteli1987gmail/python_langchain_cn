# Azure Blob Storage File

>[Azure Files](https://learn.microsoft.com/en-us/azure/storage/files/storage-files-introduction) offers fully managed file shares in the cloud that are accessible via the industry standard Server Message Block (`SMB`) protocol, Network File System (`NFS`) protocol, and `Azure Files REST API`.

This covers how to load document objects from a Azure Files.


```python
#!pip install azure-storage-blob
```


```python
from langchain.document_loaders import AzureBlobStorageFileLoader
```


```python
loader = AzureBlobStorageFileLoader(
    conn_str="<connection string>",
    container="<container name>",
    blob_name="<blob name>",
)
```


```python
loader.load()
```




    [Document(page_content='Lorem ipsum dolor sit amet.', lookup_str='', metadata={'source': '/var/folders/y6/8_bzdg295ld6s1_97_12m4lr0000gn/T/tmpxvave6wl/fake.docx'}, lookup_index=0)]




```python

```
