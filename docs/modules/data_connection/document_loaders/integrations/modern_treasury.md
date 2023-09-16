# Modern Treasury

[Modern Treasury](https://www.moderntreasury.com/)简化了复杂的支付操作。它是一个统一的平台，用于支持移动资金的产品和流程。

- 连接银行和支付系统
- 实时跟踪交易和余额
- 自动化规模化的支付操作

本笔记本介绍了如何从`Modern Treasury REST API`加载数据，并将其转换为LangChain可以接受的格式，以及矢量化的示例用法。

```python
import os

from langchain.document_loaders import ModernTreasuryLoader
from langchain.indexes import VectorstoreIndexCreator
```

Modern Treasury API 需要组织ID和API密钥，可以在Modern Treasury仪表板中的开发者设置中找到。

此文档加载程序还需要一个`resource`选项，用于定义要加载的数据。

以下资源可用：

- `payment_orders` [文档](https://docs.moderntreasury.com/reference/payment-order-object)
- `expected_payments` [文档](https://docs.moderntreasury.com/reference/expected-payment-object)
- `returns` [文档](https://docs.moderntreasury.com/reference/return-object)
- `incoming_payment_details` [文档](https://docs.moderntreasury.com/reference/incoming-payment-detail-object)
- `counterparties` [文档](https://docs.moderntreasury.com/reference/counterparty-object)
- `internal_accounts` [文档](https://docs.moderntreasury.com/reference/internal-account-object)
- `external_accounts` [文档](https://docs.moderntreasury.com/reference/external-account-object)
- `transactions` [文档](https://docs.moderntreasury.com/reference/transaction-object)
- `ledgers` [文档](https://docs.moderntreasury.com/reference/ledger-object)
- `ledger_accounts` [文档](https://docs.moderntreasury.com/reference/ledger-account-object)
- `ledger_transactions` [文档](https://docs.moderntreasury.com/reference/ledger-transaction-object)
- `events` [文档](https://docs.moderntreasury.com/reference/events)
- `invoices` [文档](https://docs.moderntreasury.com/reference/invoices)

```python
modern_treasury_loader = ModernTreasuryLoader("payment_orders")
```

```python
# 从加载程序创建矢量图检索器
# 有关更多详细信息，请参见 https://python.langchain.com/en/latest/modules/data_connection/getting_started.html

index = VectorstoreIndexCreator().from_loaders([modern_treasury_loader])
modern_treasury_doc_retriever = index.vectorstore.as_retriever()
```
