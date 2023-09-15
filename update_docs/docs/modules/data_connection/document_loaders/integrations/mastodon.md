# Mastodon

>[Mastodon](https://joinmastodon.org/) is a federated social media and social networking service.

This loader fetches the text from the "toots" of a list of `Mastodon` accounts, using the `Mastodon.py` Python package.

Public accounts can the queried by default without any authentication. If non-public accounts or instances are queried, you have to register an application for your account which gets you an access token, and set that token and your account's API base URL.

Then you need to pass in the Mastodon account names you want to extract, in the `@account@instance` format.


```python
from langchain.document_loaders import MastodonTootsLoader
```


```python
#!pip install Mastodon.py
```


```python
loader = MastodonTootsLoader(
    mastodon_accounts=["@Gargron@mastodon.social"],
    number_toots=50,  # Default value is 100
)

# Or set up access information to use a Mastodon app.
# Note that the access token can either be passed into
# constructor or you can set the envirovnment "MASTODON_ACCESS_TOKEN".
# loader = MastodonTootsLoader(
#     access_token="<ACCESS TOKEN OF MASTODON APP>",
#     api_base_url="<API BASE URL OF MASTODON APP INSTANCE>",
#     mastodon_accounts=["@Gargron@mastodon.social"],
#     number_toots=50,  # Default value is 100
# )
```


```python
documents = loader.load()
for doc in documents[:3]:
    print(doc.page_content)
    print("=" * 80)
```

    <p>It is tough to leave this behind and go back to reality. And some people live here! I’m sure there are downsides but it sounds pretty good to me right now.</p>
    ================================================================================
    <p>I wish we could stay here a little longer, but it is time to go home 🥲</p>
    ================================================================================
    <p>Last day of the honeymoon. And it’s <a href="https://mastodon.social/tags/caturday" class="mention hashtag" rel="tag">#<span>caturday</span></a>! This cute tabby came to the restaurant to beg for food and got some chicken.</p>
    ================================================================================
    

The toot texts (the documents' `page_content`) is by default HTML as returned by the Mastodon API.
