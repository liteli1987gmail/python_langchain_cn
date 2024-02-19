# self-query-supabase

这个模板允许对Supabase进行自然语言结构化查询。

[Supabase](https://supabase.com/docs)是Firebase的开源替代品，构建在[PostgreSQL](https://en.wikipedia.org/wiki/PostgreSQL)之上。

它使用[pgvector](https://github.com/pgvector/pgvector)在您的表中存储嵌入向量。

## 环境设置

将`OPENAI_API_KEY`环境变量设置为访问OpenAI模型。

要获取您的`OPENAI_API_KEY`，请转到您的OpenAI帐户的[API密钥](https://platform.openai.com/account/api-keys)并创建一个新的密钥。

要找到您的`SUPABASE_URL`和`SUPABASE_SERVICE_KEY`，请转到您的Supabase项目的[API设置](https://supabase.com/dashboard/project/_/settings/api)。

- `SUPABASE_URL`对应项目URL
- `SUPABASE_SERVICE_KEY`对应`service_role` API密钥


```shell
export SUPABASE_URL=
export SUPABASE_SERVICE_KEY=
export OPENAI_API_KEY=
```

## 设置Supabase数据库

如果您还没有设置Supabase数据库，请按照以下步骤进行设置。

1. 转到https://database.new以配置您的Supabase数据库。
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
       embedding vector (1536) -- 1536适用于OpenAI嵌入，根据需要进行更改
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

## 使用方法

要使用此包，请先安装LangChain CLI：

```shell
pip install -U langchain-cli
```

创建一个新的LangChain项目，并将此包安装为唯一的包：

```shell
langchain app new my-app --package self-query-supabase
```

要将其添加到现有项目中，请运行：

```shell
langchain app add self-query-supabase
```

将以下代码添加到您的`server.py`文件中：
```python
from self_query_supabase.chain import chain as self_query_supabase_chain

add_routes(app, self_query_supabase_chain, path="/self-query-supabase")
```

（可选）如果您可以访问LangSmith，请配置它以帮助跟踪、监视和调试LangChain应用程序。如果您无法访问，请跳过此部分。

```shell
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=<your-api-key>
export LANGCHAIN_PROJECT=<your-project>  # 如果未指定，默认为"default"
```

如果您在此目录中，则可以直接启动LangServe实例：

```shell
langchain serve
```

这将在本地启动一个运行在[http://localhost:8000](http://localhost:8000)的FastAPI应用程序的服务器

您可以在[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)上查看所有模板
在[http://127.0.0.1:8000/self-query-supabase/playground](http://127.0.0.1:8000/self-query-supabase/playground)上访问playground

通过以下代码从代码中访问模板：

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/self-query-supabase")
```

待办事项：设置Supabase数据库和安装包的说明。