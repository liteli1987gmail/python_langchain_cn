# Notion DB 1/2

>[Notion](https://www.notion.so/) is a collaboration platform with modified Markdown support that integrates kanban boards, tasks, wikis and databases. It is an all-in-one workspace for notetaking, knowledge and data management, and project and task management.

This notebook covers how to load documents from a Notion database dump.

In order to get this notion dump, follow these instructions:

## 🧑 Instructions for ingesting your own dataset

Export your dataset from Notion. You can do this by clicking on the three dots in the upper right hand corner and then clicking `Export`.

When exporting, make sure to select the `Markdown & CSV` format option.

This will produce a `.zip` file in your Downloads folder. Move the `.zip` file into this repository.

Run the following command to unzip the zip file (replace the `Export...` with your own file name as needed).

```shell
unzip Export-d3adfe0f-3131-4bf3-8987-a52017fc1bae.zip -d Notion_DB
```

Run the following command to ingest the data.


```python
from langchain.document_loaders import NotionDirectoryLoader
```


```python
loader = NotionDirectoryLoader("Notion_DB")
```


```python
docs = loader.load()
```
