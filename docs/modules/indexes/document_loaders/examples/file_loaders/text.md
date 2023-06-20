---
hide_table_of_contents: true
---

# 文本文件

本例将介绍如何从文本文件中加载数据。

```typescript

import { TextLoader } from "langchain/document_loaders/fs/text";



const loader = new TextLoader("src/document_loaders/example_data/example.txt");



const docs = await loader.load();

```

