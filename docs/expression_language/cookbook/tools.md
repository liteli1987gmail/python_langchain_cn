# 使用工具

您可以轻松地使用任何工具与可运行的代码一起使用。

```python
%pip install --upgrade --quiet  langchain langchain-openai duckduckgo-search
```

```python
from langchain.tools import DuckDuckGoSearchRun
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
```

```python
search = DuckDuckGoSearchRun()
```

```python
template = """将以下用户输入转换为搜索引擎的搜索查询：

{input}"""
prompt = ChatPromptTemplate.from_template(template)

model = ChatOpenAI()
```

```python
chain = prompt | model | StrOutputParser() | search
```

```python
chain.invoke({"input": "我想弄清楚今晚有哪些比赛"})
```

'今天和今晚有哪些体育比赛可以在电视上观看和直播？今天的2023年体育电视节目表包括足球、篮球、棒球、曲棍球、摩托车赛、足球等。在ESPN、FOX、FS1、CBS、NBC、ABC、Peacock、Paramount+、fuboTV、本地频道和许多其他网络上观看电视或在线直播。MLB今晚的比赛：如何在电视上观看、直播和下注-9月7日星期四。西雅图水手队的胡里奥·罗德里格斯在对奥克兰运动家的比赛中得分后在掩蔽所里与队友们打招呼... Circle-乡村音乐和生活方式。您可以获得今天所有MLB比赛的实况报道，以下是提供的信息。雄鹿队将在周三下午12:35在PNC公园对阵海盗队，争取在客场获胜。查看最新的赔率，并使用BetMGM Sportsbook提供的特别优惠代码“GNPLAY”！MLB今晚的比赛：如何在电视上观看、直播和下注-9月5日星期二。休斯顿太空人的凯尔·塔克在对洛杉矶天使队的比赛中击中一个二垒安打后跑向一垒，8月13日星期日，2023年，休斯顿。(AP照片/埃里克·克里斯蒂安·史密斯)(APMedia)休斯顿太空人对阵德克萨斯游骑兵队是其中之一...今晚的大学橄榄球赛程的下半场还有一些精彩的比赛可以在电视上观看。当科罗拉多大学击败TCU时，我们已经看到了一场令人兴奋的比赛。而且我们还看到了一些...'
```