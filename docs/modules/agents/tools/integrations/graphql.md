# GraphQL工具
这个Jupyter笔记本演示了如何使用BaseGraphQLTool组件与Agent一起使用。

GraphQL是一个用于API的查询语言，也是执行这些查询的运行时。GraphQL提供了对API中数据的完整和可理解的描述，给客户端提供了请求所需内容的能力，使得随着时间的推移更容易演进API，并提供了强大的开发工具。

通过在提供给Agent的工具列表中包含一个BaseGraphQLTool，您可以授予Agent从GraphQL API查询数据的能力，以满足您的任何需求。

在这个例子中，我们将使用公共的星球大战GraphQL API，该API位于以下端点上：https://swapi-graphql.netlify.app/.netlify/functions/index。

首先，您需要安装httpx和gql Python包。


```python
pip install httpx gql > /dev/null
```

现在，让我们使用指定的星球大战API端点创建一个BaseGraphQLTool实例，并用该工具初始化一个Agent。


```python
from langchain import OpenAI
from langchain.agents import load_tools, initialize_agent, AgentType
from langchain.utilities import GraphQLAPIWrapper

llm = OpenAI(temperature=0)

tools = load_tools(
    ["graphql"],
    graphql_endpoint="https://swapi-graphql.netlify.app/.netlify/functions/index",
    llm=llm,
)

agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)
```

现在，我们可以使用Agent来对星球大战GraphQL API运行查询。让我们要求Agent列出所有的星球大战电影及其发布日期。


```python
graphql_fields = """allFilms {
    films {
      title
      director
      releaseDate
      speciesConnection {
        species {
          name
          classification
          homeworld {
            name
          }
        }
      }
    }
  }

"""

suffix = "在graphql数据库中搜索具有此模式的所有stawars电影的标题"


agent.run(suffix + graphql_fields)
```

    
    
    [1m> 进入新的AgentExecutor链...[0m
    [32;1m[1;3m我需要查询graphql数据库以获取所有星球大战电影的标题
    操作: query_graphql
    操作输入: query { allFilms { films { title } } }[0m
    观察: [36;1m[1;3m"{\n  \"allFilms\": {\n    \"films\": [\n      {\n        \"title\": \"A New Hope\"\n      },\n      {\n        \"title\": \"The Empire Strikes Back\"\n      },\n      {\n        \"title\": \"Return of the Jedi\"\n      },\n      {\n        \"title\": \"The Phantom Menace\"\n      },\n      {\n        \"title\": \"Attack of the Clones\"\n      },\n      {\n        \"title\": \"Revenge of the Sith\"\n      }\n    ]\n  }\n}"[0m
    思考:[32;1m[1;3m现在我知道了所有星球大战电影的标题
    最终答案: 所有星球大战电影的标题是: A New Hope, The Empire Strikes Back, Return of the Jedi, The Phantom Menace, Attack of the Clones和Revenge of the Sith.[0m
    
    [1m> 完成链。[0m
    




    '所有星球大战电影的标题是: A New Hope, The Empire Strikes Back, Return of the Jedi, The Phantom Menace, Attack of the Clones和Revenge of the Sith。'


