# Google Cloud Storage文件

>[Google Cloud Storage](https://en.wikipedia.org/wiki/Google_Cloud_Storage)是用于存储非结构化数据的托管服务。

这涵盖了如何从`Google Cloud Storage（GCS）文件对象（blob）`加载文档对象的内容。


```python
# !pip install google-cloud-storage
```


```python
from langchain.document_loaders import GCSFileLoader
```


```python
loader = GCSFileLoader(project_name="aist", bucket="testing-hwc", blob="fake.docx")
```


```python
loader.load()
```

    /Users/harrisonchase/workplace/langchain/.venv/lib/python3.10/site-packages/google/auth/_default.py:83: UserWarning: 您的应用程序使用了来自Google Cloud SDK的最终用户凭据进行身份验证，而没有配额项目。您可能会收到"配额超过限制"或"API未启用"的错误。我们建议您重新运行`gcloud auth application-default login`并确保添加了配额项目。或者您可以改用服务帐号。有关服务帐号的更多信息，请参阅https://cloud.google.com/docs/authentication/
      warnings.warn(_CLOUD_SDK_CREDENTIALS_WARNING)
    




    [Document(page_content='Lorem ipsum dolor sit amet.', lookup_str='', metadata={'source': '/var/folders/y6/8_bzdg295ld6s1_97_12m4lr0000gn/T/tmp3srlf8n8/fake.docx'}, lookup_index=0)]




```python

```
