# Wikipedia

>[Wikipedia](https://wikipedia.org/) is a multilingual free online encyclopedia written and maintained by a community of volunteers, known as Wikipedians, through open collaboration and using a wiki-based editing system called MediaWiki. `Wikipedia` is the largest and most-read reference work in history.

This notebook shows how to retrieve wiki pages from `wikipedia.org` into the Document format that is used downstream.

## Installation

First, you need to install `wikipedia` python package.


```python
#!pip install wikipedia
```

`WikipediaRetriever` has these arguments:
- optional `lang`: default="en". Use it to search in a specific language part of Wikipedia
- optional `load_max_docs`: default=100. Use it to limit number of downloaded documents. It takes time to download all 100 documents, so use a small number for experiments. There is a hard limit of 300 for now.
- optional `load_all_available_meta`: default=False. By default only the most important fields downloaded: `Published` (date when document was published/last updated), `title`, `Summary`. If True, other fields also downloaded.

`get_relevant_documents()` has one argument, `query`: free text which used to find documents in Wikipedia

## Examples

### Running retriever


```python
from langchain.retrievers import WikipediaRetriever
```


```python
retriever = WikipediaRetriever()
```


```python
docs = retriever.get_relevant_documents(query="HUNTER X HUNTER")
```


```python
docs[0].metadata  # meta-information of the Document
```




    {'title': 'Hunter × Hunter',
     'summary': 'Hunter × Hunter (stylized as HUNTER×HUNTER and pronounced "hunter hunter") is a Japanese manga series written and illustrated by Yoshihiro Togashi. It has been serialized in Shueisha\'s shōnen manga magazine Weekly Shōnen Jump since March 1998, although the manga has frequently gone on extended hiatuses since 2006. Its chapters have been collected in 37 tankōbon volumes as of November 2022. The story focuses on a young boy named Gon Freecss who discovers that his father, who left him at a young age, is actually a world-renowned Hunter, a licensed professional who specializes in fantastical pursuits such as locating rare or unidentified animal species, treasure hunting, surveying unexplored enclaves, or hunting down lawless individuals. Gon departs on a journey to become a Hunter and eventually find his father. Along the way, Gon meets various other Hunters and encounters the paranormal.\nHunter × Hunter was adapted into a 62-episode anime television series produced by Nippon Animation and directed by Kazuhiro Furuhashi, which ran on Fuji Television from October 1999 to March 2001. Three separate original video animations (OVAs) totaling 30 episodes were subsequently produced by Nippon Animation and released in Japan from 2002 to 2004. A second anime television series by Madhouse aired on Nippon Television from October 2011 to September 2014, totaling 148 episodes, with two animated theatrical films released in 2013. There are also numerous audio albums, video games, musicals, and other media based on Hunter × Hunter.\nThe manga has been translated into English and released in North America by Viz Media since April 2005. Both television series have been also licensed by Viz Media, with the first series having aired on the Funimation Channel in 2009 and the second series broadcast on Adult Swim\'s Toonami programming block from April 2016 to June 2019.\nHunter × Hunter has been a huge critical and financial success and has become one of the best-selling manga series of all time, having over 84 million copies in circulation by July 2022.\n\n'}




```python
docs[0].page_content[:400]  # a content of the Document
```




    'Hunter × Hunter (stylized as HUNTER×HUNTER and pronounced "hunter hunter") is a Japanese manga series written and illustrated by Yoshihiro Togashi. It has been serialized in Shueisha\'s shōnen manga magazine Weekly Shōnen Jump since March 1998, although the manga has frequently gone on extended hiatuses since 2006. Its chapters have been collected in 37 tankōbon volumes as of November 2022. The sto'



### Question Answering on facts


```python
# get a token: https://platform.openai.com/account/api-keys

from getpass import getpass

OPENAI_API_KEY = getpass()
```

     ········
    


```python
import os

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
```


```python
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain

model = ChatOpenAI(model_name="gpt-3.5-turbo")  # switch to 'gpt-4'
qa = ConversationalRetrievalChain.from_llm(model, retriever=retriever)
```


```python
questions = [
    "What is Apify?",
    "When the Monument to the Martyrs of the 1830 Revolution was created?",
    "What is the Abhayagiri Vihāra?",
    # "How big is Wikipédia en français?",
]
chat_history = []

for question in questions:
    result = qa({"question": question, "chat_history": chat_history})
    chat_history.append((question, result["answer"]))
    print(f"-> **Question**: {question} \n")
    print(f"**Answer**: {result['answer']} \n")
```

    -> **Question**: What is Apify? 
    
    **Answer**: Apify is a platform that allows you to easily automate web scraping, data extraction and web automation. It provides a cloud-based infrastructure for running web crawlers and other automation tasks, as well as a web-based tool for building and managing your crawlers. Additionally, Apify offers a marketplace for buying and selling pre-built crawlers and related services. 
    
    -> **Question**: When the Monument to the Martyrs of the 1830 Revolution was created? 
    
    **Answer**: Apify is a web scraping and automation platform that enables you to extract data from websites, turn unstructured data into structured data, and automate repetitive tasks. It provides a user-friendly interface for creating web scraping scripts without any coding knowledge. Apify can be used for various web scraping tasks such as data extraction, web monitoring, content aggregation, and much more. Additionally, it offers various features such as proxy support, scheduling, and integration with other tools to make web scraping and automation tasks easier and more efficient. 
    
    -> **Question**: What is the Abhayagiri Vihāra? 
    
    **Answer**: Abhayagiri Vihāra was a major monastery site of Theravada Buddhism that was located in Anuradhapura, Sri Lanka. It was founded in the 2nd century BCE and is considered to be one of the most important monastic complexes in Sri Lanka. 
    
    
