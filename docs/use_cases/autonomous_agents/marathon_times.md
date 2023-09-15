## AutoGPT example finding Winning Marathon Times

* Implementation of https://github.com/Significant-Gravitas/Auto-GPT 
* With LangChain primitives (LLMs, PromptTemplates, VectorStores, Embeddings, Tools)


```python
# !pip install bs4
# !pip install nest_asyncio
```


```python
# General
import os
import pandas as pd
from langchain.experimental.autonomous_agents.autogpt.agent import AutoGPT
from langchain.chat_models import ChatOpenAI

from langchain.agents.agent_toolkits.pandas.base import create_pandas_dataframe_agent
from langchain.docstore.document import Document
import asyncio
import nest_asyncio


# Needed synce jupyter runs an async eventloop
nest_asyncio.apply()
```


```python
llm = ChatOpenAI(model_name="gpt-4", temperature=1.0)
```

### Set up tools

* We'll set up an AutoGPT with a `search` tool, and `write-file` tool, and a `read-file` tool, a web browsing tool, and a tool to interact with a CSV file via a python REPL

Define any other `tools` you want to use below:


```python
# Tools
import os
from contextlib import contextmanager
from typing import Optional
from langchain.agents import tool
from langchain.tools.file_management.read import ReadFileTool
from langchain.tools.file_management.write import WriteFileTool

ROOT_DIR = "./data/"


@contextmanager
def pushd(new_dir):
    """Context manager for changing the current working directory."""
    prev_dir = os.getcwd()
    os.chdir(new_dir)
    try:
        yield
    finally:
        os.chdir(prev_dir)


@tool
def process_csv(
    csv_file_path: str, instructions: str, output_path: Optional[str] = None
) -> str:
    """Process a CSV by with pandas in a limited REPL.\
 Only use this after writing data to disk as a csv file.\
 Any figures must be saved to disk to be viewed by the human.\
 Instructions should be written in natural language, not code. Assume the dataframe is already loaded."""
    with pushd(ROOT_DIR):
        try:
            df = pd.read_csv(csv_file_path)
        except Exception as e:
            return f"Error: {e}"
        agent = create_pandas_dataframe_agent(llm, df, max_iterations=30, verbose=True)
        if output_path is not None:
            instructions += f" Save output to disk at {output_path}"
        try:
            result = agent.run(instructions)
            return result
        except Exception as e:
            return f"Error: {e}"
```

**Browse a web page with PlayWright**


```python
# !pip install playwright
# !playwright install
```


```python
async def async_load_playwright(url: str) -> str:
    """Load the specified URLs using Playwright and parse using BeautifulSoup."""
    from bs4 import BeautifulSoup
    from playwright.async_api import async_playwright

    results = ""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        try:
            page = await browser.new_page()
            await page.goto(url)

            page_source = await page.content()
            soup = BeautifulSoup(page_source, "html.parser")

            for script in soup(["script", "style"]):
                script.extract()

            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            results = "\n".join(chunk for chunk in chunks if chunk)
        except Exception as e:
            results = f"Error: {e}"
        await browser.close()
    return results


def run_async(coro):
    event_loop = asyncio.get_event_loop()
    return event_loop.run_until_complete(coro)


@tool
def browse_web_page(url: str) -> str:
    """Verbose way to scrape a whole webpage. Likely to cause issues parsing."""
    return run_async(async_load_playwright(url))
```

**Q&A Over a webpage**

Help the model ask more directed questions of web pages to avoid cluttering its memory


```python
from langchain.tools import BaseTool, DuckDuckGoSearchRun
from langchain.text_splitter import RecursiveCharacterTextSplitter

from pydantic import Field
from langchain.chains.qa_with_sources.loading import (
    load_qa_with_sources_chain,
    BaseCombineDocumentsChain,
)


def _get_text_splitter():
    return RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size=500,
        chunk_overlap=20,
        length_function=len,
    )


class WebpageQATool(BaseTool):
    name = "query_webpage"
    description = (
        "Browse a webpage and retrieve the information relevant to the question."
    )
    text_splitter: RecursiveCharacterTextSplitter = Field(
        default_factory=_get_text_splitter
    )
    qa_chain: BaseCombineDocumentsChain

    def _run(self, url: str, question: str) -> str:
        """Useful for browsing websites and scraping the text information."""
        result = browse_web_page.run(url)
        docs = [Document(page_content=result, metadata={"source": url})]
        web_docs = self.text_splitter.split_documents(docs)
        results = []
        # TODO: Handle this with a MapReduceChain
        for i in range(0, len(web_docs), 4):
            input_docs = web_docs[i : i + 4]
            window_result = self.qa_chain(
                {"input_documents": input_docs, "question": question},
                return_only_outputs=True,
            )
            results.append(f"Response from window {i} - {window_result}")
        results_docs = [
            Document(page_content="\n".join(results), metadata={"source": url})
        ]
        return self.qa_chain(
            {"input_documents": results_docs, "question": question},
            return_only_outputs=True,
        )

    async def _arun(self, url: str, question: str) -> str:
        raise NotImplementedError
```


```python
query_website_tool = WebpageQATool(qa_chain=load_qa_with_sources_chain(llm))
```

### Set up memory

* The memory here is used for the agents intermediate steps


```python
# Memory
import faiss
from langchain.vectorstores import FAISS
from langchain.docstore import InMemoryDocstore
from langchain.embeddings import OpenAIEmbeddings
from langchain.tools.human.tool import HumanInputRun

embeddings_model = OpenAIEmbeddings()
embedding_size = 1536
index = faiss.IndexFlatL2(embedding_size)
vectorstore = FAISS(embeddings_model.embed_query, index, InMemoryDocstore({}), {})
```

### Setup model and AutoGPT

`Model set-up`


```python
# !pip install duckduckgo_search
web_search = DuckDuckGoSearchRun()
```


```python
tools = [
    web_search,
    WriteFileTool(root_dir="./data"),
    ReadFileTool(root_dir="./data"),
    process_csv,
    query_website_tool,
    # HumanInputRun(), # Activate if you want the permit asking for help from the human
]
```


```python
agent = AutoGPT.from_llm_and_tools(
    ai_name="Tom",
    ai_role="Assistant",
    tools=tools,
    llm=llm,
    memory=vectorstore.as_retriever(search_kwargs={"k": 8}),
    # human_in_the_loop=True, # Set to True if you want to add feedback at each step.
)
# agent.chain.verbose = True
```

### AutoGPT for Querying the Web
 
  
I've spent a lot of time over the years crawling data sources and cleaning data. Let's see if AutoGPT can help with this!

Here is the prompt for looking up recent boston marathon times and converting them to tabular form.


```python
agent.run(
    [
        "What were the winning boston marathon times for the past 5 years (ending in 2022)? Generate a table of the year, name, country of origin, and times."
    ]
)
```

    {
        "thoughts": {
            "text": "I need to find the winning Boston Marathon times for the past 5 years. I can use the DuckDuckGo Search command to search for this information.",
            "reasoning": "Using DuckDuckGo Search will help me gather information on the winning times without complications.",
            "plan": "- Use DuckDuckGo Search to find the winning Boston Marathon times\n- Generate a table with the year, name, country of origin, and times\n- Ensure there are no legal complications",
            "criticism": "None",
            "speak": "I will use the DuckDuckGo Search command to find the winning Boston Marathon times for the past 5 years."
        },
        "command": {
            "name": "DuckDuckGo Search",
            "args": {
                "query": "winning Boston Marathon times for the past 5 years ending in 2022"
            }
        }
    }
    {
        "thoughts": {
            "text": "The DuckDuckGo Search command did not provide the specific information I need. I must switch my approach and use query_webpage command to browse a webpage containing the Boston Marathon winning times for the past 5 years.",
            "reasoning": "The query_webpage command may give me more accurate and comprehensive results compared to the search command.",
            "plan": "- Use query_webpage command to find the winning Boston Marathon times\n- Generate a table with the year, name, country of origin, and times\n- Ensure there are no legal complications",
            "criticism": "I may face difficulty in finding the right webpage with the desired information.",
            "speak": "I will use the query_webpage command to find the winning Boston Marathon times for the past 5 years."
        },
        "command": {
            "name": "DuckDuckGo Search",
            "args": {
                "query": "site with winning Boston Marathon times for the past 5 years ending in 2022"
            }
        }
    }
    {
        "thoughts": {
            "text": "I need to use the query_webpage command to find the information about the winning Boston Marathon times for the past 5 years.",
            "reasoning": "The previous DuckDuckGo Search command did not provide specific enough results. The query_webpage command might give more accurate and comprehensive results.",
            "plan": "- Use query_webpage command to find the winning Boston Marathon times\\n- Generate a table with the year, name, country of origin, and times\\n- Ensure there are no legal complications",
            "criticism": "I may face difficulty in finding the right webpage with the desired information.",
            "speak": "I will use the query_webpage command to find the winning Boston Marathon times for the past 5 years."
        },
        "command": {
            "name": "query_webpage",
            "args": {
                "url": "https://en.wikipedia.org/wiki/List_of_winners_of_the_Boston_Marathon",
                "question": "What were the winning Boston Marathon times for the past 5 years ending in 2022?"
            }
        }
    }
    {
        "thoughts": {
            "text": "I have already found the winning Boston Marathon times for the past 5 years. Now, I need to generate a table with the information.",
            "reasoning": "Using the information I already have, I can create a table containing year, name, country of origin, and times.",
            "plan": "- Write the marathon data to a CSV file\n- Process the CSV file to display the table",
            "criticism": "None",
            "speak": "I will generate a table with the year, name, country of origin, and times for the winning Boston Marathon times for the past 5 years."
        },
        "command": {
            "name": "write_file",
            "args": {
                "file_path": "boston_marathon_winners.csv",
                "text": "Year,Name,Country,Time\n2022,Evans Chebet,KEN,2:06:51\n2021,Benson Kipruto,KEN,2:09:51\n2019,Lawrence Cherono,KEN,2:07:57\n2018,Yuki Kawauchi,JPN,2:15:58"
            }
        }
    }
    {
        "thoughts": {
            "text": "I have retrieved the winning Boston Marathon times for the past 5 years. Now, I need to generate a table with the year, name, country of origin, and times.",
            "reasoning": "Creating a table will help organize the data in a clear and accessible format.",
            "plan": "- Write the data to a CSV file\n- Process the CSV file to generate the table\n- Complete the task",
            "criticism": "None",
            "speak": "I will generate a table with the year, name, country of origin, and winning times using the recently retrieved data."
        },
        "command": {
            "name": "write_file",
            "args": {
                "file_path": "winning_boston_marathon_data.csv",
                "text": "Year,Name,Country,Time\n2022,Evans Chebet,KEN,2:06:51\n2021,Benson Kipruto,KEN,2:09:51\n2019,Lawrence Cherono,KEN,2:07:57\n2018,Yuki Kawauchi,JPN,2:15:58\n"
            }
        }
    }
    {
        "thoughts": {
            "text": "I have found the winning Boston Marathon times for the past five years ending in 2022. Next, I need to create a table with the year, name, country of origin, and times.",
            "reasoning": "Generating a table will help organize the information in a structured format.",
            "plan": "- Create a table with the year, name, country of origin, and times\n- Ensure there are no legal complications",
            "criticism": "None",
            "speak": "I will generate a table with the winning Boston Marathon times for the past 5 years ending in 2022."
        },
        "command": {
            "name": "write_file",
            "args": {
                "file_path": "winning_times.csv",
                "text": "Year,Name,Country,Time\n2022,Evans Chebet,Kenya,2:06:51\n2021,Benson Kipruto,Kenya,2:09:51\n2020,Canceled due to COVID-19 pandemic,,\n2019,Lawrence Cherono,Kenya,2:07:57\n2018,Yuki Kawauchi,Japan,2:15:58"
            }
        }
    }
    {
        "thoughts": {
            "text": "I need to process the CSV file to generate the table with the year, name, country of origin, and winning times.",
            "reasoning": "I have already written the data to a file named 'winning_times.csv'. Now, I need to process this CSV file to properly display the data as a table.",
            "plan": "- Use the process_csv command to read the 'winning_times.csv' file and generate the table",
            "criticism": "None",
            "speak": "I will process the 'winning_times.csv' file to display the table with the winning Boston Marathon times for the past 5 years."
        },
        "command": {
            "name": "process_csv",
            "args": {
                "csv_file_path": "winning_times.csv",
                "instructions": "Read the CSV file and display the data as a table"
            }
        }
    }
    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3mThought: The CSV file has already been read and saved into a pandas dataframe called `df`. Hence, I can simply display the data by printing the whole dataframe. Since `df.head()` returns the first 5 rows, I can use that to showcase the contents.
    
    Action: python_repl_ast
    Action Input: print(df.head())[0m   Year                               Name Country     Time
    0  2022                       Evans Chebet   Kenya  2:06:51
    1  2021                     Benson Kipruto   Kenya  2:09:51
    2  2020  Canceled due to COVID-19 pandemic     NaN      NaN
    3  2019                   Lawrence Cherono   Kenya  2:07:57
    4  2018                      Yuki Kawauchi   Japan  2:15:58
    
    Observation: [36;1m[1;3mNone[0m
    Thought:[32;1m[1;3mI used the wrong tool to perform the action. I should have used the given data and not interacted with the Python shell. I can now provide the displayed data as the answer since the information in the printed dataframe would look like a table when typed as text.
    
    Final Answer: 
       Year                               Name Country     Time
    0  2022                       Evans Chebet   Kenya  2:06:51
    1  2021                     Benson Kipruto   Kenya  2:09:51
    2  2020  Canceled due to COVID-19 pandemic     NaN      NaN
    3  2019                   Lawrence Cherono   Kenya  2:07:57
    4  2018                      Yuki Kawauchi   Japan  2:15:58[0m
    
    [1m> Finished chain.[0m
    {
        "thoughts": {
            "text": "I already have the winning Boston Marathon times for the past 5 years saved in the file 'winning_times.csv'. Now, I need to process the CSV and display the table.",
            "reasoning": "I am choosing the process_csv command because I already have the required data saved as a CSV file, and I can use this command to read and display the data as a table.",
            "plan": "- Use the process_csv command to read the 'winning_times.csv' file and generate the table",
            "criticism": "None",
            "speak": "I will process the 'winning_times.csv' file to display the table with the winning Boston Marathon times for the past 5 years."
        },
        "command": {
            "name": "process_csv",
            "args": {
                "csv_file_path": "winning_times.csv",
                "instructions": "Read the CSV file and display the data as a table"
            }
        }
    }
    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3mThought: Since the data is already loaded in a pandas dataframe, I just need to display the top rows of the dataframe.
    Action: python_repl_ast
    Action Input: df.head()[0m
    Observation: [36;1m[1;3m   Year                               Name Country     Time
    0  2022                       Evans Chebet   Kenya  2:06:51
    1  2021                     Benson Kipruto   Kenya  2:09:51
    2  2020  Canceled due to COVID-19 pandemic     NaN      NaN
    3  2019                   Lawrence Cherono   Kenya  2:07:57
    4  2018                      Yuki Kawauchi   Japan  2:15:58[0m
    Thought:[32;1m[1;3mI now know the final answer.
    Final Answer: 
       Year                               Name Country     Time
    0  2022                       Evans Chebet   Kenya  2:06:51
    1  2021                     Benson Kipruto   Kenya  2:09:51
    2  2020  Canceled due to COVID-19 pandemic     NaN      NaN
    3  2019                   Lawrence Cherono   Kenya  2:07:57
    4  2018                      Yuki Kawauchi   Japan  2:15:58[0m
    
    [1m> Finished chain.[0m
    {
        "thoughts": {
            "text": "I have already generated a table with the winning Boston Marathon times for the past 5 years. Now, I can finish the task.",
            "reasoning": "I have completed the required actions and obtained the desired data. The task is complete.",
            "plan": "- Use the finish command",
            "criticism": "None",
            "speak": "I have generated the table with the winning Boston Marathon times for the past 5 years. Task complete."
        },
        "command": {
            "name": "finish",
            "args": {
                "response": "I have generated the table with the winning Boston Marathon times for the past 5 years. Task complete."
            }
        }
    }
    




    'I have generated the table with the winning Boston Marathon times for the past 5 years. Task complete.'




```python

```
