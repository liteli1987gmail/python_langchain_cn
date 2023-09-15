# Git

>[Git](https://en.wikipedia.org/wiki/Git) is a distributed version control system that tracks changes in any set of computer files, usually used for coordinating work among programmers collaboratively developing source code during software development.

This notebook shows how to load text files from `Git` repository.

## Load existing repository from disk


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
data = loader.load()
```


```python
len(data)
```


```python
print(data[0])
```

    page_content='.venv\n.github\n.git\n.mypy_cache\n.pytest_cache\nDockerfile' metadata={'file_path': '.dockerignore', 'file_name': '.dockerignore', 'file_type': ''}
    

## Clone repository from url


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
data = loader.load()
```


```python
len(data)
```




    1074



## Filtering files to load


```python
from langchain.document_loaders import GitLoader

# eg. loading only python files
loader = GitLoader(
    repo_path="./example_data/test_repo1/",
    file_filter=lambda file_path: file_path.endswith(".py"),
)
```


```python

```
