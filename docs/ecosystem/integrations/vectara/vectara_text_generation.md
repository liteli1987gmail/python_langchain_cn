# Vectara文本生成

这个笔记本是基于[text generation](https://github.com/hwchase17/langchain/blob/master/docs/modules/chains/index_examples/vector_db_text_generation.ipynb) 笔记本，并对Vectara进行了适应。

## 准备数据

首先，我们准备数据。对于这个例子，我们从Github获取由markdown文件组成的文档站点，并将它们拆分成足够小的文档。


```python
import os
from langchain.llms import OpenAI
from langchain.docstore.document import Document
import requests
from langchain.vectorstores import Vectara
from langchain.text_splitter import CharacterTextSplitter
from langchain.prompts import PromptTemplate
import pathlib
import subprocess
import tempfile
```


```python
def get_github_docs(repo_owner, repo_name):
    with tempfile.TemporaryDirectory() as d:
        subprocess.check_call(
            f"git clone --depth 1 https://github.com/{repo_owner}/{repo_name}.git .",
            cwd=d,
            shell=True,
        )
        git_sha = (
            subprocess.check_output("git rev-parse HEAD", shell=True, cwd=d)
            .decode("utf-8")
            .strip()
        )
        repo_path = pathlib.Path(d)
        markdown_files = list(repo_path.glob("*/*.md")) + list(
            repo_path.glob("*/*.mdx")
        )
        for markdown_file in markdown_files:
            with open(markdown_file, "r") as f:
                relative_path = markdown_file.relative_to(repo_path)
                github_url = f"https://github.com/{repo_owner}/{repo_name}/blob/{git_sha}/{relative_path}"
                yield Document(page_content=f.read(), metadata={"source": github_url})


sources = get_github_docs("yirenlu92", "deno-manual-forked")

source_chunks = []
splitter = CharacterTextSplitter(separator=" ", chunk_size=1024, chunk_overlap=0)
for source in sources:
    for chunk in splitter.split_text(source.page_content):
        source_chunks.append(chunk)
```

    正在克隆到 '.'...
    

## 设置向量数据库

现在我们将文档内容拆分成块，让我们将所有这些信息放入一个向量索引中，以便轻松检索。


```python
import os

search_index = Vectara.from_texts(source_chunks, embedding=None)
```

## 使用自定义提示设置LLM链

接下来，让我们设置一个简单的LLM链，但为其提供一个自定义提示以生成博客文章。请注意，自定义提示是带参数的，需要两个输入: `context`，将是从向量搜索中获取的文档，以及`topic`，由用户提供。


```python
from langchain.chains import LLMChain

prompt_template = """Use the context below to write a 400 word blog post about the topic below:
    Context: {context}
    Topic: {topic}
    Blog post:"""

PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "topic"])

llm = OpenAI(openai_api_key=os.environ["OPENAI_API_KEY"], temperature=0)

chain = LLMChain(llm=llm, prompt=PROMPT)
```

## 生成文本

最后，我们编写一个函数将我们的输入应用到链条上。该函数接受一个输入参数`topic`。我们找到与该`topic`对应的向量索引中的文档，并将它们用作在我们简单的LLM链中的附加上下文。


```python
def generate_blog_post(topic):
    docs = search_index.similarity_search(topic, k=4)
    inputs = [{"context": doc.page_content, "topic": topic} for doc in docs]
    print(chain.apply(inputs))
```


```python
generate_blog_post("environment variables")
```

    [{'text': '\n\nEnvironment variables are a powerful tool for managing configuration settings in your applications. They allow you to store and access values from anywhere in your code, making it easier to keep your codebase organized and maintainable.\n\nHowever, there are times when you may want to use environment variables specifically for a single command. This is where shell variables come in. Shell variables are similar to environment variables, but they won\'t be exported to spawned commands. They are defined with the following syntax:\n\n```sh\nVAR_NAME=value\n```\n\nFor example, if you wanted to use a shell variable instead of an environment variable in a command, you could do something like this:\n\n```sh\nVAR=hello && echo $VAR && deno eval "console.log(\'Deno: \' + Deno.env.get(\'VAR\'))"\n```\n\nThis would output the following:\n\n```\nhello\nDeno: undefined\n```\n\nShell variables can be useful when you want to re-use a value, but don\'t want it available in any spawned processes.\n\nAnother way to use environment variables is through pipelines. Pipelines provide a way to pipe the'}, {'text': '\n\nEnvironment variables are a great way to store and access sensitive information in your applications. They are also useful for configuring applications and managing different environments. In Deno, there are two ways to use environment variables: the built-in `Deno.env` and the `.env` file.\n\nThe `Deno.env` is a built-in feature of the Deno runtime that allows you to set and get environment variables. It has getter and setter methods that you can use to access and set environment variables. For example, you can set the `FIREBASE_API_KEY` and `FIREBASE_AUTH_DOMAIN` environment variables like this:\n\n```ts\nDeno.env.set("FIREBASE_API_KEY", "examplekey123");\nDeno.env.set("FIREBASE_AUTH_DOMAIN", "firebasedomain.com");\n\nconsole.log(Deno.env.get("FIREBASE_API_KEY")); // examplekey123\nconsole.log(Deno.env.get("FIREBASE_AUTH_DOMAIN")); // firebasedomain'}, {'text': "\n\nEnvironment variables are a powerful tool for managing configuration and settings in your applications. They allow you to store and access values that can be used in your code, and they can be set and changed without having to modify your code.\n\nIn Deno, environment variables are defined using the `export` command. For example, to set a variable called `VAR_NAME` to the value `value`, you would use the following command:\n\n```sh\nexport VAR_NAME=value\n```\n\nYou can then access the value of the environment variable in your code using the `Deno.env.get()` method. For example, if you wanted to log the value of the `VAR_NAME` variable, you could use the following code:\n\n```js\nconsole.log(Deno.env.get('VAR_NAME'));\n```\n\nYou can also set environment variables for a single command. To do this, you can list the environment variables before the command, like so:\n\n```\nVAR=hello VAR2=bye deno run main.ts\n```\n\nThis will set the environment variables `VAR` and `V"}, {'text': "\n\nEnvironment variables are a powerful tool for managing settings and configuration in your applications. They can be used to store information such as user preferences, application settings, and even passwords. In this blog post, we'll discuss how to make Deno scripts executable with a hashbang (shebang).\n\nA hashbang is a line of code that is placed at the beginning of a script. It tells the system which interpreter to use when running the script. In the case of Deno, the hashbang should be `#!/usr/bin/env -S deno run --allow-env`. This tells the system to use the Deno interpreter and to allow the script to access environment variables.\n\nOnce the hashbang is in place, you may need to give the script execution permissions. On Linux, this can be done with the command `sudo chmod +x hashbang.ts`. After that, you can execute the script by calling it like any other command: `./hashbang.ts`.\n\nIn the example program, we give the context permission to access the environment variables and print the Deno installation path. This is done by using the `Deno.env.get()` function, which returns the value of the specified environment"}]
    


```python

```
