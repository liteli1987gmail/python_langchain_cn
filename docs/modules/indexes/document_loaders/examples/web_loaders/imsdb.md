---
hide_table_of_contents: true
---

# IMSDB

本例介绍如何使用Cheerio从互联网电影剧本数据库网站加载数据。每个页面将创建一个文档。

## 设置

```bash 将npm转换为yarn
npm install cheerio

```


## 用法

```typescript

import { IMSDBLoader } from "langchain/document_loaders/web/imsdb";



const loader = new IMSDBLoader("https://imsdb.com/scripts/BlacKkKlansman.html");



const docs = await loader.load();

```

