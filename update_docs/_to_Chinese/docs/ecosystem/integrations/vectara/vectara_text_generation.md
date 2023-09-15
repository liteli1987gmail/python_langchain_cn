# Vectara文本生成

本笔记本基于[text generation](https://github.com/hwchase17/langchain/blob/master/docs/modules/chains/index_examples/vector_db_text_generation.ipynb)笔记本并适应了Vectara。

## 准备数据

首先，我们准备数据。为了这个例子，我们从Github获取由markdown文件组成的文档站点并将其拆分成足够小的文档。

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

    Cloning into '...'
    

## 设置向量数据库

现在我们将文档内容分块后，让我们将所有这些信息放入向量索引以便于检索。

```python
import os

search_index = Vectara.from_texts(source_chunks, embedding=None)
```

## 设置具有自定义提示的LLM链

接下来，让我们设置一个简单的LLM链，但为其提供一个用于博客文章生成的自定义提示。请注意，自定义提示是带有参数的，并接受两个输入: `context`，它将是从向量搜索中提取的文档，以及`topic`，由用户提供。

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

最后，我们编写一个函数将我们的输入应用到链中。该函数接受一个输入参数`topic`。我们找到与该`topic`对应的向量索引中的文档，并将它们用作我们简单的LLM链中的附加上下文。

```python
def generate_blog_post(topic):
    docs = search_index.similarity_search(topic, k=4)
    inputs = [{"context": doc.page_content, "topic": topic} for doc in docs]
    print(chain.apply(inputs))
```

```python
generate_blog_post("environment variables")
```

    [{'text': '\n\n环境变量是在应用程序中管理配置设置的强大工具。它们允许您从代码的任何位置存储和访问值，使得保持代码库的组织和可维护性更容易。\n\n但是，有时您可能想要专门为单个命令使用环境变量。这就是shell变量的用途。shell变量类似于环境变量，但它们不会导出到生成的命令中。它们使用以下语法定义:\n\n```sh\nVAR_NAME=value\n```\n\n例如，如果您想在命令中使用shell变量而不是环境变量，您可以这样做:\n\n```sh\nVAR=hello && echo $VAR && deno eval "console.log(\'Deno: \' + Deno.env.get(\'VAR\'))"\n```\n\n这将输出以下内容:\n\n```\nhello\nDeno: undefined\n```\n\n当您想要重复使用一个值，但不希望它在任何生成的进程中可用时，shell变量可能很有用。\n\n使用环境变量的另一种方法是通过管道。管道提供了一种将'}, {'text': '\n\n环境变量是在应用程序中存储和访问敏感信息的好方法。它们也用于配置应用程序和管理不同的环境。在Deno中，有两种使用环境变量的方法: 内置的`Deno.env`和`.env`文件。\n\n`Deno.env`是Deno运行时的内置功能，允许您设置和获取环境变量。它具有您可以使用的getter和setter方法来访问和设置环境变量。例如，您可以这样设置`FIREBASE_API_KEY`和`FIREBASE_AUTH_DOMAIN`环境变量:\n\n```ts\nDeno.env.set("FIREBASE_API_KEY", "examplekey123");\nDeno.env.set("FIREBASE_AUTH_DOMAIN", "firebasedomain.com");\n\nconsole.log(Deno.env.get("FIREBASE_API_KEY")); // examplekey123\nconsole.log(Deno.env.get("FIREBASE_AUTH_DOMAIN")); // firebasedomain'}, {'text': '\n\n环境变量是在应用程序中管理配置和设置的强大工具。它们允许您存储和访问可在代码中使用的值，并且可以在不修改代码的情况下设置和更改它们。\n\n在Deno中，可以使用`export`命令来定义环境变量。例如，要将名为`VAR_NAME`的变量设置为值`value`，您可以使用以下命令:\n\n```sh\nexport VAR_NAME=value\n```\n\n然后，您可以使用`Deno.env.get()`方法在您的代码中访问环境变量的值。例如，如果您想要记录`VAR_NAME`变量的值，您可以使用以下代码:\n\n```js\nconsole.log(Deno.env.get('VAR_NAME'));\n```\n\n您还可以为单个命令设置环境变量。为此，您可以在命令之前列出环境变量，如下所示:\n\n```\nVAR=hello VAR2=bye deno run main.ts\n```\n\n这将设置环境变量`VAR`和`V'}, {'text': '\n\n环境变量是在应用程序中管理设置和配置的强大工具。它们可用于存储诸如用户首选项、应用程序设置甚至密码等信息。在本博客文章中，我们将讨论如何使用哈希标签（shebang）使Deno脚本可执行。\n\n哈希标签是放在脚本开头的一行代码。它告诉系统在运行脚本时使用哪个解释器。在Deno的情况下，哈希标签应为`#!/usr/bin/env -S deno run --allow-env`。这告诉系统使用Deno解释器，并允许脚本访问环境变量。\n\n一旦放置了哈希标签，您可能需要给脚本赋予执行权限。在Linux上，可以使用命令`sudo chmod +x hashbang.ts`来执行此操作。之后，您可以通过像执行任何其他命令一样调用脚本: `./hashbang.ts`。\n\n在示例程序中，我们授予上下文权限以访问环境变量并打印Deno安装路径。这是通过使用`Deno.env.get()`函数完成的，该函数返回指定环境变量的值。"}]}