# 带有向量存储的代理


本笔记涵盖了如何将代理和向量存储器组合使用。这种用例是，您已将数据摄入向量存储器中，并想以代理方式与其进行交互。


建议的方法是创建一个VectorDBQAChain，然后将其用作整体代理工具。让我们在下面看看如何做到这一点。您可以使用多个不同的向量数据库进行此操作，并使用代理作为它们之间选择的一种方式。有两种不同的方法可以实现这一点 - 您可以让代理像正常工具一样使用向量存储器，或者您可以设置`returnDirect: true`仅将代理用作路由器。


首先，您需要导入相关模块。


```typescript
import { OpenAI } from "langchain/llms/openai";

import { initializeAgentExecutorWithOptions } from "langchain/agents";

import { SerpAPI, ChainTool } from "langchain/tools";

import { Calculator } from "langchain/tools/calculator";

import { VectorDBQAChain } from "langchain/chains";

import { HNSWLib } from "langchain/vectorstores/hnswlib";

import { OpenAIEmbeddings } from "langchain/embeddings/openai";

import { RecursiveCharacterTextSplitter } from "langchain/text_splitter";

import * as fs from "fs";

```



接下来，您需要创建具有数据的向量存储器，然后创建与该向量存储器交互的QA链。


```typescript
const model = new OpenAI({ temperature: 0 });

/* Load in the file we want to do question answering over */

const text = fs.readFileSync("state_of_the_union.txt", "utf8");

/* Split the text into chunks */

const textSplitter = new RecursiveCharacterTextSplitter({ chunkSize: 1000 });

const docs = await textSplitter.createDocuments([text]);

/* Create the vectorstore */

const vectorStore = await HNSWLib.fromDocuments(docs, new OpenAIEmbeddings());

/* Create the chain */

const chain = VectorDBQAChain.fromLLM(model, vectorStore);

```



现在您拥有了该链，可以创建一个工具来使用该链。请注意，您应该更新名称和描述以特定于QA链。


```typescript
const qaTool = new ChainTool({

  name: "state-of-union-qa",

  description:

    "State of the Union QA - useful for when you need to ask questions about the most recent state of the union address.",

  chain: chain,

});

```



现在，您可以构建并使用该工具，就像使用任何其他工具一样！


```typescript
const tools = [

  new SerpAPI(process.env.SERPAPI_API_KEY, {

    location: "Austin,Texas,United States",

    hl: "en",

    gl: "us",

  }),

  new Calculator(),

  qaTool,

];



const executor = await initializeAgentExecutorWithOptions(tools, model, {

  agentType: "zero-shot-react-description",

});

console.log("Loaded agent.");



const input = `What did biden say about ketanji brown jackson is the state of the union address?`;



console.log(`Executing with input "${input}"...`);



const result = await executor.call({ input });



console.log(`Got output ${result.output}`);

```



如果您打算使用代理作为路由器，并且仅想直接返回VectorDBQAChain的结果，则还可以设置`returnDirect: true`。


```typescript

const qaTool = new ChainTool({

  name: "state-of-union-qa",

  description:

    "State of the Union QA - useful for when you need to ask questions about the most recent state of the union address.",

  chain: chain,

  returnDirect: true,

});

```

