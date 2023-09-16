# 使用OpenAI函数进行检索问答

OpenAI函数允许对响应输出进行结构化。在问答问题时，除了获取最终答案外，还可以获取支持证据、引用等，这通常很有用。

在这个笔记本中，我们展示了如何使用一个使用OpenAI函数作为整个检索流程的一部分的LLM链。


```python
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
```

    /Users/harrisonchase/.pyenv/versions/3.9.1/envs/langchain/lib/python3.9/site-packages/deeplake/util/check_latest_version.py:32: UserWarning: A newer version of deeplake (3.6.4) is available. It's recommended that you update to the latest version using `pip install -U deeplake`.
      warnings.warn(
    


```python
loader = TextLoader("../../state_of_the_union.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)
for i, text in enumerate(texts):
    text.metadata['source'] = f"{i}-pl"
embeddings = OpenAIEmbeddings()
docsearch = Chroma.from_documents(texts, embeddings)
```

    Using embedded DuckDB without persistence: data will be transient
    


```python
from langchain.chat_models import ChatOpenAI
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.prompts import PromptTemplate
from langchain.chains import create_qa_with_sources_chain
```


```python
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
```


```python
qa_chain = create_qa_with_sources_chain(llm)
```


```python
doc_prompt = PromptTemplate(
    template="Content: {page_content}\nSource: {source}",
    input_variables=["page_content", "source"],
)
```


```python
final_qa_chain = StuffDocumentsChain(
    llm_chain=qa_chain, 
    document_variable_name='context',
    document_prompt=doc_prompt,
)
```


```python
retrieval_qa = RetrievalQA(
    retriever=docsearch.as_retriever(),
    combine_documents_chain=final_qa_chain
)
```


```python
query = "总统对俄罗斯说了什么"
```


```python
retrieval_qa.run(query)
```




    '{\n  "answer": "总统对俄罗斯的行动表示强烈谴责，并宣布采取措施孤立俄罗斯并支持乌克兰。他指出俄罗斯对乌克兰的入侵将对俄罗斯产生长期影响，并强调美国及其盟友捍卫北约国家的承诺。总统还提到对俄罗斯实施制裁，并释放石油储备以帮助缓解天然气价格。总体而言，总统的讲话传达了坚定反对俄罗斯侵略行为、支持乌克兰并保护美国利益的立场。",\n  "sources": ["0-pl", "4-pl", "5-pl", "6-pl"]\n}'



## 使用Pydantic

如果需要，我们可以将链设置为返回Pydantic格式。请注意，如果下游链消耗此链的输出（包括内存），它们通常会希望输出为字符串格式，因此只有在它是最终链时才应使用此链。


```python
qa_chain_pydantic = create_qa_with_sources_chain(llm, output_parser="pydantic")
```


```python
final_qa_chain_pydantic = StuffDocumentsChain(
    llm_chain=qa_chain_pydantic, 
    document_variable_name='context',
    document_prompt=doc_prompt,
)
```


```python
retrieval_qa_pydantic = RetrievalQA(
    retriever=docsearch.as_retriever(),
    combine_documents_chain=final_qa_chain_pydantic
)
```


```python
retrieval_qa_pydantic.run(query)
```




    AnswerWithSources(answer="The President expressed strong condemnation of Russia's actions in Ukraine and announced measures to isolate Russia and provide support to Ukraine. He stated that Russia's invasion of Ukraine will have long-term consequences for Russia and emphasized the commitment of the United States and its allies to defend NATO countries. The President also mentioned the economic impact of sanctions on Russia and the release of oil reserves to help mitigate gas prices. Overall, the President conveyed a message of solidarity with Ukraine and a determination to protect American interests and support freedom.", sources=['0-pl', '4-pl', '5-pl', '6-pl'])



## 在ConversationalRetrievalChain中使用

我们还可以展示在ConversationalRetrievalChain中使用该功能。请注意，因为此链涉及内存，我们将不使用Pydantic返回类型。


```python
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
_template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question, in its original language.\
Make sure to avoid using any unclear pronouns.

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""
CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template)
condense_question_chain = LLMChain(
    llm=llm,
    prompt=CONDENSE_QUESTION_PROMPT,
)
```


```python
qa = ConversationalRetrievalChain(
    question_generator=condense_question_chain, 
    retriever=docsearch.as_retriever(),
    memory=memory, 
    combine_docs_chain=final_qa_chain
)
```


```python
query = "What did the president say about Ketanji Brown Jackson"
result = qa({"question": query})
```


```python
result
```




    {'question': 'What did the president say about Ketanji Brown Jackson',
     'chat_history': [HumanMessage(content='What did the president say about Ketanji Brown Jackson', additional_kwargs={}, example=False),
      AIMessage(content='{\n  "answer": "The President nominated Ketanji Brown Jackson as a Circuit Court of Appeals Judge and praised her as one of the nation\'s top legal minds who will continue Justice Breyer\'s legacy of excellence.",\n  "sources": ["31-pl"]\n}', additional_kwargs={}, example=False)],
     'answer': '{\n  "answer": "The President nominated Ketanji Brown Jackson as a Circuit Court of Appeals Judge and praised her as one of the nation\'s top legal minds who will continue Justice Breyer\'s legacy of excellence.",\n  "sources": ["31-pl"]\n}'}




```python
query = "关于她的前任，他说了什么"
result = qa({"question": query})
```


```python
result
```




    {'question': 'what did he say about her predecessor?',
     'chat_history': [HumanMessage(content='What did the president say about Ketanji Brown Jackson', additional_kwargs={}, example=False),
      AIMessage(content='{\n  "answer": "The President nominated Ketanji Brown Jackson as a Circuit Court of Appeals Judge and praised her as one of the nation\'s top legal minds who will continue Justice Breyer\'s legacy of excellence.",\n  "sources": ["31-pl"]\n}', additional_kwargs={}, example=False),
      HumanMessage(content='what did he say about her predecessor?', additional_kwargs={}, example=False),
      AIMessage(content='{\n  "answer": "The President honored Justice Stephen Breyer for his service as an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court.",\n  "sources": ["31-pl"]\n}', additional_kwargs={}, example=False)],
     'answer': '{\n  "answer": "The President honored Justice Stephen Breyer for his service as an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court.",\n  "sources": ["31-pl"]\n}'}




```python

```
