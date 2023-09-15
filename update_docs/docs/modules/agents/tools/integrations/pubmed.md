# PubMed Tool

This notebook goes over how to use PubMed as a tool

PubMed® comprises more than 35 million citations for biomedical literature from MEDLINE, life science journals, and online books. Citations may include links to full text content from PubMed Central and publisher web sites.


```python
from langchain.tools import PubmedQueryRun
```


```python
tool = PubmedQueryRun()
```


```python
tool.run("chatgpt")
```




    'Published: <Year>2023</Year><Month>May</Month><Day>31</Day>\nTitle: Dermatology in the wake of an AI revolution: who gets a say?\nSummary: \n\nPublished: <Year>2023</Year><Month>May</Month><Day>30</Day>\nTitle: What is ChatGPT and what do we do with it? Implications of the age of AI for nursing and midwifery practice and education: An editorial.\nSummary: \n\nPublished: <Year>2023</Year><Month>Jun</Month><Day>02</Day>\nTitle: The Impact of ChatGPT on the Nursing Profession: Revolutionizing Patient Care and Education.\nSummary: The nursing field has undergone notable changes over time and is projected to undergo further modifications in the future, owing to the advent of sophisticated technologies and growing healthcare needs. The advent of ChatGPT, an AI-powered language model, is expected to exert a significant influence on the nursing profession, specifically in the domains of patient care and instruction. The present article delves into the ramifications of ChatGPT within the nursing domain and accentuates its capacity and constraints to transform the discipline.'




```python

```
