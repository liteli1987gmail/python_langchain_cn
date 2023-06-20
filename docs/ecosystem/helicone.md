# Helicone

本页介绍如何在LangChain中使用[Helicone](https://helicone.ai)。

## Helicone 是什么？

Helicone是一个开源的观测平台，代理您的OpenAI流量，并为您提供有关您的花费、延迟和使用情况的关键见解。

![Helicone](/img/HeliconeDashboard.png)

## 快速入门

在您的LangChain环境中，您只需添加以下参数。

```typescript
const model = new OpenAI(

  {},

  {

    basePath: "https://oai.hconeai.com/v1",

  }

);

const res = await model.call("What is a helicone?");

```


现在，前往[helicone.ai](https://helicone.ai/onboarding?step=2) 创建您的帐户，并在我们的仪表板中添加OpenAI API密钥以查看日志。

![Helicone](/img/HeliconeKeys.png)

## 如何启用Helicone缓存

```typescript
const model = new OpenAI(

  {},

  {

    basePath: "https://oai.hconeai.com/v1",

    baseOptions: {

      headers: {

        "Helicone-Cache-Enabled": "true",

      },

    },

  }

);

const res = await model.call("What is a helicone?");

```


[Helicone缓存文档](https://docs.helicone.ai/advanced-usage/caching)

## 如何使用Helicone自定义属性

```typescript
const model = new OpenAI(

  {},

  {

    basePath: "https://oai.hconeai.com/v1",

    baseOptions: {

      headers: {

        "Helicone-Property-Session": "24",

        "Helicone-Property-Conversation": "support_issue_2",

        "Helicone-Property-App": "mobile",

      },

    },

  }

);

const res = await model.call("What is a helicone?");

```


[Helicone property docs](https://docs.helicone.ai/advanced-usage/custom-properties)

