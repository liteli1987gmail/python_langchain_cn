# 按标记进行分割

语言模型有一个标记限制。您不应超过标记限制。因此，当您将文本分割成块时，将标记的数量进行计数是一个好主意。有许多分词器可供使用。在计数文本中的标记时，应使用与语言模型中使用的相同的分词器。

## tiktoken

> [tiktoken](https://github.com/openai/tiktoken) 是由 `OpenAI` 创建的高速`BPE`分词器。

我们可以使用它来估计已使用的标记。对于 OpenAI 模型，它可能更准确。

1. 文本的分割方式：通过传入的字符进行分割
2. 分块大小的衡量标准：使用 `tiktoken` 分词器计数


```python
#!pip install tiktoken
```


```python
# This is a long document we can split up.
with open("../../../state_of_the_union.txt") as f:
    state_of_the_union = f.read()
from langchain.text_splitter import CharacterTextSplitter
```


```python
text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=100, chunk_overlap=0
)
texts = text_splitter.split_text(state_of_the_union)
```


```python
print(texts[0])
```

    Madam Speaker, Madam Vice President, our First Lady and Second Gentleman. Members of Congress and the Cabinet. Justices of the Supreme Court. My fellow Americans.  
    
    Last year COVID-19 kept us apart. This year we are finally together again. 
    
    Tonight, we meet as Democrats Republicans and Independents. But most importantly as Americans. 
    
    With a duty to one another to the American people to the Constitution.
    

We can also load a tiktoken splitter directly


```python
from langchain.text_splitter import TokenTextSplitter

text_splitter = TokenTextSplitter(chunk_size=10, chunk_overlap=0)

texts = text_splitter.split_text(state_of_the_union)
print(texts[0])
```

## spaCy

>[spaCy](https://spacy.io/) is an open-source software library for advanced natural language processing, written in the programming languages Python and Cython.

Another alternative to `NLTK` is to use [spaCy tokenizer](https://spacy.io/api/tokenizer).

1. How the text is split: by `spaCy` tokenizer
2. How the chunk size is measured: by number of characters


```python
#!pip install spacy
```


```python
# This is a long document we can split up.
with open("../../../state_of_the_union.txt") as f:
    state_of_the_union = f.read()
```


```python
from langchain.text_splitter import SpacyTextSplitter

text_splitter = SpacyTextSplitter(chunk_size=1000)
```


```python
texts = text_splitter.split_text(state_of_the_union)
print(texts[0])
```

    Madam Speaker, Madam Vice President, our First Lady and Second Gentleman.
    
    Members of Congress and the Cabinet.
    
    Justices of the Supreme Court.
    
    My fellow Americans.  
    
    
    
    Last year COVID-19 kept us apart.
    
    This year we are finally together again. 
    
    
    
    Tonight, we meet as Democrats Republicans and Independents.
    
    But most importantly as Americans. 
    
    
    
    With a duty to one another to the American people to the Constitution. 
    
    
    
    And with an unwavering resolve that freedom will always triumph over tyranny. 
    
    
    
    Six days ago, Russia’s Vladimir Putin sought to shake the foundations of the free world thinking he could make it bend to his menacing ways.
    
    But he badly miscalculated. 
    
    
    
    He thought he could roll into Ukraine and the world would roll over.
    
    Instead he met a wall of strength he never imagined. 
    
    
    
    He met the Ukrainian people. 
    
    
    
    From President Zelenskyy to every Ukrainian, their fearlessness, their courage, their determination, inspires the world.
    

## SentenceTransformers

The `SentenceTransformersTokenTextSplitter` is a specialized text splitter for use with the sentence-transformer models. The default behaviour is to split the text into chunks that fit the token window of the sentence transformer model that you would like to use.


```python
from langchain.text_splitter import SentenceTransformersTokenTextSplitter
```


```python
splitter = SentenceTransformersTokenTextSplitter(chunk_overlap=0)
text = "Lorem "
```


```python
count_start_and_stop_tokens = 2
text_token_count = splitter.count_tokens(text=text) - count_start_and_stop_tokens
print(text_token_count)
```

    2
    


```python
token_multiplier = splitter.maximum_tokens_per_chunk // text_token_count + 1

# `text_to_split` does not fit in a single chunk
text_to_split = text * token_multiplier

print(f"tokens in text to split: {splitter.count_tokens(text=text_to_split)}")
```

    tokens in text to split: 514
    


```python
text_chunks = splitter.split_text(text=text_to_split)

print(text_chunks[1])
```

    lorem
    

## NLTK

>[The Natural Language Toolkit](https://en.wikipedia.org/wiki/Natural_Language_Toolkit), or more commonly [NLTK](https://www.nltk.org/), is a suite of libraries and programs for symbolic and statistical natural language processing (NLP) for English written in the Python programming language.

Rather than just splitting on "\n\n", we can use `NLTK` to split based on [NLTK tokenizers](https://www.nltk.org/api/nltk.tokenize.html).

1. How the text is split: by `NLTK` tokenizer.
2. How the chunk size is measured:by number of characters


```python
# pip install nltk
```


```python
# This is a long document we can split up.
with open("../../../state_of_the_union.txt") as f:
    state_of_the_union = f.read()
```


```python
from langchain.text_splitter import NLTKTextSplitter

text_splitter = NLTKTextSplitter(chunk_size=1000)
```


```python
texts = text_splitter.split_text(state_of_the_union)
print(texts[0])
```

    Madam Speaker, Madam Vice President, our First Lady and Second Gentleman.
    
    Members of Congress and the Cabinet.
    
    Justices of the Supreme Court.
    
    My fellow Americans.
    
    Last year COVID-19 kept us apart.
    
    This year we are finally together again.
    
    Tonight, we meet as Democrats Republicans and Independents.
    
    But most importantly as Americans.
    
    With a duty to one another to the American people to the Constitution.
    
    And with an unwavering resolve that freedom will always triumph over tyranny.
    
    Six days ago, Russia’s Vladimir Putin sought to shake the foundations of the free world thinking he could make it bend to his menacing ways.
    
    But he badly miscalculated.
    
    He thought he could roll into Ukraine and the world would roll over.
    
    Instead he met a wall of strength he never imagined.
    
    He met the Ukrainian people.
    
    From President Zelenskyy to every Ukrainian, their fearlessness, their courage, their determination, inspires the world.
    
    Groups of citizens blocking tanks with their bodies.
    

## Hugging Face tokenizer

>[Hugging Face](https://huggingface.co/docs/tokenizers/index) has many tokenizers.

We use Hugging Face tokenizer, the [GPT2TokenizerFast](https://huggingface.co/Ransaka/gpt2-tokenizer-fast) to count the text length in tokens.

1. How the text is split: by character passed in
2. How the chunk size is measured: by number of tokens calculated by the `Hugging Face` tokenizer



```python
from transformers import GPT2TokenizerFast

tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
```


```python
# This is a long document we can split up.
with open("../../../state_of_the_union.txt") as f:
    state_of_the_union = f.read()
from langchain.text_splitter import CharacterTextSplitter
```


```python
text_splitter = CharacterTextSplitter.from_huggingface_tokenizer(
    tokenizer, chunk_size=100, chunk_overlap=0
)
texts = text_splitter.split_text(state_of_the_union)
```


```python
print(texts[0])
```

    Madam Speaker, Madam Vice President, our First Lady and Second Gentleman. Members of Congress and the Cabinet. Justices of the Supreme Court. My fellow Americans.  
    
    Last year COVID-19 kept us apart. This year we are finally together again. 
    
    Tonight, we meet as Democrats Republicans and Independents. But most importantly as Americans. 
    
    With a duty to one another to the American people to the Constitution.
    


```python

```
