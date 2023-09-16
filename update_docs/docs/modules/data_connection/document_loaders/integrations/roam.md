# Roam

[ROAM](https://roamresearch.com/) 是一个用于网络思维的笔记工具，旨在创建个人知识库。

本笔记本介绍了如何从 Roam 数据库加载文档。这主要受到了[这里](https://github.com/JimmyLv/roam-qa)的示例仓库的启发。

## 🟡 指南：如何导入您自己的数据集

从 Roam Research 导出您的数据集。您可以通过点击右上角的三个点，然后点击“导出”来完成此操作。

在导出时，请确保选择“Markdown 和 CSV”格式选项。

这将在您的下载文件夹中生成一个 `.zip` 文件。将 `.zip` 文件移动到此存储库中。

运行以下命令解压缩 zip 文件（根据需要替换“Export...”为您自己的文件名）：

```shell
unzip Roam-Export-1675782732639.zip -d Roam_DB
```

```python
from langchain.document_loaders import RoamLoader
```

```python
loader = RoamLoader("Roam_DB")
```

```python
docs = loader.load()
```