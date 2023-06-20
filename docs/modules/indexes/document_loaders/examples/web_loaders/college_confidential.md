---
hide_table_of_contents: true
---

# 大学机密

本例说明了如何使用Cheerio从大学机密网站加载数据。每个页面将创建一个文档。

## 设置

```bash npm2yarn
npm install cheerio

```


## 用法

```typescript

import { CollegeConfidentialLoader } from "langchain/document_loaders/web/college_confidential";



const loader = new CollegeConfidentialLoader(

  "https://www.collegeconfidential.com/colleges/brown-university/"

);



const docs = await loader.load();

```

