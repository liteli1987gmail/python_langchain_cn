# NebulaGraphQAChain

This notebook shows how to use LLMs to provide a natural language interface to NebulaGraph database.

You will need to have a running NebulaGraph cluster, for which you can run a containerized cluster by running the following script:

```bash
curl -fsSL nebula-up.siwei.io/install.sh | bash
```

Other options are:
- Install as a [Docker Desktop Extension](https://www.docker.com/blog/distributed-cloud-native-graph-database-nebulagraph-docker-extension/). See [here](https://docs.nebula-graph.io/3.5.0/2.quick-start/1.quick-start-workflow/)
- NebulaGraph Cloud Service. See [here](https://www.nebula-graph.io/cloud)
- Deploy from package, source code, or via Kubernetes. See [here](https://docs.nebula-graph.io/)

Once the cluster is running, we could create the SPACE and SCHEMA for the database.


```python
%pip install ipython-ngql
%load_ext ngql

# connect ngql jupyter extension to nebulagraph
%ngql --address 127.0.0.1 --port 9669 --user root --password nebula
# create a new space
%ngql CREATE SPACE IF NOT EXISTS langchain(partition_num=1, replica_factor=1, vid_type=fixed_string(128));
```


```python
# Wait for a few seconds for the space to be created.
%ngql USE langchain;
```

Create the schema, for full dataset, refer [here](https://www.siwei.io/en/nebulagraph-etl-dbt/).


```python
%%ngql
CREATE TAG IF NOT EXISTS movie(name string);
CREATE TAG IF NOT EXISTS person(name string, birthdate string);
CREATE EDGE IF NOT EXISTS acted_in();
CREATE TAG INDEX IF NOT EXISTS person_index ON person(name(128));
CREATE TAG INDEX IF NOT EXISTS movie_index ON movie(name(128));
```

Wait for schema creation to complete, then we can insert some data.


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

## Refresh graph schema information

If the schema of database changes, you can refresh the schema information needed to generate nGQL statements.


```python
# graph.refresh_schema()
```


```python
print(graph.get_schema)
```

    Node properties: [{'tag': 'movie', 'properties': [('name', 'string')]}, {'tag': 'person', 'properties': [('name', 'string'), ('birthdate', 'string')]}]
    Edge properties: [{'edge': 'acted_in', 'properties': []}]
    Relationships: ['(:person)-[:acted_in]->(:movie)']
    
    

## Querying the graph

We can now use the graph cypher QA chain to ask question of the graph


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


