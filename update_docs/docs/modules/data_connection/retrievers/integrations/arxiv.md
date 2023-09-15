# Arxiv

>[arXiv](https://arxiv.org/) is an open-access archive for 2 million scholarly articles in the fields of physics, mathematics, computer science, quantitative biology, quantitative finance, statistics, electrical engineering and systems science, and economics.

This notebook shows how to retrieve scientific articles from `Arxiv.org` into the Document format that is used downstream.

## Installation

First, you need to install `arxiv` python package.


```python
#!pip install arxiv
```

`ArxivRetriever` has these arguments:
- optional `load_max_docs`: default=100. Use it to limit number of downloaded documents. It takes time to download all 100 documents, so use a small number for experiments. There is a hard limit of 300 for now.
- optional `load_all_available_meta`: default=False. By default only the most important fields downloaded: `Published` (date when document was published/last updated), `Title`, `Authors`, `Summary`. If True, other fields also downloaded.

`get_relevant_documents()` has one argument, `query`: free text which used to find documents in `Arxiv.org`

## Examples

### Running retriever


```python
from langchain.retrievers import ArxivRetriever
```


```python
retriever = ArxivRetriever(load_max_docs=2)
```


```python
docs = retriever.get_relevant_documents(query="1605.08386")
```


```python
docs[0].metadata  # meta-information of the Document
```




    {'Published': '2016-05-26',
     'Title': 'Heat-bath random walks with Markov bases',
     'Authors': 'Caprice Stanley, Tobias Windisch',
     'Summary': 'Graphs on lattice points are studied whose edges come from a finite set of\nallowed moves of arbitrary length. We show that the diameter of these graphs on\nfibers of a fixed integer matrix can be bounded from above by a constant. We\nthen study the mixing behaviour of heat-bath random walks on these graphs. We\nalso state explicit conditions on the set of moves so that the heat-bath random\nwalk, a generalization of the Glauber dynamics, is an expander in fixed\ndimension.'}




```python
docs[0].page_content[:400]  # a content of the Document
```




    'arXiv:1605.08386v1  [math.CO]  26 May 2016\nHEAT-BATH RANDOM WALKS WITH MARKOV BASES\nCAPRICE STANLEY AND TOBIAS WINDISCH\nAbstract. Graphs on lattice points are studied whose edges come from a ﬁnite set of\nallowed moves of arbitrary length. We show that the diameter of these graphs on ﬁbers of a\nﬁxed integer matrix can be bounded from above by a constant. We then study the mixing\nbehaviour of heat-b'



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
    "What are Heat-bath random walks with Markov base?",
    "What is the ImageBind model?",
    "How does Compositional Reasoning with Large Language Models works?",
]
chat_history = []

for question in questions:
    result = qa({"question": question, "chat_history": chat_history})
    chat_history.append((question, result["answer"]))
    print(f"-> **Question**: {question} \n")
    print(f"**Answer**: {result['answer']} \n")
```

    -> **Question**: What are Heat-bath random walks with Markov base? 
    
    **Answer**: I'm not sure, as I don't have enough context to provide a definitive answer. The term "Heat-bath random walks with Markov base" is not mentioned in the given text. Could you provide more information or context about where you encountered this term? 
    
    -> **Question**: What is the ImageBind model? 
    
    **Answer**: ImageBind is an approach developed by Facebook AI Research to learn a joint embedding across six different modalities, including images, text, audio, depth, thermal, and IMU data. The approach uses the binding property of images to align each modality's embedding to image embeddings and achieve an emergent alignment across all modalities. This enables novel multimodal capabilities, including cross-modal retrieval, embedding-space arithmetic, and audio-to-image generation, among others. The approach sets a new state-of-the-art on emergent zero-shot recognition tasks across modalities, outperforming specialist supervised models. Additionally, it shows strong few-shot recognition results and serves as a new way to evaluate vision models for visual and non-visual tasks. 
    
    -> **Question**: How does Compositional Reasoning with Large Language Models works? 
    
    **Answer**: Compositional reasoning with large language models refers to the ability of these models to correctly identify and represent complex concepts by breaking them down into smaller, more basic parts and combining them in a structured way. This involves understanding the syntax and semantics of language and using that understanding to build up more complex meanings from simpler ones. 
    
    In the context of the paper "Does CLIP Bind Concepts? Probing Compositionality in Large Image Models", the authors focus specifically on the ability of a large pretrained vision and language model (CLIP) to encode compositional concepts and to bind variables in a structure-sensitive way. They examine CLIP's ability to compose concepts in a single-object setting, as well as in situations where concept binding is needed. 
    
    The authors situate their work within the tradition of research on compositional distributional semantics models (CDSMs), which seek to bridge the gap between distributional models and formal semantics by building architectures which operate over vectors yet still obey traditional theories of linguistic composition. They compare the performance of CLIP with several architectures from research on CDSMs to evaluate its ability to encode and reason about compositional concepts. 
    
    


```python
questions = [
    "What are Heat-bath random walks with Markov base? Include references to answer.",
]
chat_history = []

for question in questions:
    result = qa({"question": question, "chat_history": chat_history})
    chat_history.append((question, result["answer"]))
    print(f"-> **Question**: {question} \n")
    print(f"**Answer**: {result['answer']} \n")
```

    -> **Question**: What are Heat-bath random walks with Markov base? Include references to answer. 
    
    **Answer**: Heat-bath random walks with Markov base (HB-MB) is a class of stochastic processes that have been studied in the field of statistical mechanics and condensed matter physics. In these processes, a particle moves in a lattice by making a transition to a neighboring site, which is chosen according to a probability distribution that depends on the energy of the particle and the energy of its surroundings.
    
    The HB-MB process was introduced by Bortz, Kalos, and Lebowitz in 1975 as a way to simulate the dynamics of interacting particles in a lattice at thermal equilibrium. The method has been used to study a variety of physical phenomena, including phase transitions, critical behavior, and transport properties.
    
    References:
    
    Bortz, A. B., Kalos, M. H., & Lebowitz, J. L. (1975). A new algorithm for Monte Carlo simulation of Ising spin systems. Journal of Computational Physics, 17(1), 10-18.
    
    Binder, K., & Heermann, D. W. (2010). Monte Carlo simulation in statistical physics: an introduction. Springer Science & Business Media. 
    
    


```python

```
