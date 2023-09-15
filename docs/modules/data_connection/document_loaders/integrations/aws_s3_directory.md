# AWS S3 Directory

>[Amazon Simple Storage Service (Amazon S3)](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-folders.html) is an object storage service

>[AWS S3 Directory](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-folders.html)

This covers how to load document objects from an `AWS S3 Directory` object.


```python
#!pip install boto3
```


```python
from langchain.document_loaders import S3DirectoryLoader
```


```python
loader = S3DirectoryLoader("testing-hwc")
```


```python
loader.load()
```

## Specifying a prefix
You can also specify a prefix for more finegrained control over what files to load.


```python
loader = S3DirectoryLoader("testing-hwc", prefix="fake")
```


```python
loader.load()
```




    [Document(page_content='Lorem ipsum dolor sit amet.', lookup_str='', metadata={'source': '/var/folders/y6/8_bzdg295ld6s1_97_12m4lr0000gn/T/tmpujbkzf_l/fake.docx'}, lookup_index=0)]




```python

```
