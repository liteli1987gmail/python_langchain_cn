# Email

This notebook shows how to load email (`.eml`) or `Microsoft Outlook` (`.msg`) files.

## Using Unstructured


```python
#!pip install unstructured
```


```python
from langchain.document_loaders import UnstructuredEmailLoader
```


```python
loader = UnstructuredEmailLoader("example_data/fake-email.eml")
```


```python
data = loader.load()
```


```python
data
```




    [Document(page_content='This is a test email to use for unit tests.\n\nImportant points:\n\nRoses are red\n\nViolets are blue', metadata={'source': 'example_data/fake-email.eml'})]



### Retain Elements

Under the hood, Unstructured creates different "elements" for different chunks of text. By default we combine those together, but you can easily keep that separation by specifying `mode="elements"`.


```python
loader = UnstructuredEmailLoader("example_data/fake-email.eml", mode="elements")
```


```python
data = loader.load()
```


```python
data[0]
```




    Document(page_content='This is a test email to use for unit tests.', lookup_str='', metadata={'source': 'example_data/fake-email.eml'}, lookup_index=0)



## Using OutlookMessageLoader


```python
#!pip install extract_msg
```


```python
from langchain.document_loaders import OutlookMessageLoader
```


```python
loader = OutlookMessageLoader("example_data/fake-email.msg")
```


```python
data = loader.load()
```


```python
data[0]
```




    Document(page_content='This is a test email to experiment with the MS Outlook MSG Extractor\r\n\r\n\r\n-- \r\n\r\n\r\nKind regards\r\n\r\n\r\n\r\n\r\nBrian Zhou\r\n\r\n', metadata={'subject': 'Test for TIF files', 'sender': 'Brian Zhou <brizhou@gmail.com>', 'date': 'Mon, 18 Nov 2013 16:26:24 +0800'})




```python

```
