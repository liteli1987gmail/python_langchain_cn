# Google Cloud Storage目录

>[Google Cloud Storage](https://en.wikipedia.org/wiki/Google_Cloud_Storage)是用于存储非结构化数据的托管服务。

这涵盖了如何从`Google Cloud Storage（GCS）目录（存储桶）`加载文档对象的内容。


```python
# !pip install google-cloud-storage
```


```python
from langchain.document_loaders import GCSDirectoryLoader
```


```python
loader = GCSDirectoryLoader(project_name="aist", bucket="testing-hwc")
```


```python
loader.load()
```

    /Users/harrisonchase/workplace/langchain/.venv/lib/python3.10/site-packages/google/auth/_default.py:83: UserWarning: 您的应用程序使用了来自Google Cloud SDK的最终用户凭据进行身份验证，而没有配额项目。您可能会收到"配额超过限制"或"API未启用"的错误。我们建议您重新运行`gcloud auth application-default login`并确保添加了配额项目。或者您可以改用服务帐号。有关服务帐号的更多信息，请参阅https://cloud.google.com/docs/authentication/
      warnings.warn(_CLOUD_SDK_CREDENTIALS_WARNING)
    /Users/harrisonchase/workplace/langchain/.venv/lib/python3.10/site-packages/google/auth/_default.py:83: UserWarning: 您的应用程序使用了来自Google Cloud SDK的最终用户凭据进行身份验证，而没有配额项目。您可能会收到"配额超过限制"或"API未启用"的错误。我们建议您重新运行`gcloud auth application-default login`并确保添加了配额项目。或者您可以改用服务帐号。有关服务帐号的更多信息，请参阅https://cloud.google.com/docs/authentication/
      warnings.warn(_CLOUD_SDK_CREDENTIALS_WARNING)
    




    [Document(page_content='Lorem ipsum dolor sit amet.', lookup_str='', metadata={'source': '/var/folders/y6/8_bzdg295ld6s1_97_12m4lr0000gn/T/tmpz37njh7u/fake.docx'}, lookup_index=0)]



## 指定前缀
您还可以指定前缀以更精细地控制要加载的文件。


```python
loader = GCSDirectoryLoader(project_name="aist", bucket="testing-hwc", prefix="fake")
```


```python
loader.load()
```

    /Users/harrisonchase/workplace/langchain/.venv/lib/python3.10/site-packages/google/auth/_default.py:83: UserWarning: 您的应用程序使用了来自Google Cloud SDK的最终用户凭据进行身份验证，而没有配额项目。您可能会收到"配额超过限制"或"API未启用"的错误。我们建议您重新运行`gcloud auth application-default login`并确保添加了配额项目。或者您可以改用服务帐号。有关服务帐号的更多信息，请参阅https://cloud.google.com/docs/authentication/
      warnings.warn(_CLOUD_SDK_CREDENTIALS_WARNING)
    /Users/harrisonchase/workplace/langchain/.venv/lib/python3.10/site-packages/google/auth/_default.py:83: UserWarning: 您的应用程序使用了来自Google Cloud SDK的最终用户凭据进行身份验证，而没有配额项目。您可能会收到"配额超过限制"或"API未启用"的错误。我们建议您重新运行`gcloud auth application-default login`并确保添加了配额项目。或者您可以改用服务帐号。有关服务帐号的更多信息，请参阅https://cloud.google.com/docs/authentication/
      warnings.warn(_CLOUD_SDK_CREDENTIALS_WARNING)
    




    [Document(page_content='Lorem ipsum dolor sit amet.', lookup_str='', metadata={'source': '/var/folders/y6/8_bzdg295ld6s1_97_12m4lr0000gn/T/tmpylg6291i/fake.docx'}, lookup_index=0)]




```python

```
