# CSV文件

本示例介绍如何从CSV文件加载数据。

第二个参数是要从CSV文件中提取的“列”名称。每行CSV文件将创建一个文档。

当未指定“列”时，每一行都将转换为一个键/值对，并将每个键/值对输出到文档的“pageContent”中的新行中。

当指定了“列”时，将为每一行创建一个文档，并将指定列的值用作文档的“pageContent”。

备注：该处的“pageContent”指文档的页面内容)

## 设置

```bash npm2yarn
npm install d3-dsv@2

```


## 用法-提取所有列

示例CSV文件:

```csv
id,text

1,This is a sentence.

2,This is another sentence.

```


示例代码:

```typescript
import { CSVLoader } from "langchain/document_loaders/fs/csv";



const loader = new CSVLoader("src/document_loaders/example_data/example.csv");



const docs = await loader.load();

/*

[

  Document {

    "metadata": {

      "line": 1,

      "source": "src/document_loaders/example_data/example.csv",

    },

    "pageContent": "id: 1

text: This is a sentence.",

  },

  Document {

    "metadata": {

      "line": 2,

      "source": "src/document_loaders/example_data/example.csv",

    },

    "pageContent": "id: 2

text: This is another sentence.",

  },

]

*/

```


## 用法-提取单个列

示例CSV文件:

```csv
id,text

1,This is a sentence.

2,This is another sentence.

```


示例代码:

```typescript

import { CSVLoader } from "langchain/document_loaders/fs/csv";



const loader = new CSVLoader(

  "src/document_loaders/example_data/example.csv",

  "text"

);



const docs = await loader.load();

/*

[

  Document {

    "metadata": {

      "line": 1,

      "source": "src/document_loaders/example_data/example.csv",

    },

    "pageContent": "This is a sentence.",

  },

  Document {

    "metadata": {

      "line": 2,

      "source": "src/document_loaders/example_data/example.csv",

    },

    "pageContent": "This is another sentence.",

  },

]

*/

```

