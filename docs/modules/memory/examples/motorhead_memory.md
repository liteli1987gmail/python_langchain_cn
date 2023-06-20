# motorhead_memory


[Motörhead](https://github.com/getmetal/motorhead) 是一个由Rust实现的内存服务器。它可以自动处理增量摘要并允许无状态应用程序。


### 设置


请参阅 [Motörhead](https://github.com/getmetal/motorhead) 的指示以在本地运行服务器。


### 用法


```typescript
import { ConversationChain } from "langchain/chains";

import { ChatOpenAI } from "langchain/chat_models";

import { MotorheadMemory } from "langchain/memory";



const model = new ChatOpenAI({});

const memory = new MotorheadMemory({

  sessionId: "user-id",

  motorheadURL: "localhost:8080",

});



await memory.init(); // loads previous state from Motörhead 🤘

const context = memory.context

  ? `

Here's previous context: ${memory.context}`

  : "";



const chatPrompt = ChatPromptTemplate.fromPromptMessages([

  SystemMessagePromptTemplate.fromTemplate(

    `The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.${context}`

  ),

  new MessagesPlaceholder("history"),

  HumanMessagePromptTemplate.fromTemplate("{input}"),

]);



const chain = new ConversationChain({

  memory,

  prompt: chatPrompt,

  llm: chat,

});



const res1 = await chain.call({ input: "Hi! I'm Jim." });

console.log({ res1 });

```

```shell
```shell

{response: " Hi Jim! It's nice to meet you. My name is AI. What would you like to talk about?"}

```



```typescript
const res2 = await chain.call({ input: "What's my name?" });

console.log({ res2 });

```



```shell

{response: ' You said your name is Jim. Is there anything else you would like to talk about?'}

```

