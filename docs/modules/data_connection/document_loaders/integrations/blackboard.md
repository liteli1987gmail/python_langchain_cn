# Blackboard

[Blackboard Learn](https://en.wikipedia.org/wiki/Blackboard_Learn)（之前称为 Blackboard Learning Management System）是一种基于网络的虚拟学习环境和学习管理系统，由Blackboard Inc.开发。该软件具有课程管理、可定制的开放架构和可扩展的设计，可以与学生信息系统和身份验证协议集成。它可以安装在本地服务器上，由`Blackboard ASP Solutions`提供托管，也可以作为托管在Amazon Web Services上的软件即服务提供。其主要目的是将在线元素添加到传统面对面课程中，并开发几乎没有面对面会议的完全在线课程。

本文介绍了如何从[Blackboard Learn](https://www.anthology.com/products/teaching-and-learning/learning-effectiveness/blackboard-learn)实例加载数据。

此加载器与所有`Blackboard`课程不兼容。它只能与使用新的`Blackboard`界面的课程兼容。
要使用此加载器，您必须拥有BbRouter cookie。您可以通过登录课程，然后从浏览器的开发者工具中复制BbRouter cookie的值来获取此cookie。

```python
from langchain.document_loaders import BlackboardLoader

loader = BlackboardLoader(
    blackboard_course_url="https://blackboard.example.com/webapps/blackboard/execute/announcement?method=search&context=course_entry&course_id=_123456_1",
    bbrouter="expires:12345...",
    load_all_recursively=True,
)
documents = loader.load()
```