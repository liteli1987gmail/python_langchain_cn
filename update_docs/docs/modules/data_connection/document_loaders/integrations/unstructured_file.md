# 非结构化文件

这个笔记本介绍了如何使用`Unstructured`包加载多种类型的文件。 `Unstructured`目前支持加载文本文件，幻灯片，html，pdf，图像等。

```python
# # 安装包
!pip install "unstructured[local-inference]"
!pip install layoutparser[layoutmodels,tesseract]
```

```python
# # 安装其他依赖
# # https://github.com/Unstructured-IO/unstructured/blob/main/docs/source/installing.rst
# !brew install libmagic
# !brew install poppler
# !brew install tesseract
# # 如果解析xml / html文档:
# !brew install libxml2
# !brew install libxslt
```

```python
# 导入nltk
# nltk.download('punkt')
```

```python
from langchain.document_loaders import UnstructuredFileLoader
```

```python
loader = UnstructuredFileLoader("./example_data/state_of_the_union.txt")
```

```python
# 加载文档

# 
# 


docs = loader.load()
```

```python
docs[0].page_content[:400]
```



    '女士们，先生们，美国副总统，我们的第一夫人和第二绅士。国会和内阁成员。最高法院法官。我的美国同胞们。\n\n去年COVID-19使我们分开。今年我们终于再次在一起。\n\n今晚，我们作为民主党人，共和党人和独立的人见面。但最重要的是作为美国人。\n\n对美国人民，对宪法，我们彼此都有责任。'





## 保留元素

在底层，Unstructured为不同的文本块创建不同的"元素"。默认情况下，我们将它们合并在一起，但是您可以通过指定`mode="elements"`轻松保留该分隔。



```python
loader = UnstructuredFileLoader(
    "./example_data/state_of_the_union.txt", mode="elements"
)
```

```python


docs = loader.load()
```

```python

docs[:5]
```




    [Document(page_content='女士们，先生们，美国副总统，我们的第一夫人和第二绅士。国会和内阁成员。最高法院法官。我的美国同胞。', lookup_str='', metadata={'source': '../../state_of_the_union.txt'}, lookup_index=0),
     Document(page_content='去年COVID-19使我们分开。今年我们终于再次在一起。', lookup_str='', metadata={'source': '../../state_of_the_union.txt'}, lookup_index=0),
     Document(page_content='今晚，我们作为民主党人，共和党人和独立的人见面。但最重要的是作为美国人。', lookup_str='', metadata={'source': '../../state_of_the_union.txt'}, lookup_index=0),
     Document(page_content='对美国人民，对宪法，我们彼此都有责任。', lookup_str='', metadata={'source': '../../state_of_the_union.txt'}, lookup_index=0),
     Document(page_content='并且坚定决心自由将永远战胜暴政。', lookup_str='', metadata={'source': '../../state_of_the_union.txt'}, lookup_index=0)]




## 定义分区策略

Unstructured文档加载器允许用户传入一个`strategy`参数，让`unstructured`知道如何分割文档。目前支持的策略有`"hi_res"`（默认值）和`"fast"`。高分辨率分区策略更准确，但处理时间较长。快速策略更快地分割文档，但会降低准确性。并非所有文档类型都有单独的高分辨率和快速分区策略。对于这些文档类型，`strategy`关键字参数将被忽略。在某些情况下，如果缺少依赖项（即文档分区的模型），高分辨率策略将回退到快速策略。您可以在下面看到如何将策略应用于`UnstructuredFileLoader`。



```python
from langchain.document_loaders import UnstructuredFileLoader
```

```python
loader = UnstructuredFileLoader(
    "layout-parser-paper-fast.pdf", strategy="fast", mode="elements"
)
```

```python

docs = loader.load()
```

```python

docs[:5]
```




    [Document(page_content='1', lookup_str='', metadata={'source': 'layout-parser-paper-fast.pdf', 'filename': 'layout-parser-paper-fast.pdf', 'page_number': 1, 'category': 'UncategorizedText'}, lookup_index=0),
     Document(page_content='2', lookup_str='', metadata={'source': 'layout-parser-paper-fast.pdf', 'filename': 'layout-parser-paper-fast.pdf', 'page_number': 1, 'category': 'UncategorizedText'}, lookup_index=0),
     Document(page_content='0', lookup_str='', metadata={'source': 'layout-parser-paper-fast.pdf', 'filename': 'layout-parser-paper-fast.pdf', 'page_number': 1, 'category': 'UncategorizedText'}, lookup_index=0),
     Document(page_content='2', lookup_str='', metadata={'source': 'layout-parser-paper-fast.pdf', 'filename': 'layout-parser-paper-fast.pdf', 'page_number': 1, 'category': 'UncategorizedText'}, lookup_index=0),
     Document(page_content='n', lookup_str='', metadata={'source': 'layout-parser-paper-fast.pdf', 'filename': 'layout-parser-paper-fast.pdf', 'page_number': 1, 'category': 'Title'}, lookup_index=0)]




## PDF示例

处理PDF文档的方式完全相同。Unstructured会检测文件类型并提取相同类型的元素。操作模式为
- `single` 将所有元素的文本合并为一个（默认）
- `elements` 保留单独的元素
- `paged` 每个页面的文本仅合并


```python
!wget  https://raw.githubusercontent.com/Unstructured-IO/unstructured/main/example-docs/layout-parser-paper.pdf -P "../../"
```

```python
loader = UnstructuredFileLoader(
    "./example_data/layout-parser-paper.pdf", mode="elements"
)
```

```python

docs = loader.load()
```

```python

docs[:5]
```




    [Document(page_content='LayoutParser : A Uni\ufb01ed Toolkit for Deep Learning Based Document Image Analysis', lookup_str='', metadata={'source': '../../layout-parser-paper.pdf'}, lookup_index=0),
     Document(page_content='Zejiang Shen 1 ( (ea)\n ), Ruochen Zhang 2 , Melissa Dell 3 , Benjamin Charles Germain Lee 4 , Jacob Carlson 3 , and Weining Li 5', lookup_str='', metadata={'source': '../../layout-parser-paper.pdf'}, lookup_index=0),
     Document(page_content='Allen Institute for AI shannons@allenai.org', lookup_str='', metadata={'source': '../../layout-parser-paper.pdf'}, lookup_index=0),
     Document(page_content='Brown University ruochen zhang@brown.edu', lookup_str='', metadata={'source': '../../layout-parser-paper.pdf'}, lookup_index=0),
     Document(page_content='Harvard University { melissadell,jacob carlson } @fas.harvard.edu', lookup_str='', metadata={'source': '../../layout-parser-paper.pdf'}, lookup_index=0)]




## Unstructured API

如果您想通过更少的设置立即开始运行，只需运行`pip install unstructured`并使用`UnstructuredAPIFileLoader`或`UnstructuredAPIFileIOLoader`即可。这将使用托管的Unstructured API处理您的文档。请注意，当前（截至2023年5月11日）Unstructured API是开放的，但很快将需要API密钥。一旦可用，[Unstructured文档](https://unstructured-io.github.io/)页面将提供有关如何生成API密钥的说明。如果您希望自己托管Unstructured API或在本地运行它，请查看[此处的说明](https://github.com/Unstructured-IO/unstructured-api#dizzy-instructions-for-using-the-docker-image)。



```python
from langchain.document_loaders import UnstructuredAPIFileLoader
```

```python
filenames = ["example_data/fake.docx", "example_data/fake-email.eml"]
```

```python
loader = UnstructuredAPIFileLoader(
    file_path=filenames[0],
    api_key="FAKE_API_KEY",
)
```

```python

docs = loader.load()
docs[0]
```




    Document(page_content='Lorem ipsum dolor sit amet.', metadata={'source': 'example_data/fake.docx'})




您还可以使用`UnstructuredAPIFileLoader`在单个API中批处理多个文件。



```python
loader = UnstructuredAPIFileLoader(
    file_path=filenames,
    api_key="FAKE_API_KEY",
)
```

```python

docs = loader.load()
docs[0]
```




    Document(page_content='Lorem ipsum dolor sit amet.\n\nThis is a test email to use for unit tests.\n\nImportant points:\n\nRoses are red\n\nViolets are blue', metadata={'source': ['example_data/fake.docx', 'example_data/fake-email.eml']})




```python

```