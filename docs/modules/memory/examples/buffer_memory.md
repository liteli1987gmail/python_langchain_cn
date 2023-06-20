## 缓存内存

缓存内存是最简单的一种内存 - 它直接记住了以前的对话回合。

```typescript
import { OpenAI } from "langchain/llms/openai";

import { BufferMemory } from "langchain/memory";

import { ConversationChain } from "langchain/chains";



const model = new OpenAI({});

const memory = new BufferMemory();

const chain = new ConversationChain({ llm: model, memory: memory });

const res1 = await chain.call({ input: "Hi! I'm Jim." });

console.log({ res1 });

```


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


您还可以通过创建并传递一个`ChatHistory`对象来将消息加载到`BufferMemory`实例中。
这使您可以轻松地从过去的对话中获取状态。
```typescript

import { ChatMessageHistory } from "langchain/memory";

import { HumanChatMessage, AIChatMessage } from "langchain/schema";



const pastMessages = [

  new HumanChatMessage("My name's Jonas"),

  new AIChatMessage("Nice to meet you, Jonas!"),

];



const memory = new BufferMemory({

  chatHistory: new ChatMessageHistory(pastMessages),

});

```

