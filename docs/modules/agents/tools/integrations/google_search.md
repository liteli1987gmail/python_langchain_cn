# Google Search

This notebook goes over how to use the google search component.

First, you need to set up the proper API keys and environment variables. To set it up, create the GOOGLE_API_KEY in the Google Cloud credential console (https://console.cloud.google.com/apis/credentials) and a GOOGLE_CSE_ID using the Programmable Search Enginge (https://programmablesearchengine.google.com/controlpanel/create). Next, it is good to follow the instructions found [here](https://stackoverflow.com/questions/37083058/programmatically-searching-google-in-python-using-custom-search).

Then we will need to set some environment variables.


```python
import os

os.environ["GOOGLE_CSE_ID"] = ""
os.environ["GOOGLE_API_KEY"] = ""
```


```python
from langchain.tools import Tool
from langchain.utilities import GoogleSearchAPIWrapper

search = GoogleSearchAPIWrapper()

tool = Tool(
    name="Google Search",
    description="Search Google for recent results.",
    func=search.run,
)
```


```python
tool.run("Obama's first name?")
```




    "STATE OF HAWAII. 1 Child's First Name. (Type or print). 2. Sex. BARACK. 3. This Birth. CERTIFICATE OF LIVE BIRTH. FILE. NUMBER 151 le. lb. Middle Name. Barack Hussein Obama II is an American former politician who served as the 44th president of the United States from 2009 to 2017. A member of the Democratic\xa0... When Barack Obama was elected president in 2008, he became the first African American to hold ... The Middle East remained a key foreign policy challenge. Jan 19, 2017 ... Jordan Barack Treasure, New York City, born in 2008 ... Jordan Barack Treasure made national news when he was the focus of a New York newspaper\xa0... Portrait of George Washington, the 1st President of the United States ... Portrait of Barack Obama, the 44th President of the United States\xa0... His full name is Barack Hussein Obama II. Since the “II” is simply because he was named for his father, his last name is Obama. Mar 22, 2008 ... Barry Obama decided that he didn't like his nickname. A few of his friends at Occidental College had already begun to call him Barack (his\xa0... Aug 18, 2017 ... It took him several seconds and multiple clues to remember former President Barack Obama's first name. Miller knew that every answer had to\xa0... Feb 9, 2015 ... Michael Jordan misspelled Barack Obama's first name on 50th-birthday gift ... Knowing Obama is a Chicagoan and huge basketball fan,\xa0... 4 days ago ... Barack Obama, in full Barack Hussein Obama II, (born August 4, 1961, Honolulu, Hawaii, U.S.), 44th president of the United States (2009–17) and\xa0..."



## Number of Results
You can use the `k` parameter to set the number of results


```python
search = GoogleSearchAPIWrapper(k=1)

tool = Tool(
    name="I'm Feeling Lucky",
    description="Search Google and return the first result.",
    func=search.run,
)
```


```python
tool.run("python")
```




    'The official home of the Python Programming Language.'



'The official home of the Python Programming Language.'

## Metadata Results

Run query through GoogleSearch and return snippet, title, and link metadata.

- Snippet: The description of the result.
- Title: The title of the result.
- Link: The link to the result.


```python
search = GoogleSearchAPIWrapper()


def top5_results(query):
    return search.results(query, 5)


tool = Tool(
    name="Google Search Snippets",
    description="Search Google for recent results.",
    func=top5_results,
)
```


```python

```
