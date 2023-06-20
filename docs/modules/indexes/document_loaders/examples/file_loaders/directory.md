---
sidebar_position: 1
hide_table_of_contents: true
---

# 具有多个文件夹的文件夹

本示例介绍如何从具有多个文件的文件夹中加载数据。第二个参数是文件扩展名到加载器工厂的映射。每个文件将传递给匹配的加载器， 并将生成的文档连接在一起。

示例文件夹:

```文字
src/document_loaders/example_data/example/

├── example.json

├── example.jsonl

├── example.txt

└── example.csv

```


示例代码:

```typescript

import { DirectoryLoader } from "langchain/document_loaders/fs/directory";

import {

  JSONLoader,

  JSONLinesLoader,

} from "langchain/document_loaders/fs/json";

import { TextLoader } from "langchain/document_loaders/fs/text";

import { CSVLoader } from "langchain/document_loaders/fs/csv";



const loader = new DirectoryLoader(

  "src/document_loaders/example_data/example",

  {

    ".json": (path) => new JSONLoader(path, "/texts"),

    ".jsonl": (path) => new JSONLinesLoader(path, "/html"),

    ".txt": (path) => new TextLoader(path),

    ".csv": (path) => new CSVLoader(path, "text"),

  }

);

const docs = await loader.load();

console.log({ docs });

```

