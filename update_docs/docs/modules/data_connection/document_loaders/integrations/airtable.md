# Airtable


```python
! pip install pyairtable
```


```python
from langchain.document_loaders import AirtableLoader
```

* Get your API key [here](https://support.airtable.com/docs/creating-and-using-api-keys-and-access-tokens).
* Get ID of your base [here](https://airtable.com/developers/web/api/introduction).
* Get your table ID from the table url as shown [here](https://www.highviewapps.com/kb/where-can-i-find-the-airtable-base-id-and-table-id/#:~:text=Both%20the%20Airtable%20Base%20ID,URL%20that%20begins%20with%20tbl).


```python
api_key = "xxx"
base_id = "xxx"
table_id = "xxx"
```


```python
loader = AirtableLoader(api_key, table_id, base_id)
docs = loader.load()
```

Returns each table row as `dict`.


```python
len(docs)
```




    3




```python
eval(docs[0].page_content)
```




    {'id': 'recF3GbGZCuh9sXIQ',
     'createdTime': '2023-06-09T04:47:21.000Z',
     'fields': {'Priority': 'High',
      'Status': 'In progress',
      'Name': 'Document Splitters'}}


