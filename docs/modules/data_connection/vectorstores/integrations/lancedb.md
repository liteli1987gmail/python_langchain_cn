# LanceDB

>[LanceDB](https://lancedb.com/) is an open-source database for vector-search built with persistent storage, which greatly simplifies retrevial, filtering and management of embeddings. Fully open source.

This notebook shows how to use functionality related to the `LanceDB` vector database based on the Lance data format.


```python
!pip install lancedb
```

We want to use OpenAIEmbeddings so we have to get the OpenAI API Key. 


```python
import os
import getpass

os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:")
```

    OpenAI API Key: ········
    


```python
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import LanceDB
```


```python
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter

loader = TextLoader("../../../state_of_the_union.txt")
documents = loader.load()

documents = CharacterTextSplitter().split_documents(documents)

embeddings = OpenAIEmbeddings()
```


```python
import lancedb

db = lancedb.connect("/tmp/lancedb")
table = db.create_table(
    "my_table",
    data=[
        {
            "vector": embeddings.embed_query("Hello World"),
            "text": "Hello World",
            "id": "1",
        }
    ],
    mode="overwrite",
)

docsearch = LanceDB.from_documents(documents, embeddings, connection=table)

query = "What did the president say about Ketanji Brown Jackson"
docs = docsearch.similarity_search(query)
```


```python
print(docs[0].page_content)
```

    They were responding to a 9-1-1 call when a man shot and killed them with a stolen gun. 
    
    Officer Mora was 27 years old. 
    
    Officer Rivera was 22. 
    
    Both Dominican Americans who’d grown up on the same streets they later chose to patrol as police officers. 
    
    I spoke with their families and told them that we are forever in debt for their sacrifice, and we will carry on their mission to restore the trust and safety every community deserves. 
    
    I’ve worked on these issues a long time. 
    
    I know what works: Investing in crime preventionand community police officers who’ll walk the beat, who’ll know the neighborhood, and who can restore trust and safety. 
    
    So let’s not abandon our streets. Or choose between safety and equal justice. 
    
    Let’s come together to protect our communities, restore trust, and hold law enforcement accountable. 
    
    That’s why the Justice Department required body cameras, banned chokeholds, and restricted no-knock warrants for its officers. 
    
    That’s why the American Rescue Plan provided $350 Billion that cities, states, and counties can use to hire more police and invest in proven strategies like community violence interruption—trusted messengers breaking the cycle of violence and trauma and giving young people hope.  
    
    We should all agree: The answer is not to Defund the police. The answer is to FUND the police with the resources and training they need to protect our communities. 
    
    I ask Democrats and Republicans alike: Pass my budget and keep our neighborhoods safe.  
    
    And I will keep doing everything in my power to crack down on gun trafficking and ghost guns you can buy online and make at home—they have no serial numbers and can’t be traced. 
    
    And I ask Congress to pass proven measures to reduce gun violence. Pass universal background checks. Why should anyone on a terrorist list be able to purchase a weapon? 
    
    Ban assault weapons and high-capacity magazines. 
    
    Repeal the liability shield that makes gun manufacturers the only industry in America that can’t be sued. 
    
    These laws don’t infringe on the Second Amendment. They save lives. 
    
    The most fundamental right in America is the right to vote – and to have it counted. And it’s under assault. 
    
    In state after state, new laws have been passed, not only to suppress the vote, but to subvert entire elections. 
    
    We cannot let this happen. 
    
    Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections. 
    
    Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. 
    
    One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. 
    
    And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence. 
    
    A former top litigator in private practice. A former federal public defender. And from a family of public school educators and police officers. A consensus builder. Since she’s been nominated, she’s received a broad range of support—from the Fraternal Order of Police to former judges appointed by Democrats and Republicans. 
    
    And if we are to advance liberty and justice, we need to secure the Border and fix the immigration system. 
    
    We can do both. At our border, we’ve installed new technology like cutting-edge scanners to better detect drug smuggling.  
    
    We’ve set up joint patrols with Mexico and Guatemala to catch more human traffickers.  
    
    We’re putting in place dedicated immigration judges so families fleeing persecution and violence can have their cases heard faster.
    


```python

```
