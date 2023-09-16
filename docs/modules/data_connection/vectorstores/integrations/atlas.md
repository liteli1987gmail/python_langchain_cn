# Atlas


>[Atlas](https://docs.nomic.ai/index.html) is a platform for interacting with both small and internet scale unstructured datasets by `Nomic`. 

This notebook shows you how to use functionality related to the `AtlasDB` vectorstore.


```python
!pip install spacy
```


```python
!python3 -m spacy download en_core_web_sm
```


```python
!pip install nomic
```


```python
import time
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import SpacyTextSplitter
from langchain.vectorstores import AtlasDB
from langchain.document_loaders import TextLoader
```


```python
ATLAS_TEST_API_KEY = "7xDPkYXSYDc1_ErdTPIcoAR9RNd8YDlkS3nVNXcVoIMZ6"
```


```python
loader = TextLoader("../../../state_of_the_union.txt")
documents = loader.load()
text_splitter = SpacyTextSplitter(separator="|")
texts = []
for doc in text_splitter.split_documents(documents):
    texts.extend(doc.page_content.split("|"))

texts = [e.strip() for e in texts]
```


```python
db = AtlasDB.from_texts(
    texts=texts,
    name="test_index_" + str(time.time()),  # unique name for your vector store
    description="test_index",  # a description for your vector store
    api_key=ATLAS_TEST_API_KEY,
    index_kwargs={"build_topic_model": True},
)
```


```python
db.project.wait_for_project_lock()
```


```python
db.project
```



```

            <strong><a href="https://atlas.nomic.ai/dashboard/project/ee2354a3-7f9a-4c6b-af43-b0cda09d7198">test_index_1677255228.136989</strong></a>
            <br>
            A description for your project 508 datums inserted.
            <br>
            1 index built.
            <br><strong>Projections</strong>
<ul>
<li>test_index_1677255228.136989_index. Status Completed. <a target="_blank" href="https://atlas.nomic.ai/map/ee2354a3-7f9a-4c6b-af43-b0cda09d7198/db996d77-8981-48a0-897a-ff2c22bbf541">view online</a></li></ul><hr><script>
            destroy = function() {
                document.getElementById("iframedb996d77-8981-48a0-897a-ff2c22bbf541").remove()
            }
        </script>

        <h4>Projection ID: db996d77-8981-48a0-897a-ff2c22bbf541</h4>
        <div class="actions">
            <div id="hide" class="action" onclick="destroy()">Hide embedded project</div>
            <div class="action" id="out">
                <a href="https://atlas.nomic.ai/map/ee2354a3-7f9a-4c6b-af43-b0cda09d7198/db996d77-8981-48a0-897a-ff2c22bbf541" target="_blank">Explore on atlas.nomic.ai</a>
            </div>
        </div>

        <iframe class="iframe" id="iframedb996d77-8981-48a0-897a-ff2c22bbf541" allow="clipboard-read; clipboard-write" src="https://atlas.nomic.ai/map/ee2354a3-7f9a-4c6b-af43-b0cda09d7198/db996d77-8981-48a0-897a-ff2c22bbf541">
        </iframe>

        <style>
            .iframe {
                /* vh can be **very** large in vscode html. */
                height: min(75vh, 66vw);
                width: 100%;
            }
        </style>

        <style>
            .actions {
              display: block;
            }
            .action {
              min-height: 18px;
              margin: 5px;
              transition: all 500ms ease-in-out;
            }
            .action:hover {
              cursor: pointer;
            }
            #hide:hover::after {
                content: " X";
            }
            #out:hover::after {
                content: "";
            }
        </style>
```


