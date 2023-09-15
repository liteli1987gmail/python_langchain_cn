# Blockchain

## Overview

The intention of this notebook is to provide a means of testing functionality in the Langchain Document Loader for Blockchain.

Initially this Loader supports:

*   Loading NFTs as Documents from NFT Smart Contracts (ERC721 and ERC1155)
*   Ethereum Mainnnet, Ethereum Testnet, Polygon Mainnet, Polygon Testnet (default is eth-mainnet)
*   Alchemy's getNFTsForCollection API

It can be extended if the community finds value in this loader.  Specifically:

*   Additional APIs can be added (e.g. Tranction-related APIs)

This Document Loader Requires:

*   A free [Alchemy API Key](https://www.alchemy.com/)

The output takes the following format:

- pageContent= Individual NFT
- metadata={'source': '0x1a92f7381b9f03921564a437210bb9396471050c', 'blockchain': 'eth-mainnet', 'tokenId': '0x15'})

## Load NFTs into Document Loader


```python
# get ALCHEMY_API_KEY from https://www.alchemy.com/

alchemyApiKey = "..."
```

### Option 1: Ethereum Mainnet (default BlockchainType)


```python
from langchain.document_loaders.blockchain import (
    BlockchainDocumentLoader,
    BlockchainType,
)

contractAddress = "0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d"  # Bored Ape Yacht Club contract address

blockchainType = BlockchainType.ETH_MAINNET  # default value, optional parameter

blockchainLoader = BlockchainDocumentLoader(
    contract_address=contractAddress, api_key=alchemyApiKey
)

nfts = blockchainLoader.load()

nfts[:2]
```

### Option 2: Polygon Mainnet


```python
contractAddress = (
    "0x448676ffCd0aDf2D85C1f0565e8dde6924A9A7D9"  # Polygon Mainnet contract address
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
