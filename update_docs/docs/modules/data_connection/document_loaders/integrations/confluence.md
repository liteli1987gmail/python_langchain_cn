# Confluence

>[Confluence](https://www.atlassian.com/software/confluence) is a wiki collaboration platform that saves and organizes all of the project-related material. `Confluence` is a knowledge base that primarily handles content management activities. 

A loader for `Confluence` pages.


This currently supports `username/api_key`, `Oauth2 login`. Additionally, on-prem installations also support `token` authentication. 


Specify a list `page_id`-s and/or `space_key` to load in the corresponding pages into Document objects, if both are specified the union of both sets will be returned.


You can also specify a boolean `include_attachments` to include attachments, this is set to False by default, if set to True all attachments will be downloaded and ConfluenceReader will extract the text from the attachments and add it to the Document object. Currently supported attachment types are: `PDF`, `PNG`, `JPEG/JPG`, `SVG`, `Word` and `Excel`.

Hint: `space_key` and `page_id` can both be found in the URL of a page in Confluence - https://yoursite.atlassian.com/wiki/spaces/<space_key>/pages/<page_id>


Before using ConfluenceLoader make sure you have the latest version of the atlassian-python-api package installed:


```python
#!pip install atlassian-python-api
```

## Examples

### Username and Password or Username and API Token (Atlassian Cloud only)

This example authenticates using either a username and password or, if you're connecting to an Atlassian Cloud hosted version of Confluence, a username and an API Token.
You can generate an API token at: https://id.atlassian.com/manage-profile/security/api-tokens.

The `limit` parameter specifies how many documents will be retrieved in a single call, not how many documents will be retrieved in total.
By default the code will return up to 1000 documents in 50 documents batches. To control the total number of documents use the `max_pages` parameter. 
Plese note the maximum value for the `limit` parameter in the atlassian-python-api package is currently 100.  


```python
from langchain.document_loaders import ConfluenceLoader

loader = ConfluenceLoader(
    url="https://yoursite.atlassian.com/wiki", username="me", api_key="12345"
)
documents = loader.load(space_key="SPACE", include_attachments=True, limit=50)
```

### Personal Access Token (Server/On-Prem only)

This method is valid for the Data Center/Server on-prem edition only.
For more information on how to generate a Personal Access Token (PAT) check the official Confluence documentation at: https://confluence.atlassian.com/enterprise/using-personal-access-tokens-1026032365.html.
When using a PAT you provide only the token value, you cannot provide a username. 
Please note that ConfluenceLoader will run under the permissions of the user that generated the PAT and will only be able to load documents for which said user has access to.  


```python
from langchain.document_loaders import ConfluenceLoader

loader = ConfluenceLoader(url="https://yoursite.atlassian.com/wiki", token="12345")
documents = loader.load(
    space_key="SPACE", include_attachments=True, limit=50, max_pages=50
)
```
