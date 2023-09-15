# DuckDB

>[DuckDB](https://duckdb.org/) is an in-process SQL OLAP database management system.

Load a `DuckDB` query with one document per row.


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

    Writing example.csv
    


```python
loader = DuckDBLoader("SELECT * FROM read_csv_auto('example.csv')")

data = loader.load()
```


```python
print(data)
```

    [Document(page_content='Team: Nationals\nPayroll: 81.34', metadata={}), Document(page_content='Team: Reds\nPayroll: 82.2', metadata={})]
    

## Specifying Which Columns are Content vs Metadata


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
    

## Adding Source to Metadata


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
    


```python

```
