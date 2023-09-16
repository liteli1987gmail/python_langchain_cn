# GitBook
[GitBook](https://docs.gitbook.com/)是一个现代化的文档平台，团队可以在其中记录从产品到内部知识库和API的所有内容。
```python
from langchain.document_loaders import GitbookLoader
```
### 从单个GitBook页面加载
```python
loader = GitbookLoader("https://docs.gitbook.com")
```
```python
page_data = loader.load()
```
```python
page_data
```

[Document(page_content='Introduction to GitBook
GitBook是一个现代化的文档平台，团队可以在其中记录从产品到内部知识库和API的所有内容。
我们希望通过创建一个简单而强大的平台来帮助团队更高效地工作，以便他们分享自己的知识。
我们的使命是为每个人创建一个用户友好和协作的产品，通过文档共享知识。
通常5个简单的步骤发布您的文档
导入

轻松将现有内容移动到GitBook。
Git同步

享受与GitHub和GitLab的双向同步。
组织您的内容

创建页面和空间，并将它们组织到集合中
协作

邀请其他用户，并轻松进行异步协作。
发布您的文档

与选定的用户或所有人共享您的文档。
下一步
 - 入门

概述
上一次修改 
3个月前', lookup_str='', metadata={'source': 'https://docs.gitbook.com', 'title': 'Introduction to GitBook'}, lookup_index=0)]
### 从给定GitBook的所有路径加载
为了使用其工作，GitbookLoader需要用根路径（在此示例中为`https://docs.gitbook.com`）进行初始化，并将`load_all_paths`设置为`True`。
```python
loader = GitbookLoader("https://docs.gitbook.com", load_all_paths=True)
all_pages_data = loader.load()
```

从https://docs.gitbook.com获取文本
从https://docs.gitbook.com/getting-started/overview获取文本
从https://docs.gitbook.com/getting-started/import获取文本
从https://docs.gitbook.com/getting-started/git-sync获取文本
从https://docs.gitbook.com/getting-started/content-structure获取文本
从https://docs.gitbook.com/getting-started/collaboration获取文本
从https://docs.gitbook.com/getting-started/publishing获取文本
从https://docs.gitbook.com/tour/quick-find获取文本
从https://docs.gitbook.com/tour/editor获取文本
从https://docs.gitbook.com/tour/customization获取文本
从https://docs.gitbook.com/tour/member-management获取文本
从https://docs.gitbook.com/tour/pdf-export获取文本
从https://docs.gitbook.com/tour/activity-history获取文本
从https://docs.gitbook.com/tour/insights获取文本
从https://docs.gitbook.com/tour/notifications获取文本
从https://docs.gitbook.com/tour/internationalization获取文本
从https://docs.gitbook.com/tour/keyboard-shortcuts获取文本
从https://docs.gitbook.com/tour/seo获取文本
从https://docs.gitbook.com/advanced-guides/custom-domain获取文本
从https://docs.gitbook.com/advanced-guides/advanced-sharing-and-security获取文本
从https://docs.gitbook.com/advanced-guides/integrations获取文本
从https://docs.gitbook.com/billing-and-admin/account-settings获取文本
从https://docs.gitbook.com/billing-and-admin/plans获取文本
从https://docs.gitbook.com/troubleshooting/faqs获取文本
从https://docs.gitbook.com/troubleshooting/hard-refresh获取文本
从https://docs.gitbook.com/troubleshooting/report-bugs获取文本
从https://docs.gitbook.com/troubleshooting/connectivity-issues获取文本
从https://docs.gitbook.com/troubleshooting/support获取文本

```python
print(f"fetched {len(all_pages_data)} documents.")
# show second document
all_pages_data[2]
```


fetched 28 documents.


