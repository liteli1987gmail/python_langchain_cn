 # 文档

语言模型只知道它们所训练的内容的信息。为了让它们能够回答问题或总结其他信息，你需要将信息传递给语言模型。因此，拥有文档的概念非常重要。

文档本质上非常简单。它由一段文本和可选的元数据组成。文本是我们与语言模型交互的部分，而可选的元数据对于跟踪文档的元数据（例如来源)非常有用。

```typescript
interface Document {

  pageContent: string;

  metadata: Record<string, any>;

}

```


## 创建文档

你可以在LangChain中很容易地创建一个文档对象与 

```typescript
import { Document } from "langchain/document";



const doc = new Document({ pageContent: "foo" });

```


你可以使用 创建带有元数据的文档

```typescript
import { Document } from "langchain/document";



const doc = new Document({ pageContent: "foo", metadata: { source: "1" } });

```


同时还可以查看[文档加载器（Document Loaders）](../indexes/document_loaders/)，以了解从各种来源加载文档的方法。

