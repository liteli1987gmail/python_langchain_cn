---
hide_table_of_contents: true
---

# 字幕

本示例介绍如何从字幕文件中加载数据。每个字幕文件将创建一个文档。

## 设置

```bash npm2yarn
npm install srt-parser-2

```


## 用法

```typescript

import { SRTLoader } from "langchain/document_loaders/fs/srt";



const loader = new SRTLoader(

  "src/document_loaders/example_data/Star_Wars_The_Clone_Wars_S06E07_Crisis_at_the_Heart.srt"

);



const docs = await loader.load();

```

