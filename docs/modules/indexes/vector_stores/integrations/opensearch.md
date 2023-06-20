---
sidebar_class_name: 仅限 Node.js
---

# OpenSearch

:::tip 兼容性
仅限于 Node.js。
:::

[OpenSearch](https://opensearch.org/) 是完全兼容 Elasticsearch API 的 Elasticsearch 分支。在此处阅读有关其支持近似最近邻的更多信息 [here](https://opensearch.org/docs/latest/search-plugins/knn/approximate-knn/)。

Langchain.js 将 [@opensearch-project/opensearch](https://opensearch.org/docs/latest/clients/javascript/index/) 作为 OpenSearch vectorstore 的客户端。

## 设置

```bash npm2yarn
npm install -S @opensearch-project/opensearch

```


您还需要运行一个 OpenSearch 实例。您可以使用 [官方 Docker 映像](https://opensearch.org/docs/latest/opensearch/install/docker/) 来开始使用。您还可以在 [此处](https://github.com/hwchase17/langchainjs/blob/main/examples/src/indexes/vector_stores/opensearch/docker-compose.yml) 找到示例 docker-compose 文件。

## 索引文档

```typescript
import { Client } from "@opensearch-project/opensearch";

import { Document } from "langchain/document";

import { OpenAIEmbeddings } from "langchain/embeddings/openai";

import { OpenSearchVectorStore } from "langchain/vectorstores/opensearch";



const client = new Client({

  nodes: [process.env.OPENSEARCH_URL ?? "http://127.0.0.1:9200"],

});



const docs = [

  new Document({

    metadata: { foo: "bar" },

    pageContent: "opensearch is also a vector db",

  }),

  new Document({

    metadata: { foo: "bar" },

    pageContent: "the quick brown fox jumped over the lazy dog",

  }),

  new Document({

    metadata: { baz: "qux" },

    pageContent: "lorem ipsum dolor sit amet",

  }),

  new Document({

    metadata: { baz: "qux" },

    pageContent:

      "OpenSearch is a scalable, flexible, and extensible open-source software suite for search, analytics, and observability applications",

  }),

];



await OpenSearchVectorStore.fromDocuments(docs, new OpenAIEmbeddings(), {

  client,

  indexName: process.env.OPENSEARCH_INDEX, // Will default to `documents`

});

```


## 查询文档

```typescript

import { Client } from "@opensearch-project/opensearch";

import { VectorDBQAChain } from "langchain/chains";

import { OpenAIEmbeddings } from "langchain/embeddings/openai";

import { OpenAI } from "langchain/llms/openai";

import { OpenSearchVectorStore } from "langchain/vectorstores/opensearch";



const client = new Client({

  nodes: [process.env.OPENSEARCH_URL ?? "http://127.0.0.1:9200"],

});



const vectorStore = new OpenSearchVectorStore(new OpenAIEmbeddings(), {

  client,

});



/* Search the vector DB independently with meta filters */

const results = await vectorStore.similaritySearch("hello world", 1);

console.log(JSON.stringify(results, null, 2));

/* [

    {

      "pageContent": "Hello world",

      "metadata": {

        "id": 2

      }

    }

  ] */



/* Use as part of a chain (currently no metadata filters) */

const model = new OpenAI();

const chain = VectorDBQAChain.fromLLM(model, vectorStore, {

  k: 1,

  returnSourceDocuments: true,

});

const response = await chain.call({ query: "What is opensearch?" });



console.log(JSON.stringify(response, null, 2));

/* 

  {

    "text": " Opensearch is a collection of technologies that allow search engines to publish search results in a standard format, making it easier for users to search across multiple sites.",

    "sourceDocuments": [

      {

        "pageContent": "What's this?",

        "metadata": {

          "id": 3

        }

      }

    ]

  } 

  */

```

