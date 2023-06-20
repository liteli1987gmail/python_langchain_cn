# 追踪

与 Python 的 `langchain` 包类似，JS 的 `langchain` 也支持追踪。

您可以在[这里](https://python.langchain.com/en/latest/additional_resources/tracing.html)查看追踪的概述。
要启动追踪后端，请在 `langchain` 目录下运行 `docker compose up`(如果使用较旧版本的 `docker`，则使用`docker-compose up`)。
如果您已安装 Python 的 `langchain` 包，还可以使用 `langchain-server` 命令。

以下是如何在 `langchain.js` 中使用追踪的示例。唯一需要做的就是将 `LANGCHAIN_TRACING` 环境变量设置为 `true`。

```typescript
import { OpenAI } from "langchain/llms/openai";

import { initializeAgentExecutorWithOptions } from "langchain/agents";

import { SerpAPI } from "langchain/tools";

import { Calculator } from "langchain/tools/calculator";

import process from "process";



export const run = async () => {

  process.env.LANGCHAIN_TRACING = "true";

  const model = new OpenAI({ temperature: 0 });

  const tools = [

    new SerpAPI(process.env.SERPAPI_API_KEY, {

      location: "Austin,Texas,United States",

      hl: "en",

      gl: "us",

    }),

    new Calculator(),

  ];



  const executor = await initializeAgentExecutorWithOptions(tools, model, {

    agentType: "zero-shot-react-description",

    verbose: true,

  });

  console.log("Loaded agent.");



  const input = `Who is Olivia Wilde's boyfriend? What is his current age raised to the 0.23 power?`;



  console.log(`Executing with input "${input}"...`);



  const result = await executor.call({ input });



  console.log(`Got output ${result.output}`);

};

```


## 并发

追踪默认支持并发处理。

```typescript

import { OpenAI } from "langchain/llms/openai";

import { initializeAgentExecutorWithOptions } from "langchain/agents";

import { SerpAPI } from "langchain/tools";

import { Calculator } from "langchain/tools/calculator";

import process from "process";



export const run = async () => {

  process.env.LANGCHAIN_TRACING = "true";

  const model = new OpenAI({ temperature: 0 });

  const tools = [

    new SerpAPI(process.env.SERPAPI_API_KEY, {

      location: "Austin,Texas,United States",

      hl: "en",

      gl: "us",

    }),

    new Calculator(),

  ];



  const executor = await initializeAgentExecutorWithOptions(tools, model, {

    agentType: "zero-shot-react-description",

    verbose: true,

  });



  console.log("Loaded agent.");



  const input = `Who is Olivia Wilde's boyfriend? What is his current age raised to the 0.23 power?`;



  console.log(`Executing with input "${input}"...`);



  // This will result in a lot of errors, because the shared Tracer is not concurrency-safe.

  const [resultA, resultB, resultC] = await Promise.all([

    executor.call({ input }),

    executor.call({ input }),

    executor.call({ input }),

  ]);



  console.log(`Got output ${resultA.output} ${resultA.__run.runId}`);

  console.log(`Got output ${resultB.output} ${resultB.__run.runId}`);

  console.log(`Got output ${resultC.output} ${resultC.__run.runId}`);



  /*

    Got output Harry Styles, Olivia Wilde's boyfriend, is 29 years old and his age raised to the 0.23 power is 2.169459462491557. b8fb98aa-07a5-45bd-b593-e8d7376b05ca

    Got output Harry Styles, Olivia Wilde's boyfriend, is 29 years old and his age raised to the 0.23 power is 2.169459462491557. c8d916d5-ca1d-4702-8dd7-cab5e438578b

    Got output Harry Styles, Olivia Wilde's boyfriend, is 29 years old and his age raised to the 0.23 power is 2.169459462491557. bf5fe04f-ef29-4e55-8ce1-e4aa974f9484

    */

};

```

