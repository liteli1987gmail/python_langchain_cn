---
sidebar_position: 1
sidebar_label: Cheerio
hide_table_of_contents: true
---

# 网页，使用Cheerio

本示例演示如何使用Cheerio从网页加载数据。每个网页都将创建一个文档。

Cheerio是一个快速且轻量级的库，允许您使用类似于jQuery的语法解析和遍历HTML文档。您可以使用Cheerio从网页中提取数据，而无需在浏览器中呈现它们。

但是， Cheerio无法模拟浏览器，因此它无法在页面上执行JavaScript代码。这意味着它无法从需要JavaScript呈现的动态网页中提取数据。要做到这一点，您可以使用[PlaywrightWebBaseLoader](./web_playwright.md)或[PuppeteerWebBaseLoader](./web_puppeteer.md)。

## 安装

```bash npm2yarn
npm install cheerio

```


## 使用

```typescript
import { CheerioWebBaseLoader } from "langchain/document_loaders/web/cheerio";



const loader = new CheerioWebBaseLoader(

  "https://news.ycombinator.com/item?id=34817881"

);



const docs = await loader.load();

```


## 使用，自定义选择器

```typescript

import { CheerioWebBaseLoader } from "langchain/document_loaders/web/cheerio";



const loader = new CheerioWebBaseLoader(

  "https://news.ycombinator.com/item?id=34817881",

  {

    selector: "p.athing",

  }

);



const docs = await loader.load();

```

