# Document Comparison

This notebook shows how to use an agent to compare two documents.

The high level idea is we will create a question-answering chain for each document, and then use that 


```python
from pydantic import BaseModel, Field

from langchain.chat_models import ChatOpenAI
from langchain.agents import Tool
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.document_loaders import PyPDFLoader
from langchain.chains import RetrievalQA
```

    /Users/harrisonchase/.pyenv/versions/3.9.1/envs/langchain/lib/python3.9/site-packages/deeplake/util/check_latest_version.py:32: UserWarning: A newer version of deeplake (3.6.4) is available. It's recommended that you update to the latest version using `pip install -U deeplake`.
      warnings.warn(
    


```python
class DocumentInput(BaseModel):
    question: str = Field()


llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")

tools = []
files = [
    # https://abc.xyz/investor/static/pdf/2023Q1_alphabet_earnings_release.pdf
    {
        "name": "alphabet-earnings", 
        "path": "/Users/harrisonchase/Downloads/2023Q1_alphabet_earnings_release.pdf",
    }, 
    # https://digitalassets.tesla.com/tesla-contents/image/upload/IR/TSLA-Q1-2023-Update
    {
        "name": "tesla-earnings", 
        "path": "/Users/harrisonchase/Downloads/TSLA-Q1-2023-Update.pdf"
    }
]

for file in files:
    loader = PyPDFLoader(file["path"])
    pages = loader.load_and_split()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(pages)
    embeddings = OpenAIEmbeddings()
    retriever = FAISS.from_documents(docs, embeddings).as_retriever()
    
    # Wrap retrievers in a Tool
    tools.append(
        Tool(
            args_schema=DocumentInput,
            name=file["name"], 
            description=f"useful when you want to answer questions about {file['name']}",
            func=RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
        )
    )
```


```python
from langchain.agents import initialize_agent
from langchain.agents import AgentType
```


```python
llm = ChatOpenAI(
    temperature=0,
    model="gpt-3.5-turbo-0613", 
)

agent = initialize_agent(
    agent=AgentType.OPENAI_FUNCTIONS,
    tools=tools,
    llm=llm,
    verbose=True,
)

agent({"input": "did alphabet or tesla have more revenue?"})
```

    
    
    [1m> Entering new  chain...[0m
    [32;1m[1;3m
    Invoking: `alphabet-earnings` with `{'question': 'revenue'}`
    
    
    [0m[36;1m[1;3m{'query': 'revenue', 'result': 'The revenue for Alphabet Inc. in the first quarter of 2023 was $69,787 million.'}[0m[32;1m[1;3m
    Invoking: `tesla-earnings` with `{'question': 'revenue'}`
    
    
    [0m[33;1m[1;3m{'query': 'revenue', 'result': 'Total revenue for Q1-2023 was $23.3 billion.'}[0m[32;1m[1;3mAlphabet Inc. had more revenue than Tesla. In the first quarter of 2023, Alphabet Inc. had a revenue of $69,787 million, while Tesla had a revenue of $23.3 billion.[0m
    
    [1m> Finished chain.[0m
    




    {'input': 'did alphabet or tesla have more revenue?',
     'output': 'Alphabet Inc. had more revenue than Tesla. In the first quarter of 2023, Alphabet Inc. had a revenue of $69,787 million, while Tesla had a revenue of $23.3 billion.'}




```python

```
