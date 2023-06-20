---
hide_table_of_contents: true
---

# 向量库

一旦您创建了一个[向量库](../vector_stores/)， ,使用它作为检索器就非常简单:

```typescript

vectorStore = ...

retriever = vectorStore.asRetriever()

```

