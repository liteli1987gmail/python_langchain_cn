# JSON文件

JSON加载器使用[JSON指针](https://github.com/janl/node-jsonpointer)来定位您想要定位的JSON文件中的键。

### 无JSON指针示例

最简单的使用方式是不指定JSON指针。
加载程序将加载JSON对象中找到的所有字符串。

示例JSON文件:

```json
{

  "texts": ["This is a sentence.", "This is another sentence."]

}

```


示例代码:

```typescript
import { JSONLoader } from "langchain/document_loaders/fs/json";



const loader = new JSONLoader("src/document_loaders/example_data/example.json");



const docs = await loader.load();

/*

[

  Document {

    "metadata": {

      "blobType": "application/json",

      "line": 1,

      "source": "blob",

    },

    "pageContent": "This is a sentence.",

  },

  Document {

    "metadata": {

      "blobType": "application/json",

      "line": 2,

      "source": "blob",

    },

    "pageContent": "This is another sentence.",

  },

]

*/

```


### 使用JSON指针示例

您可以通过选择要从JSON对象中提取字符串的哪些键来执行更高级的场景。

在此示例中，我们仅想从“from”和“surname”条目中提取信息。

```json
{

  "1": {

    "body": "BD 2023 SUMMER",

    "from": "LinkedIn Job",

    "labels": ["IMPORTANT", "CATEGORY_UPDATES", "INBOX"]

  },

  "2": {

    "body": "Intern, Treasury and other roles are available",

    "from": "LinkedIn Job2",

    "labels": ["IMPORTANT"],

    "other": {

      "name": "plop",

      "surname": "bob"

    }

  }

}

```


示例代码:

```typescript

import { JSONLoader } from "langchain/document_loaders/fs/json";



const loader = new JSONLoader(

  "src/document_loaders/example_data/example.json",

  ["/from", "/surname"]

);



const docs = await loader.load();

/*

[

  Document {

    "metadata": {

      "blobType": "application/json",

      "line": 1,

      "source": "blob",

    },

    "pageContent": "BD 2023 SUMMER",

  },

  Document {

    "metadata": {

      "blobType": "application/json",

      "line": 2,

      "source": "blob",

    },

    "pageContent": "LinkedIn Job",

  },

  ...

]

```

