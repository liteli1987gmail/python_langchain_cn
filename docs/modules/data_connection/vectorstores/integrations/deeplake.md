#  Deep Lake

>[Deep Lake](https://docs.activeloop.ai/) as a Multi-Modal Vector Store that stores embeddings and their metadata including text, jsons, images, audio, video, and more. It saves the data locally, in your cloud, or on Activeloop storage. It performs hybrid search including embeddings and their attributes.

This notebook showcases basic functionality related to `Deep Lake`. While `Deep Lake` can store embeddings, it is capable of storing any type of data. It is a fully fledged serverless data lake with version control, query engine and streaming dataloader to deep learning frameworks.  

For more information, please see the Deep Lake [documentation](https://docs.activeloop.ai) or [api reference](https://docs.deeplake.ai)


```python
!pip install openai deeplake tiktoken
```


```python
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import DeepLake
```


```python
import os
import getpass

os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:")
activeloop_token = getpass.getpass("activeloop token:")
embeddings = OpenAIEmbeddings()
```


```python
from langchain.document_loaders import TextLoader

loader = TextLoader("docs/modules/state_of_the_union.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
```

Create a dataset locally at `./deeplake/`, then run similiarity search. The Deeplake+LangChain integration uses Deep Lake datasets under the hood, so `dataset` and `vector store` are used interchangeably. To create a dataset in your own cloud, or in the Deep Lake storage, [adjust the path accordingly](https://docs.activeloop.ai/storage-and-credentials/storage-options).


```python
db = DeepLake(
    dataset_path="./my_deeplake/", embedding_function=embeddings, overwrite=True
)
db.add_documents(docs)
# or shorter
# db = DeepLake.from_documents(docs, dataset_path="./my_deeplake/", embedding=embeddings, overwrite=True)
query = "What did the president say about Ketanji Brown Jackson"
docs = db.similarity_search(query)
```

    

    Dataset(path='./my_deeplake/', tensors=['embedding', 'id', 'metadata', 'text'])
    
      tensor      htype      shape      dtype  compression
      -------    -------    -------    -------  ------- 
     embedding  embedding  (42, 1536)  float32   None   
        id        text      (42, 1)      str     None   
     metadata     json      (42, 1)      str     None   
       text       text      (42, 1)      str     None   
    


```python
print(docs[0].page_content)
```

    Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections. 
    
    Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. 
    
    One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. 
    
    And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.
    

Later, you can reload the dataset without recomputing embeddings


```python
db = DeepLake(
    dataset_path="./my_deeplake/", embedding_function=embeddings, read_only=True
)
docs = db.similarity_search(query)
```

    Deep Lake Dataset in ./my_deeplake/ already exists, loading from the storage
    

Deep Lake, for now, is single writer and multiple reader. Setting `read_only=True` helps to avoid acquring the writer lock.

### Retrieval Question/Answering


```python
from langchain.chains import RetrievalQA
from langchain.llms import OpenAIChat

qa = RetrievalQA.from_chain_type(
    llm=OpenAIChat(model="gpt-3.5-turbo"),
    chain_type="stuff",
    retriever=db.as_retriever(),
)
```

    /Users/adilkhansarsen/Documents/work/LangChain/langchain/langchain/llms/openai.py:751: UserWarning: You are trying to use a chat model. This way of initializing it is no longer supported. Instead, please use: `from langchain.chat_models import ChatOpenAI`
      warnings.warn(
    


```python
query = "What did the president say about Ketanji Brown Jackson"
qa.run(query)
```




    'The President nominated Ketanji Brown Jackson to serve on the United States Supreme Court and spoke highly of her legal expertise and reputation as a consensus builder.'



### Attribute based filtering in metadata


```python
import random

for d in docs:
    d.metadata["year"] = random.randint(2012, 2014)

db = DeepLake.from_documents(
    docs, embeddings, dataset_path="./my_deeplake/", overwrite=True
)
```

    

    Dataset(path='./my_deeplake/', tensors=['embedding', 'id', 'metadata', 'text'])
    
      tensor      htype      shape     dtype  compression
      -------    -------    -------   -------  ------- 
     embedding  embedding  (4, 1536)  float32   None   
        id        text      (4, 1)      str     None   
     metadata     json      (4, 1)      str     None   
       text       text      (4, 1)      str     None   
    

    


```python
db.similarity_search(
    "What did the president say about Ketanji Brown Jackson",
    filter={"metadata": {"year": 2013}},
)
```

    100%|██████████| 4/4 [00:00<00:00, 3300.00it/s]
    




    [Document(lc_kwargs={'page_content': 'Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections. \n\nTonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. \n\nOne of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. \n\nAnd I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.', 'metadata': {'source': 'docs/modules/state_of_the_union.txt', 'year': 2013}}, page_content='Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections. \n\nTonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. \n\nOne of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. \n\nAnd I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.', metadata={'source': 'docs/modules/state_of_the_union.txt', 'year': 2013}),
     Document(lc_kwargs={'page_content': 'A former top litigator in private practice. A former federal public defender. And from a family of public school educators and police officers. A consensus builder. Since she’s been nominated, she’s received a broad range of support—from the Fraternal Order of Police to former judges appointed by Democrats and Republicans. \n\nAnd if we are to advance liberty and justice, we need to secure the Border and fix the immigration system. \n\nWe can do both. At our border, we’ve installed new technology like cutting-edge scanners to better detect drug smuggling.  \n\nWe’ve set up joint patrols with Mexico and Guatemala to catch more human traffickers.  \n\nWe’re putting in place dedicated immigration judges so families fleeing persecution and violence can have their cases heard faster. \n\nWe’re securing commitments and supporting partners in South and Central America to host more refugees and secure their own borders.', 'metadata': {'source': 'docs/modules/state_of_the_union.txt', 'year': 2013}}, page_content='A former top litigator in private practice. A former federal public defender. And from a family of public school educators and police officers. A consensus builder. Since she’s been nominated, she’s received a broad range of support—from the Fraternal Order of Police to former judges appointed by Democrats and Republicans. \n\nAnd if we are to advance liberty and justice, we need to secure the Border and fix the immigration system. \n\nWe can do both. At our border, we’ve installed new technology like cutting-edge scanners to better detect drug smuggling.  \n\nWe’ve set up joint patrols with Mexico and Guatemala to catch more human traffickers.  \n\nWe’re putting in place dedicated immigration judges so families fleeing persecution and violence can have their cases heard faster. \n\nWe’re securing commitments and supporting partners in South and Central America to host more refugees and secure their own borders.', metadata={'source': 'docs/modules/state_of_the_union.txt', 'year': 2013}),
     Document(lc_kwargs={'page_content': 'Tonight, I’m announcing a crackdown on these companies overcharging American businesses and consumers. \n\nAnd as Wall Street firms take over more nursing homes, quality in those homes has gone down and costs have gone up.  \n\nThat ends on my watch. \n\nMedicare is going to set higher standards for nursing homes and make sure your loved ones get the care they deserve and expect. \n\nWe’ll also cut costs and keep the economy going strong by giving workers a fair shot, provide more training and apprenticeships, hire them based on their skills not degrees. \n\nLet’s pass the Paycheck Fairness Act and paid leave.  \n\nRaise the minimum wage to $15 an hour and extend the Child Tax Credit, so no one has to raise a family in poverty. \n\nLet’s increase Pell Grants and increase our historic support of HBCUs, and invest in what Jill—our First Lady who teaches full-time—calls America’s best-kept secret: community colleges.', 'metadata': {'source': 'docs/modules/state_of_the_union.txt', 'year': 2013}}, page_content='Tonight, I’m announcing a crackdown on these companies overcharging American businesses and consumers. \n\nAnd as Wall Street firms take over more nursing homes, quality in those homes has gone down and costs have gone up.  \n\nThat ends on my watch. \n\nMedicare is going to set higher standards for nursing homes and make sure your loved ones get the care they deserve and expect. \n\nWe’ll also cut costs and keep the economy going strong by giving workers a fair shot, provide more training and apprenticeships, hire them based on their skills not degrees. \n\nLet’s pass the Paycheck Fairness Act and paid leave.  \n\nRaise the minimum wage to $15 an hour and extend the Child Tax Credit, so no one has to raise a family in poverty. \n\nLet’s increase Pell Grants and increase our historic support of HBCUs, and invest in what Jill—our First Lady who teaches full-time—calls America’s best-kept secret: community colleges.', metadata={'source': 'docs/modules/state_of_the_union.txt', 'year': 2013})]



### Choosing distance function
Distance function `L2` for Euclidean, `L1` for Nuclear, `Max` l-infinity distnace, `cos` for cosine similarity, `dot` for dot product 


```python
db.similarity_search(
    "What did the president say about Ketanji Brown Jackson?", distance_metric="cos"
)
```




    [Document(lc_kwargs={'page_content': 'Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections. \n\nTonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. \n\nOne of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. \n\nAnd I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.', 'metadata': {'source': 'docs/modules/state_of_the_union.txt', 'year': 2013}}, page_content='Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections. \n\nTonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. \n\nOne of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. \n\nAnd I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.', metadata={'source': 'docs/modules/state_of_the_union.txt', 'year': 2013}),
     Document(lc_kwargs={'page_content': 'A former top litigator in private practice. A former federal public defender. And from a family of public school educators and police officers. A consensus builder. Since she’s been nominated, she’s received a broad range of support—from the Fraternal Order of Police to former judges appointed by Democrats and Republicans. \n\nAnd if we are to advance liberty and justice, we need to secure the Border and fix the immigration system. \n\nWe can do both. At our border, we’ve installed new technology like cutting-edge scanners to better detect drug smuggling.  \n\nWe’ve set up joint patrols with Mexico and Guatemala to catch more human traffickers.  \n\nWe’re putting in place dedicated immigration judges so families fleeing persecution and violence can have their cases heard faster. \n\nWe’re securing commitments and supporting partners in South and Central America to host more refugees and secure their own borders.', 'metadata': {'source': 'docs/modules/state_of_the_union.txt', 'year': 2013}}, page_content='A former top litigator in private practice. A former federal public defender. And from a family of public school educators and police officers. A consensus builder. Since she’s been nominated, she’s received a broad range of support—from the Fraternal Order of Police to former judges appointed by Democrats and Republicans. \n\nAnd if we are to advance liberty and justice, we need to secure the Border and fix the immigration system. \n\nWe can do both. At our border, we’ve installed new technology like cutting-edge scanners to better detect drug smuggling.  \n\nWe’ve set up joint patrols with Mexico and Guatemala to catch more human traffickers.  \n\nWe’re putting in place dedicated immigration judges so families fleeing persecution and violence can have their cases heard faster. \n\nWe’re securing commitments and supporting partners in South and Central America to host more refugees and secure their own borders.', metadata={'source': 'docs/modules/state_of_the_union.txt', 'year': 2013}),
     Document(lc_kwargs={'page_content': 'Tonight, I’m announcing a crackdown on these companies overcharging American businesses and consumers. \n\nAnd as Wall Street firms take over more nursing homes, quality in those homes has gone down and costs have gone up.  \n\nThat ends on my watch. \n\nMedicare is going to set higher standards for nursing homes and make sure your loved ones get the care they deserve and expect. \n\nWe’ll also cut costs and keep the economy going strong by giving workers a fair shot, provide more training and apprenticeships, hire them based on their skills not degrees. \n\nLet’s pass the Paycheck Fairness Act and paid leave.  \n\nRaise the minimum wage to $15 an hour and extend the Child Tax Credit, so no one has to raise a family in poverty. \n\nLet’s increase Pell Grants and increase our historic support of HBCUs, and invest in what Jill—our First Lady who teaches full-time—calls America’s best-kept secret: community colleges.', 'metadata': {'source': 'docs/modules/state_of_the_union.txt', 'year': 2013}}, page_content='Tonight, I’m announcing a crackdown on these companies overcharging American businesses and consumers. \n\nAnd as Wall Street firms take over more nursing homes, quality in those homes has gone down and costs have gone up.  \n\nThat ends on my watch. \n\nMedicare is going to set higher standards for nursing homes and make sure your loved ones get the care they deserve and expect. \n\nWe’ll also cut costs and keep the economy going strong by giving workers a fair shot, provide more training and apprenticeships, hire them based on their skills not degrees. \n\nLet’s pass the Paycheck Fairness Act and paid leave.  \n\nRaise the minimum wage to $15 an hour and extend the Child Tax Credit, so no one has to raise a family in poverty. \n\nLet’s increase Pell Grants and increase our historic support of HBCUs, and invest in what Jill—our First Lady who teaches full-time—calls America’s best-kept secret: community colleges.', metadata={'source': 'docs/modules/state_of_the_union.txt', 'year': 2013}),
     Document(lc_kwargs={'page_content': 'And for our LGBTQ+ Americans, let’s finally get the bipartisan Equality Act to my desk. The onslaught of state laws targeting transgender Americans and their families is wrong. \n\nAs I said last year, especially to our younger transgender Americans, I will always have your back as your President, so you can be yourself and reach your God-given potential. \n\nWhile it often appears that we never agree, that isn’t true. I signed 80 bipartisan bills into law last year. From preventing government shutdowns to protecting Asian-Americans from still-too-common hate crimes to reforming military justice. \n\nAnd soon, we’ll strengthen the Violence Against Women Act that I first wrote three decades ago. It is important for us to show the nation that we can come together and do big things. \n\nSo tonight I’m offering a Unity Agenda for the Nation. Four big things we can do together.  \n\nFirst, beat the opioid epidemic.', 'metadata': {'source': 'docs/modules/state_of_the_union.txt', 'year': 2012}}, page_content='And for our LGBTQ+ Americans, let’s finally get the bipartisan Equality Act to my desk. The onslaught of state laws targeting transgender Americans and their families is wrong. \n\nAs I said last year, especially to our younger transgender Americans, I will always have your back as your President, so you can be yourself and reach your God-given potential. \n\nWhile it often appears that we never agree, that isn’t true. I signed 80 bipartisan bills into law last year. From preventing government shutdowns to protecting Asian-Americans from still-too-common hate crimes to reforming military justice. \n\nAnd soon, we’ll strengthen the Violence Against Women Act that I first wrote three decades ago. It is important for us to show the nation that we can come together and do big things. \n\nSo tonight I’m offering a Unity Agenda for the Nation. Four big things we can do together.  \n\nFirst, beat the opioid epidemic.', metadata={'source': 'docs/modules/state_of_the_union.txt', 'year': 2012})]



### Maximal Marginal relevance
Using maximal marginal relevance


```python
db.max_marginal_relevance_search(
    "What did the president say about Ketanji Brown Jackson?"
)
```




    [Document(lc_kwargs={'page_content': 'Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections. \n\nTonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. \n\nOne of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. \n\nAnd I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.', 'metadata': {'source': 'docs/modules/state_of_the_union.txt', 'year': 2013}}, page_content='Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections. \n\nTonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. \n\nOne of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. \n\nAnd I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.', metadata={'source': 'docs/modules/state_of_the_union.txt', 'year': 2013}),
     Document(lc_kwargs={'page_content': 'Tonight, I’m announcing a crackdown on these companies overcharging American businesses and consumers. \n\nAnd as Wall Street firms take over more nursing homes, quality in those homes has gone down and costs have gone up.  \n\nThat ends on my watch. \n\nMedicare is going to set higher standards for nursing homes and make sure your loved ones get the care they deserve and expect. \n\nWe’ll also cut costs and keep the economy going strong by giving workers a fair shot, provide more training and apprenticeships, hire them based on their skills not degrees. \n\nLet’s pass the Paycheck Fairness Act and paid leave.  \n\nRaise the minimum wage to $15 an hour and extend the Child Tax Credit, so no one has to raise a family in poverty. \n\nLet’s increase Pell Grants and increase our historic support of HBCUs, and invest in what Jill—our First Lady who teaches full-time—calls America’s best-kept secret: community colleges.', 'metadata': {'source': 'docs/modules/state_of_the_union.txt', 'year': 2013}}, page_content='Tonight, I’m announcing a crackdown on these companies overcharging American businesses and consumers. \n\nAnd as Wall Street firms take over more nursing homes, quality in those homes has gone down and costs have gone up.  \n\nThat ends on my watch. \n\nMedicare is going to set higher standards for nursing homes and make sure your loved ones get the care they deserve and expect. \n\nWe’ll also cut costs and keep the economy going strong by giving workers a fair shot, provide more training and apprenticeships, hire them based on their skills not degrees. \n\nLet’s pass the Paycheck Fairness Act and paid leave.  \n\nRaise the minimum wage to $15 an hour and extend the Child Tax Credit, so no one has to raise a family in poverty. \n\nLet’s increase Pell Grants and increase our historic support of HBCUs, and invest in what Jill—our First Lady who teaches full-time—calls America’s best-kept secret: community colleges.', metadata={'source': 'docs/modules/state_of_the_union.txt', 'year': 2013}),
     Document(lc_kwargs={'page_content': 'A former top litigator in private practice. A former federal public defender. And from a family of public school educators and police officers. A consensus builder. Since she’s been nominated, she’s received a broad range of support—from the Fraternal Order of Police to former judges appointed by Democrats and Republicans. \n\nAnd if we are to advance liberty and justice, we need to secure the Border and fix the immigration system. \n\nWe can do both. At our border, we’ve installed new technology like cutting-edge scanners to better detect drug smuggling.  \n\nWe’ve set up joint patrols with Mexico and Guatemala to catch more human traffickers.  \n\nWe’re putting in place dedicated immigration judges so families fleeing persecution and violence can have their cases heard faster. \n\nWe’re securing commitments and supporting partners in South and Central America to host more refugees and secure their own borders.', 'metadata': {'source': 'docs/modules/state_of_the_union.txt', 'year': 2013}}, page_content='A former top litigator in private practice. A former federal public defender. And from a family of public school educators and police officers. A consensus builder. Since she’s been nominated, she’s received a broad range of support—from the Fraternal Order of Police to former judges appointed by Democrats and Republicans. \n\nAnd if we are to advance liberty and justice, we need to secure the Border and fix the immigration system. \n\nWe can do both. At our border, we’ve installed new technology like cutting-edge scanners to better detect drug smuggling.  \n\nWe’ve set up joint patrols with Mexico and Guatemala to catch more human traffickers.  \n\nWe’re putting in place dedicated immigration judges so families fleeing persecution and violence can have their cases heard faster. \n\nWe’re securing commitments and supporting partners in South and Central America to host more refugees and secure their own borders.', metadata={'source': 'docs/modules/state_of_the_union.txt', 'year': 2013}),
     Document(lc_kwargs={'page_content': 'And for our LGBTQ+ Americans, let’s finally get the bipartisan Equality Act to my desk. The onslaught of state laws targeting transgender Americans and their families is wrong. \n\nAs I said last year, especially to our younger transgender Americans, I will always have your back as your President, so you can be yourself and reach your God-given potential. \n\nWhile it often appears that we never agree, that isn’t true. I signed 80 bipartisan bills into law last year. From preventing government shutdowns to protecting Asian-Americans from still-too-common hate crimes to reforming military justice. \n\nAnd soon, we’ll strengthen the Violence Against Women Act that I first wrote three decades ago. It is important for us to show the nation that we can come together and do big things. \n\nSo tonight I’m offering a Unity Agenda for the Nation. Four big things we can do together.  \n\nFirst, beat the opioid epidemic.', 'metadata': {'source': 'docs/modules/state_of_the_union.txt', 'year': 2012}}, page_content='And for our LGBTQ+ Americans, let’s finally get the bipartisan Equality Act to my desk. The onslaught of state laws targeting transgender Americans and their families is wrong. \n\nAs I said last year, especially to our younger transgender Americans, I will always have your back as your President, so you can be yourself and reach your God-given potential. \n\nWhile it often appears that we never agree, that isn’t true. I signed 80 bipartisan bills into law last year. From preventing government shutdowns to protecting Asian-Americans from still-too-common hate crimes to reforming military justice. \n\nAnd soon, we’ll strengthen the Violence Against Women Act that I first wrote three decades ago. It is important for us to show the nation that we can come together and do big things. \n\nSo tonight I’m offering a Unity Agenda for the Nation. Four big things we can do together.  \n\nFirst, beat the opioid epidemic.', metadata={'source': 'docs/modules/state_of_the_union.txt', 'year': 2012})]



### Delete dataset


```python
db.delete_dataset()
```

    

and if delete fails you can also force delete


```python
DeepLake.force_delete_by_path("./my_deeplake")
```

    

## Deep Lake datasets on cloud (Activeloop, AWS, GCS, etc.) or in memory
By default deep lake datasets are stored locally, in case you want to store them in memory, in the Deep Lake Managed DB, or in any object storage, you can provide the [corresponding path to the dataset](https://docs.activeloop.ai/storage-and-credentials/storage-options). You can retrieve your user token from [app.activeloop.ai](https://app.activeloop.ai/)


```python
os.environ["ACTIVELOOP_TOKEN"] = activeloop_token
```

Deeplake now supports running the inference in 3 modes. `python` naive way of searching inside of the data, `tensor_db` which is managed database, it runs tql on a remote optimized engine and sends results back, and `compute_engine` which is C++ implementation of search that runs locally.


```python
# Embed and store the texts
username = "<username>"  # your username on app.activeloop.ai
dataset_path = f"hub://{username}/langchain_testing_python"  # could be also ./local/path (much faster locally), s3://bucket/path/to/dataset, gcs://path/to/dataset, etc.

docs = text_splitter.split_documents(documents)

embedding = OpenAIEmbeddings()
db = DeepLake(dataset_path=dataset_path, embedding_function=embeddings, overwrite=True)
db.add_documents(docs)
```

    Your Deep Lake dataset has been successfully created!
    The dataset is private so make sure you are logged in!
    

    -

    Dataset(path='hub://adilkhan/langchain_testing_python', tensors=['embedding', 'id', 'metadata', 'text'])
    
      tensor      htype      shape      dtype  compression
      -------    -------    -------    -------  ------- 
     embedding  embedding  (42, 1536)  float32   None   
        id        text      (42, 1)      str     None   
     metadata     json      (42, 1)      str     None   
       text       text      (42, 1)      str     None   
    

     




    ['d604b1ac-093c-11ee-bdba-76d8a30504e0',
     'd604b238-093c-11ee-bdba-76d8a30504e0',
     'd604b260-093c-11ee-bdba-76d8a30504e0',
     'd604b27e-093c-11ee-bdba-76d8a30504e0',
     'd604b29c-093c-11ee-bdba-76d8a30504e0',
     'd604b2ba-093c-11ee-bdba-76d8a30504e0',
     'd604b2d8-093c-11ee-bdba-76d8a30504e0',
     'd604b2f6-093c-11ee-bdba-76d8a30504e0',
     'd604b314-093c-11ee-bdba-76d8a30504e0',
     'd604b332-093c-11ee-bdba-76d8a30504e0',
     'd604b350-093c-11ee-bdba-76d8a30504e0',
     'd604b36e-093c-11ee-bdba-76d8a30504e0',
     'd604b38c-093c-11ee-bdba-76d8a30504e0',
     'd604b3a0-093c-11ee-bdba-76d8a30504e0',
     'd604b3be-093c-11ee-bdba-76d8a30504e0',
     'd604b3dc-093c-11ee-bdba-76d8a30504e0',
     'd604b3fa-093c-11ee-bdba-76d8a30504e0',
     'd604b418-093c-11ee-bdba-76d8a30504e0',
     'd604b436-093c-11ee-bdba-76d8a30504e0',
     'd604b454-093c-11ee-bdba-76d8a30504e0',
     'd604b472-093c-11ee-bdba-76d8a30504e0',
     'd604b490-093c-11ee-bdba-76d8a30504e0',
     'd604b4a4-093c-11ee-bdba-76d8a30504e0',
     'd604b4c2-093c-11ee-bdba-76d8a30504e0',
     'd604b4e0-093c-11ee-bdba-76d8a30504e0',
     'd604b4fe-093c-11ee-bdba-76d8a30504e0',
     'd604b51c-093c-11ee-bdba-76d8a30504e0',
     'd604b53a-093c-11ee-bdba-76d8a30504e0',
     'd604b558-093c-11ee-bdba-76d8a30504e0',
     'd604b576-093c-11ee-bdba-76d8a30504e0',
     'd604b594-093c-11ee-bdba-76d8a30504e0',
     'd604b5b2-093c-11ee-bdba-76d8a30504e0',
     'd604b5c6-093c-11ee-bdba-76d8a30504e0',
     'd604b5e4-093c-11ee-bdba-76d8a30504e0',
     'd604b602-093c-11ee-bdba-76d8a30504e0',
     'd604b620-093c-11ee-bdba-76d8a30504e0',
     'd604b63e-093c-11ee-bdba-76d8a30504e0',
     'd604b65c-093c-11ee-bdba-76d8a30504e0',
     'd604b67a-093c-11ee-bdba-76d8a30504e0',
     'd604b698-093c-11ee-bdba-76d8a30504e0',
     'd604b6b6-093c-11ee-bdba-76d8a30504e0',
     'd604b6d4-093c-11ee-bdba-76d8a30504e0']




```python
query = "What did the president say about Ketanji Brown Jackson"
docs = db.similarity_search(query)
print(docs[0].page_content)
```

    Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections. 
    
    Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. 
    
    One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. 
    
    And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.
    


```python
# Embed and store the texts
username = "adilkhan"  # your username on app.activeloop.ai
dataset_path = f"hub://{username}/langchain_testing"  # could be also ./local/path (much faster locally), s3://bucket/path/to/dataset, gcs://path/to/dataset, etc.

docs = text_splitter.split_documents(documents)

embedding = OpenAIEmbeddings()
db = DeepLake(
    dataset_path=dataset_path,
    embedding_function=embeddings,
    overwrite=True,
    exec_option="tensor_db",
)
db.add_documents(docs)
```

    Your Deep Lake dataset has been successfully created!
    The dataset is private so make sure you are logged in!
    

    |

    Dataset(path='hub://adilkhan/langchain_testing', tensors=['embedding', 'id', 'metadata', 'text'])
    
      tensor      htype      shape      dtype  compression
      -------    -------    -------    -------  ------- 
     embedding  embedding  (42, 1536)  float32   None   
        id        text      (42, 1)      str     None   
     metadata     json      (42, 1)      str     None   
       text       text      (42, 1)      str     None   
    

     




    ['6584c33a-093d-11ee-bdba-76d8a30504e0',
     '6584c3ee-093d-11ee-bdba-76d8a30504e0',
     '6584c420-093d-11ee-bdba-76d8a30504e0',
     '6584c43e-093d-11ee-bdba-76d8a30504e0',
     '6584c466-093d-11ee-bdba-76d8a30504e0',
     '6584c484-093d-11ee-bdba-76d8a30504e0',
     '6584c4a2-093d-11ee-bdba-76d8a30504e0',
     '6584c4c0-093d-11ee-bdba-76d8a30504e0',
     '6584c4de-093d-11ee-bdba-76d8a30504e0',
     '6584c4fc-093d-11ee-bdba-76d8a30504e0',
     '6584c51a-093d-11ee-bdba-76d8a30504e0',
     '6584c538-093d-11ee-bdba-76d8a30504e0',
     '6584c556-093d-11ee-bdba-76d8a30504e0',
     '6584c574-093d-11ee-bdba-76d8a30504e0',
     '6584c592-093d-11ee-bdba-76d8a30504e0',
     '6584c5b0-093d-11ee-bdba-76d8a30504e0',
     '6584c5ce-093d-11ee-bdba-76d8a30504e0',
     '6584c5f6-093d-11ee-bdba-76d8a30504e0',
     '6584c614-093d-11ee-bdba-76d8a30504e0',
     '6584c632-093d-11ee-bdba-76d8a30504e0',
     '6584c646-093d-11ee-bdba-76d8a30504e0',
     '6584c66e-093d-11ee-bdba-76d8a30504e0',
     '6584c682-093d-11ee-bdba-76d8a30504e0',
     '6584c6a0-093d-11ee-bdba-76d8a30504e0',
     '6584c6be-093d-11ee-bdba-76d8a30504e0',
     '6584c6e6-093d-11ee-bdba-76d8a30504e0',
     '6584c704-093d-11ee-bdba-76d8a30504e0',
     '6584c722-093d-11ee-bdba-76d8a30504e0',
     '6584c740-093d-11ee-bdba-76d8a30504e0',
     '6584c75e-093d-11ee-bdba-76d8a30504e0',
     '6584c77c-093d-11ee-bdba-76d8a30504e0',
     '6584c79a-093d-11ee-bdba-76d8a30504e0',
     '6584c7ae-093d-11ee-bdba-76d8a30504e0',
     '6584c7cc-093d-11ee-bdba-76d8a30504e0',
     '6584c7ea-093d-11ee-bdba-76d8a30504e0',
     '6584c808-093d-11ee-bdba-76d8a30504e0',
     '6584c826-093d-11ee-bdba-76d8a30504e0',
     '6584c844-093d-11ee-bdba-76d8a30504e0',
     '6584c862-093d-11ee-bdba-76d8a30504e0',
     '6584c876-093d-11ee-bdba-76d8a30504e0',
     '6584c894-093d-11ee-bdba-76d8a30504e0',
     '6584c8bc-093d-11ee-bdba-76d8a30504e0']




```python
query = "What did the president say about Ketanji Brown Jackson"
docs = db.similarity_search(query, exec_option="tensor_db")
print(docs[0].page_content)
```

    Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections. 
    
    Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. 
    
    One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. 
    
    And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.
    

##### The difference will be apparent on a bigger datasets (~10000 rows)

### TQL Search

now we can use tql search with DeepLake


```python
search_id = db.vectorstore.dataset.id[0].numpy()
```


```python
docs = db.similarity_search(
    query=None,
    tql_query=f"SELECT * WHERE id == '{search_id[0]}'",
    exec_option="tensor_db",
)
```


```python
docs
```




    [Document(lc_kwargs={'page_content': 'Madam Speaker, Madam Vice President, our First Lady and Second Gentleman. Members of Congress and the Cabinet. Justices of the Supreme Court. My fellow Americans.  \n\nLast year COVID-19 kept us apart. This year we are finally together again. \n\nTonight, we meet as Democrats Republicans and Independents. But most importantly as Americans. \n\nWith a duty to one another to the American people to the Constitution. \n\nAnd with an unwavering resolve that freedom will always triumph over tyranny. \n\nSix days ago, Russia’s Vladimir Putin sought to shake the foundations of the free world thinking he could make it bend to his menacing ways. But he badly miscalculated. \n\nHe thought he could roll into Ukraine and the world would roll over. Instead he met a wall of strength he never imagined. \n\nHe met the Ukrainian people. \n\nFrom President Zelenskyy to every Ukrainian, their fearlessness, their courage, their determination, inspires the world.', 'metadata': {'source': 'docs/modules/state_of_the_union.txt'}}, page_content='Madam Speaker, Madam Vice President, our First Lady and Second Gentleman. Members of Congress and the Cabinet. Justices of the Supreme Court. My fellow Americans.  \n\nLast year COVID-19 kept us apart. This year we are finally together again. \n\nTonight, we meet as Democrats Republicans and Independents. But most importantly as Americans. \n\nWith a duty to one another to the American people to the Constitution. \n\nAnd with an unwavering resolve that freedom will always triumph over tyranny. \n\nSix days ago, Russia’s Vladimir Putin sought to shake the foundations of the free world thinking he could make it bend to his menacing ways. But he badly miscalculated. \n\nHe thought he could roll into Ukraine and the world would roll over. Instead he met a wall of strength he never imagined. \n\nHe met the Ukrainian people. \n\nFrom President Zelenskyy to every Ukrainian, their fearlessness, their courage, their determination, inspires the world.', metadata={'source': 'docs/modules/state_of_the_union.txt'})]



### Creating dataset on AWS S3


```python
dataset_path = f"s3://BUCKET/langchain_test"  # could be also ./local/path (much faster locally), hub://bucket/path/to/dataset, gcs://path/to/dataset, etc.

embedding = OpenAIEmbeddings()
db = DeepLake.from_documents(
    docs,
    dataset_path=dataset_path,
    embedding=embeddings,
    overwrite=True,
    creds={
        "aws_access_key_id": os.environ["AWS_ACCESS_KEY_ID"],
        "aws_secret_access_key": os.environ["AWS_SECRET_ACCESS_KEY"],
        "aws_session_token": os.environ["AWS_SESSION_TOKEN"],  # Optional
    },
)
```

    s3://hub-2.0-datasets-n/langchain_test loaded successfully.
    

    Evaluating ingest: 100%|██████████| 1/1 [00:10<00:00
    \

    Dataset(path='s3://hub-2.0-datasets-n/langchain_test', tensors=['embedding', 'ids', 'metadata', 'text'])
    
      tensor     htype     shape     dtype  compression
      -------   -------   -------   -------  ------- 
     embedding  generic  (4, 1536)  float32   None   
        ids      text     (4, 1)      str     None   
     metadata    json     (4, 1)      str     None   
       text      text     (4, 1)      str     None   
    

     

## Deep Lake API
you can access the Deep Lake  dataset at `db.ds`


```python
# get structure of the dataset
db.vectorstore.summary()
```

    Dataset(path='hub://adilkhan/langchain_testing', tensors=['embedding', 'id', 'metadata', 'text'])
    
      tensor      htype      shape      dtype  compression
      -------    -------    -------    -------  ------- 
     embedding  embedding  (42, 1536)  float32   None   
        id        text      (42, 1)      str     None   
     metadata     json      (42, 1)      str     None   
       text       text      (42, 1)      str     None   
    


```python
# get embeddings numpy array
embeds = db.vectorstore.dataset.embedding.numpy()
```

### Transfer local dataset to cloud
Copy already created dataset to the cloud. You can also transfer from cloud to local.


```python
import deeplake

username = "davitbun"  # your username on app.activeloop.ai
source = f"hub://{username}/langchain_test"  # could be local, s3, gcs, etc.
destination = f"hub://{username}/langchain_test_copy"  # could be local, s3, gcs, etc.

deeplake.deepcopy(src=source, dest=destination, overwrite=True)
```

    Copying dataset: 100%|██████████| 56/56 [00:38<00:00
    

    This dataset can be visualized in Jupyter Notebook by ds.visualize() or at https://app.activeloop.ai/davitbun/langchain_test_copy
    Your Deep Lake dataset has been successfully created!
    The dataset is private so make sure you are logged in!
    




    Dataset(path='hub://davitbun/langchain_test_copy', tensors=['embedding', 'ids', 'metadata', 'text'])




```python
db = DeepLake(dataset_path=destination, embedding_function=embeddings)
db.add_documents(docs)
```

     

    This dataset can be visualized in Jupyter Notebook by ds.visualize() or at https://app.activeloop.ai/davitbun/langchain_test_copy
    
    

    /

    hub://davitbun/langchain_test_copy loaded successfully.
    
    

    Deep Lake Dataset in hub://davitbun/langchain_test_copy already exists, loading from the storage
    

    Dataset(path='hub://davitbun/langchain_test_copy', tensors=['embedding', 'ids', 'metadata', 'text'])
    
      tensor     htype     shape     dtype  compression
      -------   -------   -------   -------  ------- 
     embedding  generic  (4, 1536)  float32   None   
        ids      text     (4, 1)      str     None   
     metadata    json     (4, 1)      str     None   
       text      text     (4, 1)      str     None   
    

    Evaluating ingest: 100%|██████████| 1/1 [00:31<00:00
    -

    Dataset(path='hub://davitbun/langchain_test_copy', tensors=['embedding', 'ids', 'metadata', 'text'])
    
      tensor     htype     shape     dtype  compression
      -------   -------   -------   -------  ------- 
     embedding  generic  (8, 1536)  float32   None   
        ids      text     (8, 1)      str     None   
     metadata    json     (8, 1)      str     None   
       text      text     (8, 1)      str     None   
    

     




    ['ad42f3fe-e188-11ed-b66d-41c5f7b85421',
     'ad42f3ff-e188-11ed-b66d-41c5f7b85421',
     'ad42f400-e188-11ed-b66d-41c5f7b85421',
     'ad42f401-e188-11ed-b66d-41c5f7b85421']


