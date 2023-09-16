# Confluence

>[Confluence](https://www.atlassian.com/software/confluence)是一个维基协作作平台，用于保存和组织所有与项目相关的材料。`Confluence`是一个主要处理内容管理活动的知识库。

一个用于`Confluence`页面的加载器。

当前支持`username/api_key`、`Oauth2登录`。此外，本地安装还支持`token`身份验证。

指定一个列表`page_id`和/或`space_key`，将对应的页面加载到文档对象中，如果两者都指定，则返回两者的并集。

您还可以指定一个布尔值`include_attachments`来包含附件，默认情况下设置为False，如果设置为True，则下载所有附件，并且ConfluenceReader将从附件中提取文本并将其添加到文档对象中。当前支持的附件类型有：`PDF`、`PNG`、`JPEG/JPG`、`SVG`、`Word`和`Excel`。

提示：`space_key`和`page_id`都可以在Confluence页面的URL中找到- https://yoursite.atlassian.com/wiki/spaces/<space_key>/pages/<page_id>

在使用ConfluenceLoader之前，请确保已安装了最新版本的atlassian-python-api包。

```python
#!pip install atlassian-python-api
```

## Examples

### 用户名和密码或用户名和API令牌（仅适用于Atlassian Cloud）

此示例使用用户名和密码或如果您连接到的Confluence是Atlassian Cloud托管版本，则使用用户名和API令牌进行身份验证。

您可以在以下位置生成API令牌：https://id.atlassian.com/manage-profile/security/api-tokens

`limit`参数指定每次调用中将检索多少个文档，而不是总共检索多少个文档。默认情况下，代码将批次返回1000个文档。要控制文档的总数，请使用`max_pages`参数。

请注意，atlassian-python-api包中`limit`参数的最大值目前为100。

```python
from langchain.document_loaders import ConfluenceLoader

loader = ConfluenceLoader(
    url="https://yoursite.atlassian.com/wiki",
    username="me",
    api_key="12345"
)
documents = loader.load(space_key="SPACE", include_attachments=True, limit=50)
```

### 个人访问令牌（仅适用于Server/On-Prem）

此方法仅适用于Data Center/Server本地版本。

有关如何生成个人访问令牌（PAT）的详细信息，请参阅官方Confluence文档：https://confluence.atlassian.com/enterprise/using-personal-access-tokens-1026032365.html

在使用PAT时，只需提供令牌值，无需提供用户名。请注意，ConfluenceLoader将在具有访问权限的文档中生成PAT的用户运行，并且只能加载该用户具有访问权限的文档。

```python
from langchain.document_loaders import ConfluenceLoader

loader = ConfluenceLoader(
    url="https://yoursite.atlassian.com/wiki",
    token="12345"
)
documents = loader.load(
    space_key="SPACE",
    include_attachments=True,
    limit=50,
    max_pages=50
)
```