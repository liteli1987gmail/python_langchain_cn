# Loading documents from a YouTube url

Building chat or QA applications on YouTube videos is a topic of high interest.

Below we show how to easily go from a YouTube url to text to chat!

We wil use the `OpenAIWhisperParser`, which will use the OpenAI Whisper API to transcribe audio to text.

Note: You will need to have an `OPENAI_API_KEY` supplied.


```python
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import OpenAIWhisperParser
from langchain.document_loaders.blob_loaders.youtube_audio import YoutubeAudioLoader
```

We will use `yt_dlp` to download audio for YouTube urls.

We will use `pydub` to split downloaded audio files (such that we adhere to Whisper API's 25MB file size limit).


```python
! pip install yt_dlp
! pip install pydub
```

### YouTube url to text

Use `YoutubeAudioLoader` to fetch / download the audio files.

Then, ues `OpenAIWhisperParser()` to transcribe them to text.

Let's take the first lecture of Andrej Karpathy's YouTube course as an example! 


```python
# Two Karpathy lecture videos
urls = ["https://youtu.be/kCc8FmEb1nY", "https://youtu.be/VMj-3S1tku0"]

# Directory to save audio files
save_dir = "~/Downloads/YouTube"

# Transcribe the videos to text
loader = GenericLoader(YoutubeAudioLoader(urls, save_dir), OpenAIWhisperParser())
docs = loader.load()
```

    [youtube] Extracting URL: https://youtu.be/kCc8FmEb1nY
    [youtube] kCc8FmEb1nY: Downloading webpage
    [youtube] kCc8FmEb1nY: Downloading android player API JSON
    [info] kCc8FmEb1nY: Downloading 1 format(s): 140
    [dashsegments] Total fragments: 11
    [download] Destination: /Users/31treehaus/Desktop/AI/langchain-fork/docs/modules/indexes/document_loaders/examples/Let's build GPT： from scratch, in code, spelled out..m4a
    [download] 100% of  107.73MiB in 00:00:18 at 5.92MiB/s                   
    [FixupM4a] Correcting container of "/Users/31treehaus/Desktop/AI/langchain-fork/docs/modules/indexes/document_loaders/examples/Let's build GPT： from scratch, in code, spelled out..m4a"
    [ExtractAudio] Not converting audio /Users/31treehaus/Desktop/AI/langchain-fork/docs/modules/indexes/document_loaders/examples/Let's build GPT： from scratch, in code, spelled out..m4a; file is already in target format m4a
    [youtube] Extracting URL: https://youtu.be/VMj-3S1tku0
    [youtube] VMj-3S1tku0: Downloading webpage
    [youtube] VMj-3S1tku0: Downloading android player API JSON
    [info] VMj-3S1tku0: Downloading 1 format(s): 140
    [download] /Users/31treehaus/Desktop/AI/langchain-fork/docs/modules/indexes/document_loaders/examples/The spelled-out intro to neural networks and backpropagation： building micrograd.m4a has already been downloaded
    [download] 100% of  134.98MiB
    [ExtractAudio] Not converting audio /Users/31treehaus/Desktop/AI/langchain-fork/docs/modules/indexes/document_loaders/examples/The spelled-out intro to neural networks and backpropagation： building micrograd.m4a; file is already in target format m4a
    


```python
# Returns a list of Documents, which can be easily viewed or parsed
docs[0].page_content[0:500]
```




    "Hello, my name is Andrej and I've been training deep neural networks for a bit more than a decade. And in this lecture I'd like to show you what neural network training looks like under the hood. So in particular we are going to start with a blank Jupyter notebook and by the end of this lecture we will define and train a neural net and you'll get to see everything that goes on under the hood and exactly sort of how that works on an intuitive level. Now specifically what I would like to do is I w"



### Building a chat app from YouTube video

Given `Documents`, we can easily enable chat / question+answering.


```python
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
```


```python
# Combine doc
combined_docs = [doc.page_content for doc in docs]
text = " ".join(combined_docs)
```


```python
# Split them
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=150)
splits = text_splitter.split_text(text)
```


```python
# Build an index
embeddings = OpenAIEmbeddings()
vectordb = FAISS.from_texts(splits, embeddings)
```


```python
# Build a QA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0),
    chain_type="stuff",
    retriever=vectordb.as_retriever(),
)
```


```python
# Ask a question!
query = "Why do we need to zero out the gradient before backprop at each step?"
qa_chain.run(query)
```




    "We need to zero out the gradient before backprop at each step because the backward pass accumulates gradients in the grad attribute of each parameter. If we don't reset the grad to zero before each backward pass, the gradients will accumulate and add up, leading to incorrect updates and slower convergence. By resetting the grad to zero before each backward pass, we ensure that the gradients are calculated correctly and that the optimization process works as intended."




```python
query = "What is the difference between an encoder and decoder?"
qa_chain.run(query)
```




    'In the context of transformers, an encoder is a component that reads in a sequence of input tokens and generates a sequence of hidden representations. On the other hand, a decoder is a component that takes in a sequence of hidden representations and generates a sequence of output tokens. The main difference between the two is that the encoder is used to encode the input sequence into a fixed-length representation, while the decoder is used to decode the fixed-length representation into an output sequence. In machine translation, for example, the encoder reads in the source language sentence and generates a fixed-length representation, which is then used by the decoder to generate the target language sentence.'




```python
query = "For any token, what are x, k, v, and q?"
qa_chain.run(query)
```




    'For any token, x is the input vector that contains the private information of that token, k and q are the key and query vectors respectively, which are produced by forwarding linear modules on x, and v is the vector that is calculated by propagating the same linear module on x again. The key vector represents what the token contains, and the query vector represents what the token is looking for. The vector v is the information that the token will communicate to other tokens if it finds them interesting, and it gets aggregated for the purposes of the self-attention mechanism.'


