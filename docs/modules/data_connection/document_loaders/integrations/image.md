# 图片

本文介绍了如何将`JPG`或`PNG`等图片加载到我们可以在下游使用的文档格式中。

## 使用非结构化图片


```python
#!pip install pdfminer
```


```python
from langchain.document_loaders.image import UnstructuredImageLoader
```


```python
loader = UnstructuredImageLoader("layout-parser-paper-fast.jpg")
```


```python
data = loader.load()
```


```python
data[0]
```




    Document(page_content="LayoutParser: A Unified Toolkit for Deep\nLearning Based Document Image Analysis\n\n\n‘Zxjiang Shen' (F3}, Ruochen Zhang”, Melissa Dell*, Benjamin Charles Germain\nLeet, Jacob Carlson, and Weining LiF\n\n\nsugehen\n\nshangthrows, et\n\n“Abstract. Recent advanocs in document image analysis (DIA) have been\n‘pimarliy driven bythe application of neural networks dell roar\n{uteomer could be aly deployed in production and extended fo farther\n[nvetigtion. However, various factory ke lcely organize codebanee\nsnd sophisticated modal cnigurations compat the ey ree of\n‘erin! innovation by wide sence, Though there have been sng\n‘Hors to improve reuablty and simplify deep lees (DL) mode\n‘aon, sone of them ae optimized for challenge inthe demain of DIA,\nThis roprscte a major gap in the extng fol, sw DIA i eal to\nscademic research acon wie range of dpi in the social ssencee\n[rary for streamlining the sage of DL in DIA research and appicn\n‘tons The core LayoutFaraer brary comes with a sch of simple and\nIntative interfaee or applying and eutomiing DI. odel fr Inyo de\npltfom for sharing both protrined modes an fal document dist\n{ation pipeline We demonutate that LayootPareer shea fr both\nlightweight and lrgeseledgtieation pipelines in eal-word uae ces\nThe leary pblely smal at Btspe://layost-pareergsthab So\n\n\n\n‘Keywords: Document Image Analysis» Deep Learning Layout Analysis\n‘Character Renguition - Open Serres dary « Tol\n\n\nIntroduction\n\n\n‘Deep Learning(DL)-based approaches are the state-of-the-art for a wide range of\ndoctiment image analysis (DIA) tea including document image clasiffeation [I]\n", lookup_str='', metadata={'source': 'layout-parser-paper-fast.jpg'}, lookup_index=0)



### 保留元素

在幕后，Unstructured为不同的文本块创建不同的"元素"。默认情况下，我们将它们组合在一起，但您可以通过指定`mode="elements"`来保留该分隔。


```python
loader = UnstructuredImageLoader("layout-parser-paper-fast.jpg", mode="elements")
```


```python
data = loader.load()
```


```python
data[0]
```




    Document(page_content='LayoutParser: A Unified Toolkit for Deep\nLearning Based Document Image Analysis\n', lookup_str='', metadata={'source': 'layout-parser-paper-fast.jpg', 'filename': 'layout-parser-paper-fast.jpg', 'page_number': 1, 'category': 'Title'}, lookup_index=0)


