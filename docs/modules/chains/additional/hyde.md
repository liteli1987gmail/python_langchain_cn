# 虚拟文档嵌入
这个笔记本介绍了如何使用虚拟文档嵌入（HyDE），如[这篇论文](https$：//arxiv.org/abs/2212.10496)所述。

在高层次上，HyDE是一种嵌入技术，它接受查询，生成一个虚拟答案，然后嵌入该生成的文档并将其用作最终示例。

为了使用HyDE，我们需要提供一个基本的嵌入模型，以及一个用于生成这些文档的LLMChain。默认情况下，HyDE类带有一些默认的提示（有关详细信息，请参阅论文），但我们也可以创建自己的提示。

```python
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import LLMChain, HypotheticalDocumentEmbedder
from langchain.prompts import PromptTemplate
```

```python
base_embeddings = OpenAIEmbeddings()
llm = OpenAI()
```




```python
# 使用“web_search”提示进行加载
embeddings = HypotheticalDocumentEmbedder.from_llm(llm, base_embeddings, "web_search")
```

```python
# 现在我们可以像使用任何嵌入类一样使用它！
result = embeddings.embed_query("泰姬陵在哪里？")
```

## 多次生成
我们还可以生成多个文档，然后将这些文档的嵌入组合起来。默认情况下，我们通过取平均值来组合这些文档的嵌入。我们可以通过改变用于生成文档的LLM来实现这一点。

```python
multi_llm = OpenAI(n=4, best_of=4)
```

```python
embeddings = HypotheticalDocumentEmbedder.from_llm(
    multi_llm, base_embeddings, "web_search"
)
```

```python
result = embeddings.embed_query("泰姬陵在哪里？")
```

## 使用我们自己的提示
除了使用预配置的提示外，我们还可以轻松构建自己的提示并在生成文档的LLMChain中使用它们。如果我们知道查询所在的领域，这可能非常有用，因为我们可以将提示调整为生成更类似于该领域的文本。

在下面的示例中，让我们将其调整为生成关于国情咨文的文本（因为我们将在下一个示例中使用它）。

```python
prompt_template = """请回答关于最近一次国情咨文的用户问题
问题$：{question}
回答$："""
prompt = PromptTemplate(input_variables=["question"], template=prompt_template)
llm_chain = LLMChain(llm=llm, prompt=prompt)
```

```python
embeddings = HypotheticalDocumentEmbedder(
    llm_chain=llm_chain, base_embeddings=base_embeddings
)
```

```python
result = embeddings.embed_query(
    "总统在关于Ketanji Brown Jackson的发言中说了什么"
)
```

## 使用HyDE
现在我们有了HyDE，我们可以像使用任何其他嵌入类一样使用它！在这里，我们使用它在国情咨文示例中查找相似的段落。


```python
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma

with open("../../state_of_the_union.txt") as f:
    state_of_the_union = f.read()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_text(state_of_the_union)
```


```python
docsearch = Chroma.from_texts(texts, embeddings)

query = "总统在关于Ketanji Brown Jackson的发言中说了什么"
docs = docsearch.similarity_search(query)
```

    使用直接本地API运行Chroma。
    使用DuckDB内存中的数据库。数据将是临时的。
    

```python
print(docs[0].page_content)
```

    In state after state, new laws have been passed, not only to suppress the vote, but to subvert entire elections. 
    
    We cannot let this happen. 
    
    Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections. 
    
    Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. 
    
    One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. 
    
    And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.
    


```python

```
