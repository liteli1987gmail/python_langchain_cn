# Notion DB 2/2

[Notion](https://www.notion.so/)是一个协作平台，支持修改过的Markdown，集成看板，任务，维基和数据库。它是一个集成了笔记、知识和数据管理以及项目和任务管理的全能工作空间。

`NotionDBLoader`是一个用于从`Notion`数据库加载内容的Python类。它从数据库中检索页面，读取其内容，并返回文档对象的列表。

## 要求

- 一个`Notion`数据库
- Notion集成令牌

## 设置

### 1. 创建Notion表数据库

在Notion中创建一个新的表数据库。您可以向数据库添加任何列，并将其视为元数据。例如，您可以添加以下列：

- Title：将Title设置为默认属性。
- Categories：一个多选属性，用于存储与页面关联的类别。
- Keywords：一个多选属性，用于存储与页面关联的关键字。

将内容添加到数据库中每个页面的正文中。NotionDBLoader将从这些页面提取内容和元数据。

## 2. 创建Notion集成

要创建Notion集成，按照以下步骤操作：

1. 访问[Notion Developers](https://www.notion.com/my-integrations)页面，并使用您的Notion账户登录。
2. 点击"+ New integration"按钮。
3. 为集成命名，并选择数据库所在的工作区。
4. 选择所需的功能，此扩展仅需要读取内容的功能。
5. 单击"Submit"按钮以创建集成。

创建集成后，将提供一个`集成令牌（API密钥）`。请复制此令牌并将其保存在安全的地方，因为您需要使用NotionDBLoader时会用到它。

### 3. 将集成连接到数据库

要将集成连接到数据库，请按照以下步骤操作：

1. 在Notion中打开数据库。
2. 点击数据库视图右上角的三点菜单图标。
3. 点击"+ New integration"按钮。
4. 找到您的集成，您可能需要在搜索框中开始输入其名称。
5. 点击"Connect"按钮以将集成连接到数据库。

### 4. 获取数据库ID

要获取数据库ID，请按照以下步骤操作：

1. 在Notion中打开数据库。
2. 点击数据库视图右上角的三点菜单图标。
3. 在菜单中选择"Copy link"以将数据库URL复制到剪贴板。
4. 数据库ID是在URL中找到的一长串字母数字字符。通常它看起来像这样：https://www.notion.so/username/8935f9d140a04f95a872520c4f123456?v=.... 在此示例中，数据库ID是8935f9d140a04f95a872520c4f123456。

设置数据库并获取整合令牌和数据库ID后，现在可以使用NotionDBLoader代码从Notion数据库中加载内容和元数据。

## 用法

NotionDBLoader是langchain包的文档加载程序的一部分。您可以按照以下方式使用它：

```python
from getpass import getpass

NOTION_TOKEN = getpass()
DATABASE_ID = getpass()
```



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



