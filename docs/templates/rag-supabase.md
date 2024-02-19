# rag_supabase

这个模板用于执行带有Supabase的RAG。

[Supabase](https://supabase.com/docs)是一个开源的Firebase替代品。它构建在[PostgreSQL](https://en.wikipedia.org/wiki/PostgreSQL)之上，这是一个免费且开源的关系数据库管理系统（RDBMS），并使用[pgvector](https://github.com/pgvector/pgvector)在您的表中存储嵌入向量。

## 环境设置

将`OPENAI_API_KEY`环境变量设置为访问OpenAI模型。

要获取您的`OPENAI_API_KEY`，请转到您的OpenAI帐户的[API密钥](https://platform.openai.com/account/api-keys)页面并创建一个新的密钥。

要找到您的`SUPABASE_URL`和`SUPABASE_SERVICE_KEY`，请转到您的Supabase项目的[API设置](https://supabase.com/dashboard/project/_/settings/api)页面。

- `SUPABASE_URL`对应项目URL
- `SUPABASE_SERVICE_KEY`对应`service_role` API密钥

```shell
export SUPABASE_URL=
export SUPABASE_SERVICE_KEY=
export OPENAI_API_KEY=
```

## 设置Supabase数据库

如果您还没有设置Supabase数据库，请按照以下步骤进行设置。

1. 前往https://database.new来创建您的Supabase数据库。
2. 在工作室中，跳转到[SQL编辑器](https://supabase.com/dashboard/project/_/sql/new)并运行以下脚本以启用`pgvector`并将您的数据库设置为向量存储：

   ```sql
   -- 启用pgvector扩展以处理嵌入向量
   create extension if not exists vector;

   -- 创建一个表来存储您的文档
   create table
     documents (
       id uuid primary key,
       content text, -- 对应Document.pageContent
       metadata jsonb, -- 对应Document.metadata
       embedding vector (1536) -- 1536适用于OpenAI嵌入向量，根据需要进行更改
     );

   -- 创建一个用于搜索文档的函数
   create function match_documents (
     query_embedding vector (1536),
     filter jsonb default '{}'
   ) returns table (
     id uuid,
     content text,
     metadata jsonb,
     similarity float
   ) language plpgsql as $$
   #variable_conflict use_column
   begin
     return query
     select
       id,
       content,
       metadata,
       1 - (documents.embedding <=> query_embedding) as similarity
     from documents
     where metadata @> filter
     order by documents.embedding <=> query_embedding;
   end;
   $$;
   ```

## 设置环境变量

由于我们使用[`SupabaseVectorStore`](https://python.langchain.com/docs/integrations/vectorstores/supabase)和[`OpenAIEmbeddings`](https://python.langchain.com/docs/integrations/text_embedding/openai)，我们需要加载它们的API密钥。

## 使用方法

首先，安装LangChain CLI：

```shell
pip install -U langchain-cli
```

要创建一个新的LangChain项目并将其作为唯一的包安装，可以执行以下操作：

```shell
langchain app new my-app --package rag-supabase
```

如果要将其添加到现有项目中，只需运行：

```shell
langchain app add rag-supabase
```

并将以下代码添加到您的`server.py`文件中：

```python
from rag_supabase.chain import chain as rag_supabase_chain

add_routes(app, rag_supabase_chain, path="/rag-supabase")
```

（可选）现在让我们配置LangSmith。
LangSmith将帮助我们跟踪、监视和调试LangChain应用程序。
LangSmith目前处于私有测试版，您可以在[此处](https://smith.langchain.com/)注册。
如果您没有访问权限，可以跳过此部分。

```shell
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=<your-api-key>
export LANGCHAIN_PROJECT=<your-project>  # 如果未指定，默认为"default"
```

如果您在此目录中，则可以直接启动LangServe实例：

```shell
langchain serve
```

这将在本地启动FastAPI应用程序，服务器正在[http://localhost:8000](http://localhost:8000)上运行。

我们可以在[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)上查看所有模板。
我们可以在[http://127.0.0.1:8000/rag-supabase/playground](http://127.0.0.1:8000/rag-supabase/playground)上访问playground。

我们可以通过以下代码访问模板：

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/rag-supabase")
```

TODO：添加有关设置Supabase数据库的详细信息