# 阿里云开放搜索 opensearch

[阿里巴巴云开放搜索](https://www.alibabacloud.com/product/opensearch) （Alibaba Cloud OpenSearch）是一个全方位的智能搜索服务开发平台。OpenSearch 是在阿里巴巴开发的大规模分布式搜索引擎的基础上构建而成，服务于阿里巴巴集团的 500 多个业务场景以及数千个阿里云客户。OpenSearch 帮助企业在不同的搜索场景下开发智能搜索服务，包括电商、O2O、多媒体、内容行业、社区和论坛以及企业的大数据查询。

OpenSearch 帮助您开发高品质、无需维护以及高性能的智能搜索服务，为用户提供高效准确的搜索体验。

OpenSearch 提供向量搜索功能。在特定的场景下，尤其是测试题搜索和图像搜索场景下，您可以结合多模态搜索功能一起使用向量搜索功能来提高搜索结果的准确性。本主题将描述向量索引的语法和使用说明。

## 购买实例并进行配置

- 在 [阿里云](https://opensearch.console.aliyun.com) 购买 OpenSearch 向量搜索版并根据 [文档](https://help.aliyun.com/document_detail/463198.html?spm=a2c4g.465092.0.0.2cd15002hdwavO) 进行实例配置。
  
## 阿里巴巴云开放搜索向量存储包装器

支持以下函数：

- `add_texts`
- `add_documents`
- `from_texts`
- `from_documents`
- `similarity_search`
- `asimilarity_search`
- `similarity_search_by_vector`
- `asimilarity_search_by_vector`
- `similarity_search_with_relevance_scores`

有关阿里巴巴云开放搜索包装器的更详细演示，请参见[此笔记本](../modules/indexes/vectorstores/examples/alibabacloud_opensearch.ipynb)

如果您在使用过程中遇到任何问题，请随时联系 [xingshaomin.xsm@alibaba-inc.com](xingshaomin.xsm@alibaba-inc.com) 我们将尽最大努力为您提供帮助和支持。