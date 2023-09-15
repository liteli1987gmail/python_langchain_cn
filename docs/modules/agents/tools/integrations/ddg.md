# DuckDuckGo Search

This notebook goes over how to use the duck-duck-go search component.


```python
# !pip install duckduckgo-search
```


```python
from langchain.tools import DuckDuckGoSearchRun
```


```python
search = DuckDuckGoSearchRun()
```


```python
search.run("Obama's first name?")
```




    'Barack Obama, in full Barack Hussein Obama II, (born August 4, 1961, Honolulu, Hawaii, U.S.), 44th president of the United States (2009-17) and the first African American to hold the office. Before winning the presidency, Obama represented Illinois in the U.S. Senate (2005-08). Barack Hussein Obama II (/ b ə ˈ r ɑː k h uː ˈ s eɪ n oʊ ˈ b ɑː m ə / bə-RAHK hoo-SAYN oh-BAH-mə; born August 4, 1961) is an American former politician who served as the 44th president of the United States from 2009 to 2017. A member of the Democratic Party, he was the first African-American president of the United States. Obama previously served as a U.S. senator representing ... Barack Obama was the first African American president of the United States (2009-17). He oversaw the recovery of the U.S. economy (from the Great Recession of 2008-09) and the enactment of landmark health care reform (the Patient Protection and Affordable Care Act ). In 2009 he was awarded the Nobel Peace Prize. His birth certificate lists his first name as Barack: That\'s how Obama has spelled his name throughout his life. His name derives from a Hebrew name which means "lightning.". The Hebrew word has been transliterated into English in various spellings, including Barak, Buraq, Burack, and Barack. Most common names of U.S. presidents 1789-2021. Published by. Aaron O\'Neill , Jun 21, 2022. The most common first name for a U.S. president is James, followed by John and then William. Six U.S ...'


