# Elasticsearch

介绍如何在Elasticsearch中使用托管的嵌入模型生成嵌入的步骤

使用`ElasticsearchEmebddings`类的最简单方法是
- 使用`from_credentials`构造函数（如果您使用Elastic Cloud）
- 或使用`from_es_connection`构造函数与任何Elasticsearch集群

```python
!pip -q install elasticsearch langchain
```

......

## Testing with `from_credentials`

This required an Elastic Cloud `cloud_id`

```python
# 使用凭据实例化ElasticsearchEmbeddings
embeddings = ElasticsearchEmbeddings.from_credentials(
    model_id,
    es_cloud_id="your_cloud_id",
    es_user="your_user",
    es_password="your_password",
)
```

......

## Testing with Existing Elasticsearch client connection

This can be used with any Elasticsearch deployment

```python
# 创建Elasticsearch连接
es_connection = Elasticsearch(
    hosts=["https://es_cluster_url:port"], basic_auth=("user", "password")
)
```

......
