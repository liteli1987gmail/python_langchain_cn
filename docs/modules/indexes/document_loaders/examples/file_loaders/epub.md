---
sidebar_label: EPUB文件
---

# EPUB文件

本例演示如何从EPUB文件中加载数据。默认情况下，每个章节会创建一个文档，您可以通过将“splitChapters”选项设置为“false”来更改此行为。

# 设置

```bash npm2yarn
npm install epub2 html-to-text

```


# 用法：每章一个文档

```typescript
import { EPubLoader } from "langchain/document_loaders/fs/epub";



const loader = new EPubLoader("src/document_loaders/example_data/example.epub");



const docs = await loader.load();

```


# 用法：每个文件一个文档

```typescript

import { EPubLoader } from "langchain/document_loaders/fs/epub";



const loader = new EPubLoader(

  "src/document_loaders/example_data/example.epub",

  {

    splitChapters: false,

  }

);



const docs = await loader.load();

```

