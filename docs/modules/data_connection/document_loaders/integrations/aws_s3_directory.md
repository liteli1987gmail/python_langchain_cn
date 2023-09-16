# AWS S3 Directory

[Amazon Simple Storage Service (Amazon S3)](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-folders.html)是一个对象存储服务。

[AWS S3 Directory](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-folders.html)

本文介绍了如何从`AWS S3 Directory`对象加载文档对象。

```python
!pip install boto3
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

## 指定前缀

您还可以指定一个前缀，以更精细地控制要加载的文件。

```python
loader = S3DirectoryLoader("testing-hwc", prefix="fake")
```



```python
loader.load()
```





    [Document(page_content='Lorem ipsum dolor sit amet.', lookup_str='', metadata={'source': '/var/folders/y6/8_bzdg295ld6s1_97_12m4lr0000gn/T/tmpujbkzf_l/fake.docx'}, lookup_index=0)]





```python

```