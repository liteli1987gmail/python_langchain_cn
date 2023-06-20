---
hide_table_of_contents: true
---

# Docx files

本示例介绍如何从docx文件中加载数据。

# 安装 Setup

```bash npm2yarn
npm install mammoth

```


# 用法 Usage

```typescript

import { DocxLoader } from "langchain/document_loaders/fs/docx";



const loader = new DocxLoader(

  "src/document_loaders/tests/example_data/attention.docx"

);



const docs = await loader.load();

```

