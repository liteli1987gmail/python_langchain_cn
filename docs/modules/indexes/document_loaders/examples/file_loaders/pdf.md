# PDF文件

在这个例子中，我们将介绍如何从PDF文件中导入数据。默认情况下，每个页面将创建一个文档。通过将 `splitPages` 选项设置为 `false` 可以更改此行为。

## 设置

```bash npm2yarn
npm install pdf-parse

```


## 用法，每个页面一个文档

```typescript
import { PDFLoader } from "langchain/document_loaders/fs/pdf";



const loader = new PDFLoader("src/document_loaders/example_data/example.pdf");



const docs = await loader.load();

```


## 用法，每个文件一个文档

```typescript
import { PDFLoader } from "langchain/document_loaders/fs/pdf";



const loader = new PDFLoader("src/document_loaders/example_data/example.pdf", {

  splitPages: false,

});



const docs = await loader.load();

```


## 用法，自定义 `pdfjs` 构建

默认情况下，我们使用与大多数环境（包括 Node.js 和现代浏览器)兼容的 `pdf-parse` 捆绑的 `pdfjs` 构建。如果要使用更高版本的 `pdfjs-dist` ，或者要使用自定义构建的 `pdfjs-dist` ，则可以提供返回解析为 `PDFJS` 对象的 promise 的自定义 `pdfjs` 函数。

在下面的示例中，我们使用“旧版”（请参阅[pdfjs文档](https://github.com/mozilla/pdf.js/wiki/Frequently-Asked-Questions#which-browsersenvironments-are-supported))，该构建包括默认构建中未包含的几个 polyfill。

```bash npm2yarn
npm install pdfjs-dist

```


```typescript

import { PDFLoader } from "langchain/document_loaders/fs/pdf";



const loader = new PDFLoader("src/document_loaders/example_data/example.pdf", {

  // you may need to add `.then(m => m.default)` to the end of the import

  pdfjs: () => import("pdfjs-dist/legacy/build/pdf.js"),

});

```

