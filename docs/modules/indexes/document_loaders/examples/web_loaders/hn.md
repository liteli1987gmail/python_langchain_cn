---
hide_table_of_contents: true
---

# 黑客新闻

本例介绍如何使用Cheerio从黑客新闻网站加载数据。每页将创建一个文档。

## 设置

```bash npm2yarn（备注：将npm命令转化为yarn)
npm install cheerio

```


## 用法

```typescript

import { HNLoader } from "langchain/document_loaders/web/hn";



const loader = new HNLoader("https://news.ycombinator.com/item?id=34817881");



const docs = await loader.load();

```

