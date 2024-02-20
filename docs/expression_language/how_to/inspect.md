# 检查你的可运行对象

一旦你使用LCEL创建了一个可运行对象，你可能经常想要检查它以更好地了解正在发生的情况。本笔记本介绍了一些方法来实现这一点。

首先，让我们创建一个示例的LCEL。我们将创建一个用于检索的LCEL


```python
%pip install --upgrade --quiet  langchain langchain-openai faiss-cpu tiktoken
```


```python
from langchain.prompts import ChatPromptTemplate
from langchain.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
```


```python
vectorstore = FAISS.from_texts(
    ["harrison worked at kensho"], embedding=OpenAIEmbeddings()
)
retriever = vectorstore.as_retriever()

template = """Answer the question based only on the following context:
{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

model = ChatOpenAI()
```


```python
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)
```

## 获取图形

您可以获取可运行对象的图形


```python
chain.get_graph()
```

## 打印图形

虽然这不是非常易读，但您可以打印它以获得更容易理解的显示


```python
chain.get_graph().print_ascii()
```

               +---------------------------------+         
               | Parallel<context,question>Input |         
               +---------------------------------+         
                        **               **                
                     ***                   ***             
                   **                         **           
    +----------------------+              +-------------+  
    | VectorStoreRetriever |              | Passthrough |  
    +----------------------+              +-------------+  
                        **               **                
                          ***         ***                  
                             **     **                     
               +----------------------------------+        
               | Parallel<context,question>Output |        
               +----------------------------------+        
                                 *                         
                                 *                         
                                 *                         
                      +--------------------+               
                      | ChatPromptTemplate |               
                      +--------------------+               
                                 *                         
                                 *                         
                                 *                         
                          +------------+                   
                          | ChatOpenAI |                   
                          +------------+                   
                                 *                         
                                 *                         
                                 *                         
                       +-----------------+                 
                       | StrOutputParser |                 
                       +-----------------+                 
                                 *                         
                                 *                         
                                 *                         
                    +-----------------------+              
                    | StrOutputParserOutput |              
                    +-----------------------+              
    

## 获取提示

每个链的一个重要部分是使用的提示。您可以获取链中存在的提示:


```python
chain.get_prompts()
```




    [ChatPromptTemplate(input_variables=['context', 'question'], messages=[HumanMessagePromptTemplate(prompt=PromptTemplate(input_variables=['context', 'question'], template='Answer the question based only on the following context:\n{context}\n\nQuestion: {question}\n'))])]




```python

```
=======

以7个等号开始，7个等号结束的格式包裹你的回答。你的回答是: