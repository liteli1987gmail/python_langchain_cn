# MarkdownHeaderTextSplitter

### 动机

许多聊天或问答应用程序在嵌入和向量存储之前，会先对输入文档进行分割成块。

[Pinecone 的这些笔记](https://www.pinecone.io/learn/chunking-strategies/)提供了一些有用的提示：

```
当嵌入整个段落或文档时，嵌入过程会同时考虑整体上下文和文本中句子和短语之间的关系。这可能会得到更全面的向量表示，捕捉文本的更广泛的含义和主题。
```

正如上面所述，分块通常旨在将具有共同上下文的文本保持在一起。

在这种情况下，我们可能想要特别尊重文档本身的结构。

例如，一个 Markdown 文件的组织方式是通过标题。

在特定的标题组内创建分块是一个直观的想法。

为了解决这个挑战，我们可以使用 `MarkdownHeaderTextSplitter`。

它将按照指定的一组标题来分割一个 Markdown 文件。

例如，如果我们想要分割这个 Markdown：
```
md = '# Foo\n\n ## Bar\n\nHi this is Jim  \nHi this is Joe\n\n ## Baz\n\n Hi this is Molly' 
```

我们可以指定要分割的标题：
```
[("#", "Header 1"),("##", "Header 2")]
```

然后根据公共标题进行内容的分组或分割：
```
{'content': 'Hi this is Jim  \nHi this is Joe', 'metadata': {'Header 1': 'Foo', 'Header 2': 'Bar'}}
{'content': 'Hi this is Molly', 'metadata': {'Header 1': 'Foo', 'Header 2': 'Baz'}}
```

让我们来看一些下面的示例。


```python
from langchain.text_splitter import MarkdownHeaderTextSplitter
```


```python
markdown_document = "# Foo\n\n    ## Bar\n\nHi this is Jim\n\nHi this is Joe\n\n ### Boo \n\n Hi this is Lance \n\n ## Baz\n\n Hi this is Molly"

headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]

markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
md_header_splits = markdown_splitter.split_text(markdown_document)
for split in md_header_splits:
    print(split)
```

    {'content': 'Hi this is Jim  \nHi this is Joe', 'metadata': {'Header 1': 'Foo', 'Header 2': 'Bar'}}
    {'content': 'Hi this is Lance', 'metadata': {'Header 1': 'Foo', 'Header 2': 'Bar', 'Header 3': 'Boo'}}
    {'content': 'Hi this is Molly', 'metadata': {'Header 1': 'Foo', 'Header 2': 'Baz'}}
    

Within each markdown group we can then apply any text splitter we want. 


```python
markdown_document = "# Intro \n\n    ## History \n\n Markdown[9] is a lightweight markup language for creating formatted text using a plain-text editor. John Gruber created Markdown in 2004 as a markup language that is appealing to human readers in its source code form.[9] \n\n Markdown is widely used in blogging, instant messaging, online forums, collaborative software, documentation pages, and readme files. \n\n ## Rise and divergence \n\n As Markdown popularity grew rapidly, many Markdown implementations appeared, driven mostly by the need for \n\n additional features such as tables, footnotes, definition lists,[note 1] and Markdown inside HTML blocks. \n\n #### Standardization \n\n From 2012, a group of people, including Jeff Atwood and John MacFarlane, launched what Atwood characterised as a standardisation effort. \n\n ## Implementations \n\n Implementations of Markdown are available for over a dozen programming languages."

headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
]

# MD splits
markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
md_header_splits = markdown_splitter.split_text(markdown_document)

# Char-level splits
from langchain.text_splitter import RecursiveCharacterTextSplitter
chunk_size = 10
chunk_overlap = 0
text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

# Split within each header group
all_splits=[]
all_metadatas=[]    
for header_group in md_header_splits:
    _splits = text_splitter.split_text(header_group['content'])
    _metadatas = [header_group['metadata'] for _ in _splits]
    all_splits += _splits
    all_metadatas += _metadatas
```


```python
all_splits[0]
```




    'Markdown[9'




```python
all_metadatas[0]
```




    {'Header 1': 'Intro', 'Header 2': 'History'}



### Use case

Let's appy `MarkdownHeaderTextSplitter` to a Notion page [here](https://rlancemartin.notion.site/Auto-Evaluation-of-Metadata-Filtering-18502448c85240828f33716740f9574b?pvs=4) as a test.

The page is downloaded as markdown and stored locally as shown [here](https://python.langchain.com/docs/modules/data_connection/document_loaders/integrations/notion).


```python
# Load Notion database as a markdownfile file
from langchain.document_loaders import NotionDirectoryLoader
loader = NotionDirectoryLoader("../Notion_DB_Metadata")
docs = loader.load()
md_file=docs[0].page_content
```


```python
# Let's create groups based on the section headers
headers_to_split_on = [
    ("###", "Section"),
]
markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
md_header_splits = markdown_splitter.split_text(md_file)
md_header_splits[3]
```




    {'content': 'We previously introduced [auto-evaluator](https://blog.langchain.dev/auto-evaluator-opportunities/), an open-source tool for grading LLM question-answer chains. Here, we extend auto-evaluator with a [lightweight Streamlit app](https://github.com/langchain-ai/auto-evaluator/tree/main/streamlit) that can connect to any existing Pinecone index. We add the ability to test metadata filtering using `SelfQueryRetriever` as well as some other approaches that we’ve found to be useful, as discussed below.  \n[ret_trim.mov](Auto-Evaluation%20of%20Metadata%20Filtering%2018502448c85240828f33716740f9574b/ret_trim.mov)',
     'metadata': {'Section': 'Evaluation'}}



Now, we split the text in each group and keep the group as metadata.


```python
# Define our text splitter
from langchain.text_splitter import RecursiveCharacterTextSplitter
chunk_size = 500
chunk_overlap = 50
text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
 
# Create splits within each header group
all_splits=[]
all_metadatas=[]
for header_group in md_header_splits:
    _splits = text_splitter.split_text(header_group['content'])
    _metadatas = [header_group['metadata'] for _ in _splits]
    all_splits += _splits
    all_metadatas += _metadatas
```


```python
all_splits[6]
```




    'In these cases, semantic search will look for the concept `episode 53` in the chunks, but instead we simply want to filter the chunks for `episode 53` and then perform semantic search to extract those that best summarize the episode. Metadata filtering does this, so long as we 1) we have a metadata filter for episode number and 2) we can extract the value from the query (e.g., `54` or `252`) that we want to extract. The LangChain `SelfQueryRetriever` does the latter (see'




```python
all_metadatas[6]
```




    {'Section': 'Motivation'}



This sets us up well do perform metadata filtering based on the document structure.

Let's bring this all togther by building a vectorstore first.


```python
! pip install chromadb
```


```python
# Build vectorstore
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_texts(texts=all_splits,metadatas=all_metadatas,embedding=OpenAIEmbeddings())
```

Let's create a `SelfQueryRetriever` that can filter based upon metadata we defined.


```python
# Create retriever 
from langchain.llms import OpenAI
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains.query_constructor.base import AttributeInfo

# Define our metadata
metadata_field_info = [
    AttributeInfo(
        name="Section",
        description="Headers of the markdown document that organize the ideas",
        type="string or list[string]",
    ),
]
document_content_description = "Headers of the markdown document"

# Define self query retriver
llm = OpenAI(temperature=0)
sq_retriever = SelfQueryRetriever.from_llm(llm, vectorstore, document_content_description, metadata_field_info, verbose=True)
```

Now we can fetch chunks specifically from any section of the doc!


```python
# Test
question="Summarize the Introduction section of the document"
sq_retriever.get_relevant_documents(question)
```

    query='Introduction' filter=Comparison(comparator=<Comparator.EQ: 'eq'>, attribute='Section', value='Introduction') limit=None
    




    [Document(page_content='![Untitled](Auto-Evaluation%20of%20Metadata%20Filtering%2018502448c85240828f33716740f9574b/Untitled.png)', metadata={'Section': 'Introduction'}),
     Document(page_content='Q+A systems often use a two-step approach: retrieve relevant text chunks and then synthesize them into an answer. There many ways to approach this. For example, we recently [discussed](https://blog.langchain.dev/auto-evaluation-of-anthropic-100k-context-window/) the Retriever-Less option (at bottom in the below diagram), highlighting the Anthropic 100k context window model. Metadata filtering is an alternative approach that pre-filters chunks based on a user-defined criteria in a VectorDB using', metadata={'Section': 'Introduction'}),
     Document(page_content='on a user-defined criteria in a VectorDB using metadata tags prior to semantic search.', metadata={'Section': 'Introduction'})]



Now, we can create chat or Q+A apps that are aware of the explict document structure. 

Of course, semantic search without specific metadata filtering would probably work reasonably well for this simple document.

But, the ability to retain document structure for metadata filtering can be helpful for more complicated or longer documents.


```python
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
qa_chain = RetrievalQA.from_chain_type(llm,retriever=sq_retriever)
qa_chain.run(question)
```

    query='Introduction' filter=Comparison(comparator=<Comparator.EQ: 'eq'>, attribute='Section', value='Introduction') limit=None
    




    'The document discusses different approaches to retrieve relevant text chunks and synthesize them into an answer in Q+A systems. One of the approaches is metadata filtering, which pre-filters chunks based on user-defined criteria in a VectorDB using metadata tags prior to semantic search. The Retriever-Less option, which uses the Anthropic 100k context window model, is also mentioned as an alternative approach.'




```python
question="Summarize the Testing section of the document"
qa_chain.run(question)
```

    query='Testing' filter=Comparison(comparator=<Comparator.EQ: 'eq'>, attribute='Section', value='Testing') limit=None
    




    'The Testing section of the document describes how the performance of the SelfQueryRetriever was evaluated using various test cases. The tests were designed to evaluate the ability of the SelfQueryRetriever to correctly infer metadata filters from the query using metadata_field_info. The results of the tests showed that the SelfQueryRetriever performed well in some cases, but failed in others. The document also provides a link to the code for the auto-evaluator and instructions on how to use it. Additionally, the document mentions the use of the Kor library for structured data extraction to explicitly specify transformations that the auto-evaluator can use.'


