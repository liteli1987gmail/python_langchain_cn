# Git

[Git](https://en.wikipedia.org/wiki/Git) 是一种分布式版本控制系统，用于跟踪计算机文件集的更改，通常用于协调开发人员在软件开发过程中共同开发源代码。

这个笔记本演示了如何从 `Git` 仓库加载文本文件。

## 从础盘加载现有仓库

```python
!pip install GitPython
```

```python
from git import Repo

repo = Repo.clone_from(
    "https://github.com/hwchase17/langchain", to_path="./example_data/test_repo1"
)
branch = repo.head.reference
```

```python
from langchain.document_loaders import GitLoader
```

```python
loader = GitLoader(repo_path="./example_data/test_repo1/", branch=branch)
```

```python
ndata = loader.load()
```

```python
len(data)
```

```python
print(data[0])
```

    page_content='.venv\n.github\n.git\n.mypy_cache\n.pytest_cache\nDockerfile' metadata={'file_path': '.dockerignore', 'file_name': '.dockerignore', 'file_type': ''}

## 从 URL 克隆仓库

```python
from langchain.document_loaders import GitLoader
```

```python
loader = GitLoader(
    clone_url="https://github.com/hwchase17/langchain",
    repo_path="./example_data/test_repo2/",
    branch="master",
)
```

```python
ndata = loader.load()
```

```python
len(data)
```


    1074


## 过滤要加载的文件

```python
from langchain.document_loaders import GitLoader

# 例如，仅加载 Python 文件
loader = GitLoader(
    repo_path="./example_data/test_repo1/",
    file_filter=lambda file_path: file_path.endswith(".py"),
)
```



