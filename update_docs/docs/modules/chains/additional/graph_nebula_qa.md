# NebulaGraphQAChain

本笔记本展示了如何使用语言模型为NebulaGraph数据库提供自然语言接口。

您需要运行一个NebulaGraph集群，可以通过运行以下脚本来运行一个容器化集群：

```bash
curl -fsSL nebula-up.siwei.io/install.sh | bash
```

其他选项包括：

- 作为[Docker桌面扩展](https://www.docker.com/blog/distributed-cloud-native-graph-database-nebulagraph-docker-extension/)安装。请参阅[这里](https://docs.nebula-graph.io/3.5.0/2.quick-start/1.quick-start-workflow/)
- NebulaGraph云服务。请参阅[这里](https://www.nebula-graph.io/cloud)
- 通过软件包、源代码或Kubernetes部署。请参阅[这里](https://docs.nebula-graph.io/)

集群运行后，我们可以为数据库创建SPACE和SCHEMA。

```python
%pip install ipython-ngql
%load_ext ngql

# 连接 ngql jupyter 扩展到 nebulagraph
%ngql --address 127.0.0.1 --port 9669 --user root --password nebula

# 创建一个新的space
%ngql CREATE SPACE IF NOT EXISTS langchain(partition_num=1, replica_factor=1, vid_type=fixed_string(128));
```

稍等几秒钟，等待space创建完成。

创建schema，完整数据集请参阅[这里](https://www.siwei.io/en/nebulagraph-etl-dbt/)。

```python
%%ngql
CREATE TAG IF NOT EXISTS movie(name string);
CREATE TAG IF NOT EXISTS person(name string, birthdate string);
CREATE EDGE IF NOT EXISTS acted_in();
CREATE TAG INDEX IF NOT EXISTS person_index ON person(name(128));
CREATE TAG INDEX IF NOT EXISTS movie_index ON movie(name(128));
```

等待schema创建完成后，我们可以插入一些数据。

```python
%%ngql
INSERT VERTEX person(name, birthdate) VALUES "Al Pacino":("Al Pacino", "1940-04-25");
INSERT VERTEX movie(name) VALUES "The Godfather II":("The Godfather II");
INSERT VERTEX movie(name) VALUES "The Godfather Coda: The Death of Michael Corleone":("The Godfather Coda: The Death of Michael Corleone");
INSERT EDGE acted_in() VALUES "Al Pacino"->"The Godfather II":();
INSERT EDGE acted_in() VALUES "Al Pacino"->"The Godfather Coda: The Death of Michael Corleone":();
```

UsageError: Cell magic `%%ngql` not found.

```python
from langchain.chat_models import ChatOpenAI
from langchain.chains import NebulaGraphQAChain
from langchain.graphs import NebulaGraph
```

```python
graph = NebulaGraph(
    space="langchain",
    username="root",
    password="nebula",
    address="127.0.0.1",
    port=9669,
    session_pool_size=30,
)
```

## 刷新图谱架构信息

如果数据库的架构发生变化，您可以刷新生成nGQL语句所需的架构信息。

```python
# graph.refresh_schema()
```

```python
print(graph.get_schema)
```

    Node properties: [{'tag': 'movie', 'properties': [('name', 'string')]}, {'tag': 'person', 'properties': [('name', 'string'), ('birthdate', 'string')]}]
    Edge properties: [{'edge': 'acted_in', 'properties': []}]
    Relationships: ['(:person)-[:acted_in]->(:movie)']


## 查询图谱

我们现在可以使用图谱cypher QA链来询问图谱问题。

```python
chain = NebulaGraphQAChain.from_llm(
    ChatOpenAI(temperature=0), graph=graph, verbose=True
)
```

```python
chain.run("Who played in The Godfather II?")
```

    
    
    [1m> Entering new NebulaGraphQAChain chain...[0m
    Generated nGQL:
    [32;1m[1;3mMATCH (p:`person`)-[:acted_in]->(m:`movie`) WHERE m.`movie`.`name` == 'The Godfather II'
    RETURN p.`person`.`name`[0m
    Full Context:
    [32;1m[1;3m{'p.person.name': ['Al Pacino']}[0m
    [1m> Finished chain.[0m
    




    'Al Pacino played in The Godfather II.'


