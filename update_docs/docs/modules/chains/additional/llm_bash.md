# Bash chain
This notebook showcases using LLMs and a bash process to perform simple filesystem commands.


```python
from langchain.chains import LLMBashChain
from langchain.llms import OpenAI

llm = OpenAI(temperature=0)

text = "Please write a bash script that prints 'Hello World' to the console."

bash_chain = LLMBashChain.from_llm(llm, verbose=True)

bash_chain.run(text)
```

    
    
    [1m> Entering new LLMBashChain chain...[0m
    Please write a bash script that prints 'Hello World' to the console.[32;1m[1;3m
    
    ```bash
    echo "Hello World"
    ```[0m
    Code: [33;1m[1;3m['echo "Hello World"'][0m
    Answer: [33;1m[1;3mHello World
    [0m
    [1m> Finished chain.[0m
    




    'Hello World\n'



## Customize Prompt
You can also customize the prompt that is used. Here is an example prompting to avoid using the 'echo' utility


```python
from langchain.prompts.prompt import PromptTemplate
from langchain.chains.llm_bash.prompt import BashOutputParser

_PROMPT_TEMPLATE = """If someone asks you to perform a task, your job is to come up with a series of bash commands that will perform the task. There is no need to put "#!/bin/bash" in your answer. Make sure to reason step by step, using this format:
Question: "copy the files in the directory named 'target' into a new directory at the same level as target called 'myNewDirectory'"
I need to take the following actions:
- List all files in the directory
- Create a new directory
- Copy the files from the first directory into the second directory
```bash
ls
mkdir myNewDirectory
cp -r target/* myNewDirectory
```

Do not use 'echo' when writing the script.

That is the format. Begin!
Question: {question}"""

PROMPT = PromptTemplate(
    input_variables=["question"],
    template=_PROMPT_TEMPLATE,
    output_parser=BashOutputParser(),
)
```


```python
bash_chain = LLMBashChain.from_llm(llm, prompt=PROMPT, verbose=True)

text = "Please write a bash script that prints 'Hello World' to the console."

bash_chain.run(text)
```

    
    
    [1m> Entering new LLMBashChain chain...[0m
    Please write a bash script that prints 'Hello World' to the console.[32;1m[1;3m
    
    ```bash
    printf "Hello World\n"
    ```[0m
    Code: [33;1m[1;3m['printf "Hello World\\n"'][0m
    Answer: [33;1m[1;3mHello World
    [0m
    [1m> Finished chain.[0m
    




    'Hello World\n'



## Persistent Terminal

By default, the chain will run in a separate subprocess each time it is called. This behavior can be changed by instantiating with a persistent bash process.


```python
from langchain.utilities.bash import BashProcess


persistent_process = BashProcess(persistent=True)
bash_chain = LLMBashChain.from_llm(llm, bash_process=persistent_process, verbose=True)

text = "List the current directory then move up a level."

bash_chain.run(text)
```

    
    
    [1m> Entering new LLMBashChain chain...[0m
    List the current directory then move up a level.[32;1m[1;3m
    
    ```bash
    ls
    cd ..
    ```[0m
    Code: [33;1m[1;3m['ls', 'cd ..'][0m
    Answer: [33;1m[1;3mapi.html			llm_summarization_checker.html
    constitutional_chain.html	moderation.html
    llm_bash.html			openai_openapi.yaml
    llm_checker.html		openapi.html
    llm_math.html			pal.html
    llm_requests.html		sqlite.html[0m
    [1m> Finished chain.[0m
    




    'api.html\t\t\tllm_summarization_checker.html\r\nconstitutional_chain.html\tmoderation.html\r\nllm_bash.html\t\t\topenai_openapi.yaml\r\nllm_checker.html\t\topenapi.html\r\nllm_math.html\t\t\tpal.html\r\nllm_requests.html\t\tsqlite.html'




```python
# Run the same command again and see that the state is maintained between calls
bash_chain.run(text)
```

    
    
    [1m> Entering new LLMBashChain chain...[0m
    List the current directory then move up a level.[32;1m[1;3m
    
    ```bash
    ls
    cd ..
    ```[0m
    Code: [33;1m[1;3m['ls', 'cd ..'][0m
    Answer: [33;1m[1;3mexamples		getting_started.html	index_examples
    generic			how_to_guides.rst[0m
    [1m> Finished chain.[0m
    




    'examples\t\tgetting_started.html\tindex_examples\r\ngeneric\t\t\thow_to_guides.rst'




```python

```
