---
sidebar_label: 使用 AWS Lambda 的代理
hide_table_of_contents: true
---

# 使用 AWS Lambda 集成代理

请查看完整文档: https://docs.aws.amazon.com/lambda/index.html

**AWS Lambda** 是由亚马逊网络服务（AWS)提供的无服务器计算服务，旨在允许开发人员构建和运行应用程序和服务，无需提供或管理服务器。这种无服务器架构使您能够专注于编写和部署代码，而 AWS 会自动处理扩展，补丁和管理所需的基础架构来运行您的应用程序。

通过在提供给代理工具列表中包含 AWSLambda，您可以授予代理调用在您的 AWS Cloud 中运行的代码的能力，以满足您的需求。

当代理使用 AWSLambda 工具时，它将提供一个 `string` 类型的参数，该参数将通过 `event` 参数传递到 Lambda 函数中。

这个快速入门将演示代理如何使用 Lambda 函数通过 [Amazon 简单邮件服务](https://aws.amazon.com/ses/) 发送电子邮件。发送电子邮件的 lambda 代码未提供，但如果您想了解这可以如何完成，请参见[此处](https://repost.aws/knowledge-center/lambda-send-email-ses)。请记住，这只是一个故意简单的例子；Lambda 可用于执行无限数量的其他目的（包括执行更多的 Langchains)！

### 凭据注释:

- 如果你没有通过AWS CLI运行过[`aws configure`](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)，则必须在AWSLambda构造函数中提供`region`, `accessKeyId`, 和 `secretAccessKey`。

使用这些凭证的IAM角色必须具有调用Lambda函数的权限。


```typescript

import { OpenAI } from "langchain/llms/openai";

import { SerpAPI } from "langchain/tools";

import { AWSLambda } from "langchain/tools/aws_lambda";

import { initializeAgentExecutorWithOptions } from "langchain/agents";



const model = new OpenAI({ temperature: 0 });

const emailSenderTool = new AWSLambda({

  name: "email-sender",

  // tell the Agent precisely what the tool does

  description:

    "Sends an email with the specified content to testing123@gmail.com",

  region: "us-east-1", // optional: AWS region in which the function is deployed

  accessKeyId: "abc123", // optional: access key id for a IAM user with invoke permissions

  secretAccessKey: "xyz456", // optional: secret access key for that IAM user

  functionName: "SendEmailViaSES", // the function name as seen in AWS Console

});

const tools = [emailSenderTool, new SerpAPI("api_key_goes_here")];

const executor = await initializeAgentExecutorWithOptions(tools, model, {

  agentType: "zero-shot-react-description",

});



const input = `Find out the capital of Croatia. Once you have it, email the answer to testing123@gmail.com.`;

const result = await executor.call({ input });

console.log(result);

```

