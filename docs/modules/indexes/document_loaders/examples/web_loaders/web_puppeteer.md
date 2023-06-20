---
sidebar_position: 2
sidebar_label: Puppeteer
hide_table_of_contents: true
sidebar_class_name: node-only
---

# 使用 Puppeteer 打造网页

:::tip 兼容性
仅适用于 Node.js。
:::

本例演示如何使用 Puppeteer 从网站加载数据，并为每个网页创建一个文档。

Puppeteer 是一个基于 Node.js 的库，为控制无头 Chrome 或 Chromium 提供了高级 API。使用 Puppeteer 可以自动化网页交互，包括从需要 JavaScript 渲染的动态网页中提取数据。

如果您想要一个轻量级的解决方案，并且您要加载的网页不需要 JavaScript 渲染，则可以使用 [CheerioWebBaseLoader](./web_cheerio.md)。

## 设置

```bash npm2yarn
npm install puppeteer

```


## 使用

```typescript
import { PuppeteerWebBaseLoader } from "langchain/document_loaders/web/puppeteer";



/**

 * Loader uses `page.evaluate(() => document.body.innerHTML)`

 * as default evaluate function

 **/

const loader = new PuppeteerWebBaseLoader("https://www.tabnews.com.br/");



const docs = await loader.load();

```


## 选项

以下是您可以使用 PuppeteerWebBaseLoaderOptions 接口将参数传递给 PuppeteerWebBaseLoader 构造函数的解释:

```typescript
type PuppeteerWebBaseLoaderOptions = {

  launchOptions?: PuppeteerLaunchOptions;

  gotoOptions?: PuppeteerGotoOptions;

  evaluate?: (page: Page, browser: Browser) => Promise<string>;

};

```


1. `launchOptions`: 一个可选的对象，用于指定要传递给 puppeteer.launch() 方法的附加选项。这可以包括选项，如 headless 标志，以在无头模式下启动浏览器，或者 slowMo 选项，以减慢 Puppeteer 的操作，使其更容易跟踪。

2. `gotoOptions`: 一个可选的对象，用于指定要传递给 page.goto() 方法的附加选项。这可以包括选项，如 timeout 选项，以指定最大导航时间（以毫秒为单位)，或者 waitUntil 选项，以指定何时将导航视为成功。


3. `evaluate`（可选)：可以使用page.evaluate()方法在页面上评估JavaScript代码的可选函数。这对于从页面提取数据或与页面元素交互非常有用。该函数应返回一个Promise，该Promise解析为包含评估结果的字符串。


通过将这些选项传递给`PuppeteerWebBaseLoader`构造函数，您可以自定义加载程序的行为并使用Puppeteer的强大功能来抓取和与网页交互。


以下是一个基本示例:：


```typescript

import { PuppeteerWebBaseLoader } from "langchain/document_loaders/web/puppeteer";



const loader = new PuppeteerWebBaseLoader("https://www.tabnews.com.br/", {

  launchOptions: {

    headless: true,

  },

  gotoOptions: {

    waitUntil: "domcontentloaded",

  },

  /** Pass custom evaluate, in this case you get page and browser instances */

  async evaluate(page: Page, browser: Browser) {

    await page.waitForResponse("https://www.tabnews.com.br/va/view");



    const result = await page.evaluate(() => document.body.innerHTML);

    return result;

  },

});



const docs = await loader.load();

```

