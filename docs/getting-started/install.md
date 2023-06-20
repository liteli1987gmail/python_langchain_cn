---
sidebar_position: 1
---

# 安装和设置



## 支持的环境

LangChain 是使用 TypeScript 编写的，可以在以下环境中使用:

- Node.js (ESM 和 CommonJS) - 18.x， 19.x， 20.x
- Cloudflare Workers
- Vercel / Next.js (浏览器， 无服务器和边缘函数)
- Supabase Edge 函数
- 浏览器
- Deno

## 快速开始

如果您想在 Node.js 中快速开始使用 LangChain，请[克隆此存储库](https://github.com/domeccleston/langchain-ts-starter) 并按照自述文件中的说明设置依赖项。

如果您希望自己设置或者在其他环境中运行 LangChain，请继续阅读下面的说明。

## 安装

要开始使用 LangChain，请使用以下命令安装:

```bash npm2yarn
npm install -S langchain

```


### TypeScript

LangChain 是使用 TypeScript 编写的，并为其所有的公共 API 提供了类型定义。

## 加载库

### ESM

LangChain 为 Node.js 环境提供了一个 ESM 构建版。您可以使用以下语法导入它:

```typescript
import { OpenAI } from "langchain/llms/openai";

```


如果您在一个 ESM 项目中使用 TypeScript，我们建议您更新您的 `tsconfig.json`，并包含以下设置:

```json title="tsconfig.json"
{

  "compilerOptions": {

    ...

    "target": "ES2020", // or higher

    "module": "nodenext",

  }

}

```


### CommonJS


LangChain提供了面向Node.js环境的CommonJS构建。你可以使用以下语法进行导入:。

```typescript
const { OpenAI } = require("langchain/llms/openai");

```


### Cloudflare Workers

LangChain可以在Cloudflare Workers中使用。你可以使用以下语法进行导入:。

```typescript
import { OpenAI } from "langchain/llms/openai";

```


### Vercel / Next.js

LangChain可以在Vercel / Next.js中使用。我们支持在前端组件、无服务器函数和Edge函数中使用LangChain。你可以使用以下语法进行导入:。

```typescript
import { OpenAI } from "langchain/llms/openai";

```


### Deno / Supabase Edge Functions

LangChain可以在Deno / Supabase Edge Functions中使用。你可以使用以下语法进行导入:。

```typescript
import { OpenAI } from "https://esm.sh/langchain/llms/openai";

```


我们推荐查看我们的[Supabase模板](https://github.com/langchain-ai/langchain-template-supabase)以查看在Supabase Edge Functions中如何使用LangChain的示例。

### 浏览器

LangChain可以在浏览器中使用。在我们的CI中，我们使用Webpack和Vite测试了LangChain的捆绑，但其他捆绑器也应该可以使用。你可以使用以下语法进行导入:。

```typescript
import { OpenAI } from "langchain/llms/openai";

```


## 从版本<0.0.52进行更新

如果您正在更新LangChain的0.0.52之前的版本，您需要更新导入以使用新的路径结构。

例如，如果您以前执行的是

```typescript
import { OpenAI } from "langchain/llms";

```


现在，您需要执行以下操作

```typescript
import { OpenAI } from "langchain/llms/openai";

```



适用于下列6个模块的所有导入，这些模块已分割为每个集成的子模块。组合模块已被弃用，在 Node.js 之外不起作用，并将在将来的版本中删除。

- 如果您使用的是 `langchain/llms`，请参见 [LLMs](../modules/models/llms/integrations) 以获取更新后的导入路径。
- 如果您使用的是 `langchain/chat_models`，请参见 [Chat Models](../modules/models/chat/integrations) 以获取更新后的导入路径。
- 如果您使用的是 `langchain/embeddings`，请参见 [Embeddings](../modules/models/embeddings/integrations) 以获取更新后的导入路径。
- 如果您使用的是 `langchain/vectorstores`，请参见 [Vector Stores](../modules/indexes/vector_stores/integrations/) 以获取更新后的导入路径。
- 如果您使用的是 `langchain/document_loaders`，请参见 [Document Loaders](../modules/indexes/document_loaders/examples/) 以获取更新后的导入路径。
- 如果您使用的是 `langchain/retrievers`，请参见 [Retrievers](../modules/indexes/retrievers/) 以获取更新后的导入路径。

其他模块不受此更改影响，您可以继续从同一路径导入它们。

此外，为了支持新的环境，需要进行一些重大更改:

- `import { Calculator } from "langchain/tools";` 现已移至
  - `import { Calculator } from "langchain/tools/calculator";`

- `import { loadLLM } from "langchain/llms";` 现已移至
  - `import { loadLLM } from "langchain/llms/load";`

- `import { loadAgent } from "langchain/agents";` 现已移至
  - `import { loadAgent } from "langchain/agents/load";`

- `import { loadPrompt } from "langchain/prompts";` 现已移至
  - `import { loadPrompt } from "langchain/prompts/load";`

- `import { loadChain } from "langchain/chains";` 现已移至
  - `import { loadChain } from "langchain/chains/load";`


## 不受支持: Node.js 16


我们不支持 Node.js 16，但如果您仍然希望在 Node.js 16 上运行 LangChain，您需要按照本节中的说明进行操作。我们不能保证这些说明在未来仍能工作。


您将需要全局安装`fetch`， 可以通过以下方式之一来实现:


- 使用 `NODE_OPTIONS='--experimental-fetch' node ...` 命令运行您的应用程序， 或
- 安装 `node-fetch` 并按照[此处](https://github.com/node-fetch/node-fetch#providing-global-access)的说明进行操作


此外，您还需要将 `unstructuredClone` 进行 polyfill， 您可以通过安装 `core-js` 并按照[此处](https://github.com/zloirock/core-js)的说明进行操作来实现。

如果您在 Node.js 18+ 上运行此代码，您不需要采取任何措施。