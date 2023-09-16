# Airtable

```python
! pip install pyairtable
```

```python
from langchain.document_loaders import AirtableLoader
```

- 获取[API key](https://support.airtable.com/docs/creating-and-using-api-keys-and-access-tokens)。
- 获取[base ID](https://airtable.com/developers/web/api/introduction)。
- 从表格URL获取[table ID](https://www.highviewapps.com/kb/where-can-i-find-the-airtable-base-id-and-table-id/#:~:text=Both%20the%20Airtable%20Base%20ID,URL%20that%20begins%20with%20tbl)。

```python
api_key = "xxx"
base_id = "xxx"
table_id = "xxx"
```

```python
loader = AirtableLoader(api_key, table_id, base_id)
docs = loader.load()
```

返回每行表格数据为`dict`。

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
