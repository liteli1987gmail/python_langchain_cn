# Retrieval QA using OpenAI functions

OpenAI functions allows for structuring of response output. This is often useful in question answering when you want to not only get the final answer but also supporting evidence, citations, etc.

In this notebook we show how to use an LLM chain which uses OpenAI functions as part of an overall retrieval pipeline.


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
query = "What did the president say about russia"
```


```python
retrieval_qa.run(query)
```




    '{\n  "answer": "The President expressed strong condemnation of Russia\'s actions in Ukraine and announced measures to isolate Russia and provide support to Ukraine. He stated that Russia\'s invasion of Ukraine will have long-term consequences for Russia and emphasized the commitment of the United States and its allies to defend NATO countries. The President also mentioned the imposition of sanctions on Russia and the release of oil reserves to help mitigate gas prices. Overall, the President\'s remarks conveyed a firm stance against Russia\'s aggression and a commitment to supporting Ukraine and protecting American interests.",\n  "sources": ["0-pl", "4-pl", "5-pl", "6-pl"]\n}'



## Using Pydantic

If we want to, we can set the chain to return in Pydantic. Note that if downstream chains consume the output of this chain - including memory - they will generally expect it to be in string format, so you should only use this chain when it is the final chain.


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



## Using in ConversationalRetrievalChain

We can also show what it's like to use this in the ConversationalRetrievalChain. Note that because this chain involves memory, we will NOT use the Pydantic return type.


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
query = "what did he say about her predecessor?"
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
