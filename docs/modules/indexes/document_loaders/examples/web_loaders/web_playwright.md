---
sidebar_position: 3
hide_table_of_contents: true
sidebar_class_name: node-only
sidebar_label: Playwright
---

# Webpages， with Playwright

:::tip 兼容性
仅限于 Node.js。
:::

本示例演示了如何使用 Playwright 从网页中加载数据。将为每个网页创建一个文档。

Playwright 是一个 Node.js 库，提供了一个高级 API，用于控制多个浏览器引擎，包括 Chromium、Firefox 和 WebKit。您可以使用 Playwright 自动化网页交互，包括从需要 JavaScript 渲染的动态网页中提取数据。

如果您想要一个更轻量级的解决方案，想要加载的网页不需要 JavaScript 渲染，那么可以使用 [CheerioWebBaseLoader](./web_cheerio.md)。

## 设置

```bash npm2yarn
npm install playwright

```


## 用法

```typescript
import { PlaywrightWebBaseLoader } from "langchain/document_loaders/web/playwright";



/**

 * Loader uses `page.content()`

 * as default evaluate function

 **/

const loader = new PlaywrightWebBaseLoader("https://www.tabnews.com.br/");



const docs = await loader.load();

```


## 选项

这里是关于可以通过使用 PlaywrightWebBaseLoaderOptions 接口将参数传递给 PlaywrightWebBaseLoader 构造函数的参数的解释:

```typescript
type PlaywrightWebBaseLoaderOptions = {

  launchOptions?: LaunchOptions;

  gotoOptions?: PlaywrightGotoOptions;

  evaluate?: PlaywrightEvaluate;

};

```


1. `launchOptions`: 一个可选对象，用于指定要传递给 playwright.chromium.launch() 方法的其他选项。这可以包括选项，例如在无头模式下启动浏览器的 headless 标志。

2. `gotoOptions`: 一个可选对象，用于指定要传递给 page.goto() 方法的其他选项。这可以包括选项，例如 timeout 选项以指定最大导航时间（以毫秒为单位)或 waitUntil 选项以指定何时将导航视为成功。


3. `evaluate`: 是一个可选函数，可以使用自定义评估函数在页面上评估JavaScript代码。这对于从页面提取数据或与页面元素进行交互非常有用。该函数应返回解析为包含评估结果的字符串的Promise。


通过将这些选项传递给`PlaywrightWebBaseLoader`构造函数,您可以自定义加载程序的行为，并使用Playwright强大的功能对Web页面进行抓取和交互。


以下是一个基本示例:：


```typescript

import { PlaywrightWebBaseLoader } from "langchain/document_loaders/web/playwright";



const loader = new PlaywrightWebBaseLoader("https://www.tabnews.com.br/", {

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

