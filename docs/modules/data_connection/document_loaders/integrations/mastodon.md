# Mastodon

>[Mastodon](https://joinmastodon.org/) 是一个联邦式社交媒体和社交网络服务。

该加载器使用 `Mastodon.py` Python 包从一组 `Mastodon` 账户的"toots"中获取文本。

默认情况下，可以查询公共账户而无需进行任何身份验证。如果查询非公共账户或实例，则必须为您的账户注册一个应用程序以获取访问令牌，并设置该令牌和您的账户的 API 基本 URL。

然后，您需要以 `@account@instance` 的格式传入要提取的 Mastodon 账户名称。


```python
from langchain.document_loaders import MastodonTootsLoader
```


```python
#!pip install Mastodon.py
```


```python
loader = MastodonTootsLoader(
    mastodon_accounts=["@Gargron@mastodon.social"],
    number_toots=50,  # 默认值为 100
)
```


或者设置访问信息来使用 Mastodon 应用程序。

请注意，访问令牌可以传递给构造函数，或者您可以设置环境变量 "MASTODON_ACCESS_TOKEN"。


```python
# loader = MastodonTootsLoader(
#     access_token="<MASTODON APP 的访问令牌>",
#     api_base_url="<MASTODON APP 实例的 API 基本 URL>",
#     mastodon_accounts=["@Gargron@mastodon.social"],
#     number_toots=50,  # 默认值为 100
# )
```


```python
documents = loader.load()
for doc in documents[:3]:
    print(doc.page_content)
    print("=" * 80)
```

```

    <p>It is tough to leave this behind and go back to reality. And some people live here! I’m sure there are downsides but it sounds pretty good to me right now.</p>
    ================================================================================
    <p>I wish we could stay here a little longer, but it is time to go home 🥲</p>
    ================================================================================
    <p>Last day of the honeymoon. And it’s <a href="https://mastodon.social/tags/caturday" class="mention hashtag" rel="tag">#<span>caturday</span></a>! This cute tabby came to the restaurant to beg for food and got some chicken.</p>
    ================================================================================
```  

toot 文本（即文档的 `page_content`）默认为 Mastodon API 返回的 HTML 格式。