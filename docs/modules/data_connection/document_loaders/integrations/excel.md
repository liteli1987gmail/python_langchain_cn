# Microsoft Excel
`UnstructuredExcelLoader` 用于加载 `Microsoft Excel` 文件。该加载器适用于 `.xlsx` 和 `.xls` 文件。页面内容将是 Excel 文件的原始文本。如果在“元素”模式下使用加载器，Excel 文件的 HTML 表示将在文档元数据的 `text_as_html` 键下可用。

```python
from langchain.document_loaders import UnstructuredExcelLoader
```

```python
loader = UnstructuredExcelLoader("example_data/stanley-cups.xlsx", mode="elements")
docs = loader.load()
docs[0]
```


    Document(page_content='\n  \n    \n      Team\n      Location\n      Stanley Cups\n    \n    \n      Blues\n      STL\n      1\n    \n    \n      Flyers\n      PHI\n      2\n    \n    \n      Maple Leafs\n      TOR\n      13\n    \n  \n', metadata={'source': 'example_data/stanley-cups.xlsx', 'filename': 'stanley-cups.xlsx', 'file_directory': 'example_data', 'filetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'page_number': 1, 'page_name': 'Stanley Cups', 'text_as_html': '<table border="1" class="dataframe">\n  <tbody>\n    <tr>\n      <td>Team</td>\n      <td>Location</td>\n      <td>Stanley Cups</td>\n    </tr>\n    <tr>\n      <td>Blues</td>\n      <td>STL</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <td>Flyers</td>\n      <td>PHI</td>\n      <td>2</td>\n    </tr>\n    <tr>\n      <td>Maple Leafs</td>\n      <td>TOR</td>\n      <td>13</td>\n    </tr>\n  </tbody>\n</table>', 'category': 'Table'})




```python

```
