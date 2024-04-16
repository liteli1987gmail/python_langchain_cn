# 安全

LangChain与各种外部资源（如本地和远程文件系统、API和数据库）有着广泛的集成生态系统。这些集成使开发人员能够创建多功能应用程序，将LLM的强大功能与访问、交互和操作外部资源的能力相结合。

## 最佳实践

在构建此类应用程序时，开发人员应记住遵循良好的安全实践：

* [**限制权限**](https://en.wikipedia.org/wiki/Principle_of_least_privilege)：将权限限定在应用程序的需求范围内。授予广泛或过多的权限可能会引入重大安全漏洞。为避免此类漏洞，考虑使用只读凭据、禁止访问敏感资源、使用沙箱技术（如在容器内运行）等，根据应用程序的需要选择适当的方法。
* **预防潜在的滥用**：正如人类可能会犯错一样，大型语言模型（LLM）也可能会犯错。始终假设任何系统访问或凭据可能会被分配的权限允许的任何方式使用。例如，如果一对数据库凭据允许删除数据，最安全的做法是假设任何能够使用这些凭据的LLM实际上可能会删除数据。
* [**深度防御**](https://en.wikipedia.org/wiki/Defense_in_depth_(computing))：没有完美的安全技术。通过优化和良好的链式设计可以减少大型语言模型（LLM）可能出错的几率，但无法完全消除。最好的做法是结合多层安全方法，而不是依赖于任何单一防御层来确保安全。例如：同时使用只读权限和沙箱技术，以确保LLM只能访问明确为其使用的数据。

不这样做的风险包括但不限于：
* 数据损坏或丢失。
* 未经授权访问机密信息。
* 关键资源的性能或可用性受损。

具有缓解策略的示例场景：

* 用户可能要求具有文件系统访问权限的代理删除不应删除的文件，或读取包含敏感信息的文件内容。为了缓解这个问题，限制代理只能使用特定目录，并且只允许其读取或写入安全的文件。考虑通过在容器中运行代理来进一步隔离代理。
* 用户可能要求具有对外部API的写入访问权限的代理向API写入恶意数据，或从该API删除数据。为了缓解这个问题，给予代理只读的API密钥，或限制其仅使用已经抵御此类滥用的端点。
* 用户可能要求具有对数据库访问权限的代理删除表或更改模式。为了缓解这个问题，将凭据范围限定为代理需要访问的表，并考虑发放只读凭据。

如果您正在构建访问文件系统、API或数据库等外部资源的应用程序，请考虑与公司的安全团队交流，以确定如何设计和保护您的应用程序。

## 报告漏洞

请通过电子邮件将安全漏洞报告给security@langchain.dev。这将确保问题得到及时处理和采取必要的措施。

## 企业解决方案

LangChain可能为具有额外安全要求的客户提供企业解决方案。请通过sales@langchain.dev与我们联系。