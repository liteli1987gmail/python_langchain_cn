# Brave Search

This notebook goes over how to use the Brave Search tool.


```python
from langchain.tools import BraveSearch
```


```python
api_key = "..."
```


```python
tool = BraveSearch.from_api_key(api_key=api_key, search_kwargs={"count": 3})
```


```python
tool.run("obama middle name")
```




    '[{"title": "Barack Obama - Wikipedia", "link": "https://en.wikipedia.org/wiki/Barack_Obama", "snippet": "Outside of politics, <strong>Obama</strong> has published three bestselling books: Dreams from My Father (1995), The Audacity of Hope (2006) and A Promised Land (2020). Rankings by scholars and historians, in which he has been featured since 2010, place him in the <strong>middle</strong> to upper tier of American presidents."}, {"title": "Obama\'s Middle Name -- My Last Name -- is \'Hussein.\' So?", "link": "https://www.cair.com/cair_in_the_news/obamas-middle-name-my-last-name-is-hussein-so/", "snippet": "Many Americans understand that common names don\\u2019t only come in the form of a \\u201cSmith\\u201d or a \\u201cJohnson.\\u201d Perhaps, they have a neighbor, mechanic or teacher named Hussein. Or maybe they\\u2019ve seen fashion designer Hussein Chalayan in the pages of Vogue or recall <strong>King Hussein</strong>, our ally in the Middle East."}, {"title": "What\'s up with Obama\'s middle name? - Quora", "link": "https://www.quora.com/Whats-up-with-Obamas-middle-name", "snippet": "Answer (1 of 15): A better question would be, \\u201cWhat\\u2019s up with Obama\\u2019s first name?\\u201d President <strong>Barack Hussein Obama</strong>\\u2019s father\\u2019s name was <strong>Barack Hussein Obama</strong>. He was named after his father. Hussein, Obama\\u2019s middle name, is a very common Arabic name, meaning &quot;good,&quot; &quot;handsome,&quot; or &quot;beautiful.&quot;"}]'




```python

```
