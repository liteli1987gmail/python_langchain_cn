# Notion DB 2/2

>[Notion](https://www.notion.so/) is a collaboration platform with modified Markdown support that integrates kanban boards, tasks, wikis and databases. It is an all-in-one workspace for notetaking, knowledge and data management, and project and task management.

`NotionDBLoader` is a Python class for loading content from a `Notion` database. It retrieves pages from the database, reads their content, and returns a list of Document objects.

## Requirements

- A `Notion` Database
- Notion Integration Token

## Setup

### 1. Create a Notion Table Database
Create a new table database in Notion. You can add any column to the database and they will be treated as metadata. For example you can add the following columns:

- Title: set Title as the default property.
- Categories: A Multi-select property to store categories associated with the page.
- Keywords: A Multi-select property to store keywords associated with the page.

Add your content to the body of each page in the database. The NotionDBLoader will extract the content and metadata from these pages.

## 2. Create a Notion Integration
To create a Notion Integration, follow these steps:

1. Visit the [Notion Developers](https://www.notion.com/my-integrations) page and log in with your Notion account.
2. Click on the "+ New integration" button.
3. Give your integration a name and choose the workspace where your database is located.
4. Select the require capabilities, this extension only need the Read content capability
5. Click the "Submit" button to create the integration.
Once the integration is created, you'll be provided with an `Integration Token (API key)`. Copy this token and keep it safe, as you'll need it to use the NotionDBLoader.

### 3. Connect the Integration to the Database
To connect your integration to the database, follow these steps:

1. Open your database in Notion.
2. Click on the three-dot menu icon in the top right corner of the database view.
3. Click on the "+ New integration" button.
4. Find your integration, you may need to start typing its name in the search box.
5. Click on the "Connect" button to connect the integration to the database.


### 4. Get the Database ID
To get the database ID, follow these steps:

1. Open your database in Notion.
2. Click on the three-dot menu icon in the top right corner of the database view.
3. Select "Copy link" from the menu to copy the database URL to your clipboard.
4. The database ID is the long string of alphanumeric characters found in the URL. It typically looks like this: https://www.notion.so/username/8935f9d140a04f95a872520c4f123456?v=.... In this example, the database ID is 8935f9d140a04f95a872520c4f123456.

With the database properly set up and the integration token and database ID in hand, you can now use the NotionDBLoader code to load content and metadata from your Notion database.

## Usage
NotionDBLoader is part of the langchain package's document loaders. You can use it as follows:


```python
from getpass import getpass

NOTION_TOKEN = getpass()
DATABASE_ID = getpass()
```

    ········
    ········
    


```python
from langchain.document_loaders import NotionDBLoader
```


```python
loader = NotionDBLoader(
    integration_token=NOTION_TOKEN,
    database_id=DATABASE_ID,
    request_timeout_sec=30,  # optional, defaults to 10
)
```


```python
docs = loader.load()
```


```python
print(docs)
```

    
    
