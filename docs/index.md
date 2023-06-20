# 欢迎使用LangChain

![LangChain](https://pica.zhimg.com/50/v2-56e8bbb52aa271012541c1fe1ceb11a2_r.gif 'LangChain中文网')

LangChain是一种基于语言模型的应用程序开发框架。我们相信，最强大和不同的应用程序不仅会通过API调用语言模型，还会:


- _了解数据_: 连接语言模型与其他数据源
- _有代理_: 允许语言模型与其环境交互


LangChain框架是根据上述原则设计的。


## 入门


查看下面的指南，了解如何使用LangChain创建语言模型应用程序。


- [快速入门](./getting-started/guide-llm.mdx)使用LLMs
- [快速入门](./getting-started/guide-chat.mdx)使用聊天模型


## 组件


LangChain提供支持的几个主要模块。针对每个模块，我们提供一些示例，以便开始并熟悉一些概念。每个示例都链接到使用的模块的API文档。


这些模块按递增的复杂性排列#


- [模式](./modules/schema/): 这包括在整个库中使用的接口和基类。


- [模型](./modules/models/): 这包括与各种LLM，聊天模型和嵌入模型的集成。


- [提示符](./modules/prompts/): 这包括提示符模板和与提示符一起使用的功能，例如输出解析器和示例选择器。


- [索引](./modules/indexes/): 这包括用于处理您自己的数据的模式和功能，并使其准备好与语言模型交互（包括文档加载程序、向量存储器、文本分割器和检索器)。


- [Memory](./modules/memory/): 内存是指链/代理调用之间保存状态的概念。LangChain提供标准的内存接口，一个内存实现的集合，以及使用内存的链/代理的示例。


- [Chains](./modules/chains/): 链不仅仅只是单个LLM调用，它是一系列调用（不论是对LLM还是其他工具)。LangChain提供标准的链接口，与其他工具进行多样化的集成，并提供常见应用的端到端链。


- [Agents](./modules/agents/): 代理涉及LLM对要采取的行动做出决策，采取行动，看到观察结果，然后重复该过程直到完成。LangChain提供代理标准接口，提供一系列代理供选择以及端到端代理示例。


## API 参考


[这里](./api/) 可以找到LangChain所有模块的API参考以及所有导出类和函数的完整文档。


## 生产


当您从原型制作过渡到生产过程时，我们正在开发资源来帮助您完成此过程。
These including:



- [部署](./production/deployment): 关于如何将应用程序部署到生产环境的资源。
- [事件/回调](./production/callbacks): LangChain模块公开的事件资源。
- [跟踪](./production/tracing): 有关如何使用跟踪记录和调试应用程序的资源。


## 附加资源

以下是我们认为在开发应用程序时可能有用的其他资源收集！

- [LangChainHub](https://github.com/hwchase17/langchain-hub): LangChainHub 是一个分享和探索其他语言链和代理的地方。

- [Discord](https://discord.gg/6adMQxSpJS): 加入我们的 Discord，讨论关于 LangChain 的一切！

- [生产支持](https://forms.gle/57d8AmXBYp8PP8tZA): 当您将 LangChain 移入生产环境时，我们很乐意提供更全面的支持。请填写此表单，我们将为您设置专用的支持 Slack 频道。

