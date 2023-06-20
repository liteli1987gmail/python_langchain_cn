

# Milvus

[Milvus](https://milvus.io/)是专为嵌入式相似性搜索和 AI 应用而构建的向量数据库。

:::info 兼容性
仅可在 Node.js 上使用。
:::

## 安装

1. 在计算机上使用 Docker 运行 Milvus 实例 [文档](https://milvus.io/docs/v2.1.x/install_standalone-docker.md)
2. 安装 Milvus Node.js SDK。

   ```bash npm2yarn

   npm install -S @zilliz/milvus2-sdk-node

   ```


3. 在运行代码之前设置 Milvus 的环境变量

   3.1 OpenAI


   ```bash

   export OPENAI_API_KEY=YOUR_OPENAI_API_KEY_HERE

   export MILVUS_URL=YOUR_MILVUS_URL_HERE # for example http://localhost:19530

   ```


   3.2 Azure OpenAI


   ```bash

   export AZURE_OPENAI_API_KEY=YOUR_AZURE_OPENAI_API_KEY_HERE

   export AZURE_OPENAI_API_INSTANCE_NAME=YOUR_AZURE_OPENAI_INSTANCE_NAME_HERE

   export AZURE_OPENAI_API_DEPLOYMENT_NAME=YOUR_AZURE_OPENAI_DEPLOYMENT_NAME_HERE

   export AZURE_OPENAI_API_COMPLETIONS_DEPLOYMENT_NAME=YOUR_AZURE_OPENAI_COMPLETIONS_DEPLOYMENT_NAME_HERE

   export AZURE_OPENAI_API_EMBEDDINGS_DEPLOYMENT_NAME=YOUR_AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME_HERE

   export AZURE_OPENAI_API_VERSION=YOUR_AZURE_OPENAI_API_VERSION_HERE

   export MILVUS_URL=YOUR_MILVUS_URL_HERE # for example http://localhost:19530

   ```


## 索引和查询文档

```typescript
import { Milvus } from "langchain/vectorstores/milvus";

import { OpenAIEmbeddings } from "langchain/embeddings/openai";



// text sample from Godel, Escher, Bach

const vectorStore = await Milvus.fromTexts(

  [

    "Tortoise: Labyrinth? Labyrinth? Could it Are we in the notorious Little\

            Harmonic Labyrinth of the dreaded Majotaur?",

    "Achilles: Yiikes! What is that?",

    "Tortoise: They say-although I person never believed it myself-that an I\

            Majotaur has created a tiny labyrinth sits in a pit in the middle of\

            it, waiting innocent victims to get lost in its fears complexity.\

            Then, when they wander and dazed into the center, he laughs and\

            laughs at them-so hard, that he laughs them to death!",

    "Achilles: Oh, no!",

    "Tortoise: But it's only a myth. Courage, Achilles.",

  ],

  [{ id: 2 }, { id: 1 }, { id: 3 }, { id: 4 }, { id: 5 }],

  new OpenAIEmbeddings(),

  {

    collectionName: "goldel_escher_bach",

  }

);



// or alternatively from docs

const vectorStore = await Milvus.fromDocuments(docs, new OpenAIEmbeddings(), {

  collectionName: "goldel_escher_bach",

});



const response = await vectorStore.similaritySearch("scared", 2);

```


## 查询现有集合的文档

```typescript

import { Milvus } from "langchain/vectorstores/milvus";

import { OpenAIEmbeddings } from "langchain/embeddings/openai";



const vectorStore = await Milvus.fromExistingCollection(

  new OpenAIEmbeddings(),

  {

    collectionName: "goldel_escher_bach",

  }

);



const response = await vectorStore.similaritySearch("scared", 2);

```

