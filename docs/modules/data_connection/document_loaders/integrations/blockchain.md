# Blockchain
## 概述
这个笔记本的目的是为Langchain区块文档加载器的功能进行测试提供一种方式。
最初，此加载器支持以下功能：
* 从NFT智能合约（ERC721和ERC1155）加载NFT作为文档
* 以太坊主网、以太坊测试网、Polygon主网、Polygon测试网（默认值为eth-mainnet）
* Alchemy的getNFTsForCollection API

如果社区发现此加载器有价值，可以进行扩展。具体来说，可以添加其他API（例如与交易相关的API）。
此文档加载器需要：
* 免费的[Alchemy API Key](https://www.alchemy.com/)

输入采用以下格式：
- pageContent= Individual NFT
- metadata={'source': '0x1a92f7381b9f03921564a437210bb9396471050c', 'blockchain': 'eth-mainnet', 'tokenId': '0x15'})

## 将NFT加载到文档加载器
```python
# 从 https://www.alchemy.com/ 获取 ALCHEMY_API_KEY
alchemyApiKey = "..."
```

### 选项1：以太坊主网（默认BlockchainType）
```python
from langchain.document_loaders.blockchain import (
    BlockchainDocumentLoader,
    BlockchainType,
)

contractAddress = "0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d"  # Bored Ape Yacht Club 合约地址
blockchainType = BlockchainType.ETH_MAINNET  # 默认值，可选参数
blockchainLoader = BlockchainDocumentLoader(
    contract_address=contractAddress, api_key=alchemyApiKey
)

nfts = blockchainLoader.load()

nfts[:2]
```

### 选项2：Polygon主网
```python
contractAddress = (
    "0x448676ffCd0aDf2D85C1f0565e8dde6924A9A7D9"  # Polygon主网合约地址
)

blockchainType = BlockchainType.POLYGON_MAINNET

blockchainLoader = BlockchainDocumentLoader(
    contract_address=contractAddress,
    blockchainType=blockchainType,
    api_key=alchemyApiKey,
)

nfts = blockchainLoader.load()

nfts[:2]
```