---
hide_table_of_contents: true
---

# GitBook

本示例介绍如何使用 Cheerio 从任何 GitBook 中加载数据。将为每个页面创建一个文档。

## 设置

```bash npm2yarn
npm install cheerio

```


## 从单个 GitBook 页面加载

```typescript
import { GitbookLoader } from "langchain/document_loaders/web/gitbook";



const loader = new GitbookLoader(

  "https://docs.gitbook.com/product-tour/navigation"

);



const docs = await loader.load();

```


## 从给定 GitBook 中的所有路径加载

为了使此项功能正常工作，需要使用根路径（例如 https://docs.gitbook.com)初始化 GitbookLoader，并将 `shouldLoadAllPaths` 设置为 `true`。

```typescript

import { GitbookLoader } from "langchain/document_loaders/web/gitbook";



const loader = new GitbookLoader("https://docs.gitbook.com", {

  shouldLoadAllPaths: true,

});



const docs = await loader.load();

```

