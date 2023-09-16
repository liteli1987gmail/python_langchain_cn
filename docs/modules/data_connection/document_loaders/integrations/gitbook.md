# GitBook
>[GitBook](https://docs.gitbook.com/)是一个现代化的文档平台，团队可以在其中记录从产品到内部知识库和API的所有内容。

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


    [Document(page_content='Introduction to GitBook\nGitBook是一个现代化的文档平台，团队可以在其中记录从产品到内部知识库和API的所有内容。\n我们希望通过创建一个简单而强大的平台来帮助团队更高效地工作，以便他们分享自己的知识。\n我们的使命是为每个人创建一个用户友好和协作的产品，通过文档共享知识。\n通过5个简单的步骤发布您的文档\n导入\n\n轻松将现有内容移至GitBook。\nGit同步\n\n享受与GitHub和GitLab的双向同步。\n组织您的内容\n\n创建页面和空间，并将它们组织到集合中\n协作\n\n邀请其他用户，并轻松进行异步协作。\n发布您的文档\n\n与选定的用户或所有人共享您的文档。\n下一步\n - 入门\n概述\n上次修改 \n3个月前', lookup_str='', metadata={'source': 'https://docs.gitbook.com', 'title': 'Introduction to GitBook'}, lookup_index=0)]

### 从给定GitBook的所有路径加载
为了使其工作，GitbookLoader需要用根路径（在此示例中为`https://docs.gitbook.com`）进行初始化，并将`load_all_paths`设置为`True`。

```python
loader = GitbookLoader("https://docs.gitbook.com", load_all_paths=True)
all_pages_data = loader.load()
```

    从https://docs.gitbook.com/获取文本
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
    




    Document(page_content="导入\n找出如何轻松迁移现有文档以及支持的格式。\n导入功能允许您在GitBook中迁移和统一现有文档。您可以选择导入单个或多个页面，尽管有限制。\n权限\n具有编辑权限或更高权限的所有成员都可以使用导入功能。\n支持的格式\nGitBook支持从网站或文件导入:\nMarkdown（.md或.markdown）\nHTML（.html）\nMicrosoft Word（.docx）。\n我们还支持从:\nConfluence\nNotion\nGitHub Wiki\nQuip\nDropbox Paper\nGoogle Docs\n在导入多个页面时，您还可以上传包含HTML或Markdown文件的ZIP\n \n文件夹。\n注意：此功能处于测试版。\n请随时建议我们尚不支持的导入源，并告诉我们\n如果您遇到任何问题。\n导入面板\n创建新空间时，您将有选项立即导入内容:\n新页面菜单\n通过选择\n导入页面\n菜单中的\n导入子页面\n，或在目录中找到的页面操作菜单中的\n导入子页面\n导入页面或子页面\n当您选择输入源时，说明将解释如何进行。\n尽管GitBook支持从不同类型的来源导入内容，但由于产品功能和文档格式的差异，最终结果可能与您的源不同。\n限制\nGitBook当前对导入内容有以下限制:\n单次导入的最大页面数为\n20。\n单次导入的最大文件数（图像等）为\n20。\n入门 - \n上一步\n概述\n下一步 - 入门\nGit同步\n上次修改 \n4个月前", lookup_str='', metadata={'source': 'https://docs.gitbook.com/getting-started/import', 'title': 'Import'}, lookup_index=0)



```python

```