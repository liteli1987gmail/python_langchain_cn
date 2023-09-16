# DuckDB
>[DuckDB](https://duckdb.org/)是一个内部SQL OLAP数据库管理系统。
使用每行一个文档的方式加载`DuckDB`查询。

```python
#!pip install duckdb
```

```python
from langchain.document_loaders import DuckDBLoader
```

```python
%%file example.csv
Team,Payroll
Nationals,81.34
Reds,82.20
```

    编写 example.csv
    


```python
loader = DuckDBLoader("SELECT * FROM read_csv_auto('example.csv')")
data = loader.load()
```

```python
print(data)
```

    [Document(page_content='Team: Nationals\nPayroll: 81.34', metadata={}), Document(page_content='Team: Reds\nPayroll: 82.2', metadata={})]
    

## 指定哪些列为内容列，哪些列为元数据列


```python
loader = DuckDBLoader(
    "SELECT * FROM read_csv_auto('example.csv')",
    page_content_columns=["Team"],
    metadata_columns=["Payroll"],
)
data = loader.load()
```

```python
print(data)
```

    [Document(page_content='Team: Nationals', metadata={'Payroll': 81.34}), Document(page_content='Team: Reds', metadata={'Payroll': 82.2})]
    

## 将源添加到元数据


```python
loader = DuckDBLoader(
    "SELECT Team, Payroll, Team As source FROM read_csv_auto('example.csv')",
    metadata_columns=["source"],
)
data = loader.load()
```

```python
print(data)
```

    [Document(page_content='Team: Nationals\nPayroll: 81.34\nsource: Nationals', metadata={'source': 'Nationals'}), Document(page_content='Team: Reds\nPayroll: 82.2\nsource: Reds', metadata={'source': 'Reds'})]








