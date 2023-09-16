# Microsoft OneDrive
>[Microsoft OneDrive](https://en.wikipedia.org/wiki/OneDrive)（以前是`SkyDrive`）是由Microsoft运营的文件托管服务。

本笔记本介绍了如何从`OneDrive`加载文档。目前，仅支持docx、doc和pdf文件。

## 先决条件
1. 根据[Microsoft身份平台](https://learn.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app)的说明，注册一个应用程序。
2. 注册完成后，Azure门户显示应用程序注册的概述窗格。您将看到应用程序（客户端）ID。也称为`客户端ID`，此值唯一地标识Microsoft身份平台中的应用程序。
3. 在您遵循**项目1**的步骤时，您可以将重定向URI设置为`http://localhost:8000/callback`
4. 在您遵循**项目1**的步骤时，在Application Secrets部分生成一个新密码（`client_secret`）。
5. 按照此[文档](https://learn.microsoft.com/en-us/azure/active-directory/develop/quickstart-configure-app-expose-web-apis#add-a-scope)的说明，将以下`SCOPES`（`offline_access`和`Files.Read.All`）添加到您的应用程序中。
6. 访问[Graph Explorer Playground](https://developer.microsoft.com/en-us/graph/graph-explorer)以获取您的`OneDrive ID`。第一步是确保您已登录与您的OneDrive帐户关联的帐户。然后，您需要向`https://graph.microsoft.com/v1.0/me/drive`发出请求，响应将返回一个包含一个字段`id`的有效负载，该字段保存了您的OneDrive帐户的ID。
7. 您需要使用命令`pip install o365`安装o365包。
8. 在步骤结束时，您必须拥有以下值：
- `CLIENT_ID`
- `CLIENT_SECRET`
- `DRIVE_ID`

## 🟡 从OneDrive摄取您的文档的说明

### 🍑 身份验证

默认情况下，`OneDriveLoader`希望将`CLIENT_ID`和`CLIENT_SECRET`的值存储为名为`O365_CLIENT_ID`和`O365_CLIENT_SECRET`的环境变量。您可以通过在应用程序的根目录下使用`.env`文件或使用以下命令在脚本中传递这些环境变量。

```python
os.environ['O365_CLIENT_ID'] = "YOUR CLIENT ID"
os.environ['O365_CLIENT_SECRET'] = "YOUR CLIENT SECRET"
```

此加载程序使用称为[*代表用户*](https://learn.microsoft.com/en-us/graph/auth-v2-user?context=graph%2Fapi%2F1.0&view=graph-rest-1.0)的身份验证。这是一个需要用户同意的2步骤身份验证。当您实例化加载器时，它将调用一个URL，用户必须访问该URL以在所需权限上为应用程序授予同意。然后，用户必须访问此URL并为应用程序授予同意。然后，用户必须复制生成的页面URL并将其粘贴回控制台。然后，如果登录尝试成功，该方法将返回True。

```python
from langchain.document_loaders.onedrive import OneDriveLoader

loader = OneDriveLoader(drive_id="YOUR DRIVE ID")
```

身份验证完成后，加载器将在`~/.credentials/`文件夹中存储一个令牌（`o365_token.txt`）。稍后可以使用此令牌进行身份验证，而无需再次执行复制/粘贴步骤。要使用此令牌进行身份验证，请在加载器实例化时将`auth_with_token`参数更改为True。

```python
from langchain.document_loaders.onedrive import OneDriveLoader

loader = OneDriveLoader(drive_id="YOUR DRIVE ID", auth_with_token=True)
```

### 🗂 文档加载器

#### 📑 从OneDrive目录加载文档

`OneDriveLoader`可以从OneDrive的特定文件夹加载文档。例如，您要加载存储在`Documents/clients`文件夹中的所有文档。

```python
from langchain.document_loaders.onedrive import OneDriveLoader

loader = OneDriveLoader(drive_id="YOUR DRIVE ID", folder_path="Documents/clients", auth_with_token=True)
documents = loader.load()
```

#### 📑 从文档ID列表加载文档

另一种可能性是为您想要加载的每个文档提供一个`object_id`列表。为此，您需要查询[Microsoft Graph API](https://developer.microsoft.com/en-us/graph/graph-explorer)以查找您感兴趣的所有文档ID。此[链接](https://learn.microsoft.com/en-us/graph/api/resources/onedrive?view=graph-rest-1.0#commonly-accessed-resources)提供了一些有助于检索文档ID的端点列表。

例如，要检索存储在Documents文件夹根目录中的所有对象的信息，您需要向以下位置发出请求：`https://graph.microsoft.com/v1.0/drives/{YOUR DRIVE ID}/root/children`。一旦您获得了您感兴趣的ID列表，然后您可以使用以下参数实例化加载器。

```python
from langchain.document_loaders.onedrive import OneDriveLoader

loader = OneDriveLoader(drive_id="YOUR DRIVE ID", object_ids=["ID_1", "ID_2"], auth_with_token=True)
documents = loader.load()
```