# PubMed

This notebook goes over how to use `PubMed` as a retriever

`PubMed®` comprises more than 35 million citations for biomedical literature from `MEDLINE`, life science journals, and online books. Citations may include links to full text content from `PubMed Central` and publisher web sites.


```python
from langchain.retrievers import PubMedRetriever
```


```python
retriever = PubMedRetriever()
```


```python
retriever.get_relevant_documents("chatgpt")
```




    [Document(page_content='', metadata={'uid': '37268021', 'title': 'Dermatology in the wake of an AI revolution: who gets a say?', 'pub_date': '<Year>2023</Year><Month>May</Month><Day>31</Day>'}),
     Document(page_content='', metadata={'uid': '37267643', 'title': 'What is ChatGPT and what do we do with it? Implications of the age of AI for nursing and midwifery practice and education: An editorial.', 'pub_date': '<Year>2023</Year><Month>May</Month><Day>30</Day>'}),
     Document(page_content='The nursing field has undergone notable changes over time and is projected to undergo further modifications in the future, owing to the advent of sophisticated technologies and growing healthcare needs. The advent of ChatGPT, an AI-powered language model, is expected to exert a significant influence on the nursing profession, specifically in the domains of patient care and instruction. The present article delves into the ramifications of ChatGPT within the nursing domain and accentuates its capacity and constraints to transform the discipline.', metadata={'uid': '37266721', 'title': 'The Impact of ChatGPT on the Nursing Profession: Revolutionizing Patient Care and Education.', 'pub_date': '<Year>2023</Year><Month>Jun</Month><Day>02</Day>'})]


