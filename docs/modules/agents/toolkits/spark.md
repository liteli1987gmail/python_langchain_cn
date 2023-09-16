# Spark Dataframe 代理

本笔记本展示了如何使用代理与 Spark dataframe 和 Spark Connect 进行交互。它主要针对问题回答进行了优化。

**注意：此代理在底层调用了 Python 代理，该代理执行由 LLM 生成的 Python 代码 - 如果 LLM 生成的 Python 代码有害的话，这可能是不好的。请谨慎使用。**


```python
import os

os.environ["OPENAI_API_KEY"] = "...input your openai api key here..."
```


```python
from langchain.llms import OpenAI
from pyspark.sql import SparkSession
from langchain.agents import create_spark_dataframe_agent

spark = SparkSession.builder.getOrCreate()
csv_file_path = "titanic.csv"
df = spark.read.csv(csv_file_path, header=True, inferSchema=True)
df.show()
```

    23/05/15 20:33:10 WARN Utils: Your hostname, Mikes-Mac-mini.local resolves to a loopback address: 127.0.0.1; using 192.168.68.115 instead (on interface en1)
    23/05/15 20:33:10 WARN Utils: Set SPARK_LOCAL_IP if you need to bind to another address
    Setting default log level to "WARN".
    To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
    23/05/15 20:33:10 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
    

    +-----------+--------+------+--------------------+------+----+-----+-----+----------------+-------+-----+--------+
    |PassengerId|Survived|Pclass|                Name|   Sex| Age|SibSp|Parch|          Ticket|   Fare|Cabin|Embarked|
    +-----------+--------+------+--------------------+------+----+-----+-----+----------------+-------+-----+--------+
    |          1|       0|     3|Braund, Mr. Owen ...|  male|22.0|    1|    0|       A/5 21171|   7.25| null|       S|
    |          2|       1|     1|Cumings, Mrs. Joh...|female|38.0|    1|    0|        PC 17599|71.2833|  C85|       C|
    |          3|       1|     3|Heikkinen, Miss. ...|female|26.0|    0|    0|STON/O2. 3101282|  7.925| null|       S|
    |          4|       1|     1|Futrelle, Mrs. Ja...|female|35.0|    1|    0|          113803|   53.1| C123|       S|
    |          5|       0|     3|Allen, Mr. Willia...|  male|35.0|    0|    0|          373450|   8.05| null|       S|
    |          6|       0|     3|    Moran, Mr. James|  male|null|    0|    0|          330877| 8.4583| null|       Q|
    |          7|       0|     1|McCarthy, Mr. Tim...|  male|54.0|    0|    0|           17463|51.8625|  E46|       S|
    |          8|       0|     3|Palsson, Master. ...|  male| 2.0|    3|    1|          349909| 21.075| null|       S|
    |          9|       1|     3|Johnson, Mrs. Osc...|female|27.0|    0|    2|          347742|11.1333| null|       S|
    |         10|       1|     2|Nasser, Mrs. Nich...|female|14.0|    1|    0|          237736|30.0708| null|       C|
    |         11|       1|     3|Sandstrom, Miss. ...|female| 4.0|    1|    1|         PP 9549|   16.7|   G6|       S|
    |         12|       1|     1|Bonnell, Miss. El...|female|58.0|    0|    0|          113783|  26.55| C103|       S|
    |         13|       0|     3|Saundercock, Mr. ...|  male|20.0|    0|    0|       A/5. 2151|   8.05| null|       S|
    |         14|       0|     3|Andersson, Mr. An...|  male|39.0|    1|    5|          347082| 31.275| null|       S|
    |         15|       0|     3|Vestrom, Miss. Hu...|female|14.0|    0|    0|          350406| 7.8542| null|       S|
    |         16|       1|     2|Hewlett, Mrs. (Ma...|female|55.0|    0|    0|          248706|   16.0| null|       S|
    |         17|       0|     3|Rice, Master. Eugene|  male| 2.0|    4|    1|          382652| 29.125| null|       Q|
    |         18|       1|     2|Williams, Mr. Cha...|  male|null|    0|    0|          244373|   13.0| null|       S|
    |         19|       0|     3|Vander Planke, Mr...|female|31.0|    1|    0|          345763|   18.0| null|       S|
    |         20|       1|     3|Masselmani, Mrs. ...|female|null|    0|    0|            2649|  7.225| null|       C|
    +-----------+--------+------+--------------------+------+----+-----+-----+----------------+-------+-----+--------+
    only showing top 20 rows
    
    


```python
agent = create_spark_dataframe_agent(llm=OpenAI(temperature=0), df=df, verbose=True)
```


```python
agent.run("how many rows are there?")
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3mThought: I need to find out how many rows are in the dataframe
    Action: python_repl_ast
    Action Input: df.count()[0m
    Observation: [36;1m[1;3m891[0m
    Thought:[32;1m[1;3m I now know the final answer
    Final Answer: There are 891 rows in the dataframe.[0m
    
    [1m> Finished chain.[0m
    




    'There are 891 rows in the dataframe.'




```python
agent.run("how many people have more than 3 siblings")
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3mThought: I need to find out how many people have more than 3 siblings
    Action: python_repl_ast
    Action Input: df.filter(df.SibSp > 3).count()[0m
    Observation: [36;1m[1;3m30[0m
    Thought:[32;1m[1;3m I now know the final answer
    Final Answer: 30 people have more than 3 siblings.[0m
    
    [1m> Finished chain.[0m
    




    '30 people have more than 3 siblings.'




```python
agent.run("whats the square root of the average age?")
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3mThought: I need to get the average age first
    Action: python_repl_ast
    Action Input: df.agg({"Age": "mean"}).collect()[0][0][0m
    Observation: [36;1m[1;3m29.69911764705882[0m
    Thought:[32;1m[1;3m I now have the average age, I need to get the square root
    Action: python_repl_ast
    Action Input: math.sqrt(29.69911764705882)[0m
    Observation: [36;1m[1;3mname 'math' is not defined[0m
    Thought:[32;1m[1;3m I need to import math first
    Action: python_repl_ast
    Action Input: import math[0m
    Observation: [36;1m[1;3m[0m
    Thought:[32;1m[1;3m I now have the math library imported, I can get the square root
    Action: python_repl_ast
    Action Input: math.sqrt(29.69911764705882)[0m
    Observation: [36;1m[1;3m5.449689683556195[0m
    Thought:[32;1m[1;3m I now know the final answer
    Final Answer: 5.449689683556195[0m
    
    [1m> Finished chain.[0m
    




    '5.449689683556195'




```python
spark.stop()
```

## Spark Connect Example


```python
# in apache-spark root directory. (tested here with "spark-3.4.0-bin-hadoop3 and later")
# To launch Spark with support for Spark Connect sessions, run the start-connect-server.sh script.
!./sbin/start-connect-server.sh --packages org.apache.spark:spark-connect_2.12:3.4.0
```


```python
from pyspark.sql import SparkSession

# Now that the Spark server is running, we can connect to it remotely using Spark Connect. We do this by
# creating a remote Spark session on the client where our application runs. Before we can do that, we need
# to make sure to stop the existing regular Spark session because it cannot coexist with the remote
# Spark Connect session we are about to create.
SparkSession.builder.master("local[*]").getOrCreate().stop()
```

    23/05/08 10:06:09 WARN Utils: Service 'SparkUI' could not bind on port 4040. Attempting port 4041.
    


```python
# The command we used above to launch the server configured Spark to run as localhost:15002.
# So now we can create a remote Spark session on the client using the following command.
spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
```


```python
csv_file_path = "titanic.csv"
df = spark.read.csv(csv_file_path, header=True, inferSchema=True)
df.show()
```

    +-----------+--------+------+--------------------+------+----+-----+-----+----------------+-------+-----+--------+
    |PassengerId|Survived|Pclass|                Name|   Sex| Age|SibSp|Parch|          Ticket|   Fare|Cabin|Embarked|
    +-----------+--------+------+--------------------+------+----+-----+-----+----------------+-------+-----+--------+
    |          1|       0|     3|Braund, Mr. Owen ...|  male|22.0|    1|    0|       A/5 21171|   7.25| null|       S|
    |          2|       1|     1|Cumings, Mrs. Joh...|female|38.0|    1|    0|        PC 17599|71.2833|  C85|       C|
    |          3|       1|     3|Heikkinen, Miss. ...|female|26.0|    0|    0|STON/O2. 3101282|  7.925| null|       S|
    |          4|       1|     1|Futrelle, Mrs. Ja...|female|35.0|    1|    0|          113803|   53.1| C123|       S|
    |          5|       0|     3|Allen, Mr. Willia...|  male|35.0|    0|    0|          373450|   8.05| null|       S|
    |          6|       0|     3|    Moran, Mr. James|  male|null|    0|    0|          330877| 8.4583| null|       Q|
    |          7|       0|     1|McCarthy, Mr. Tim...|  male|54.0|    0|    0|           17463|51.8625|  E46|       S|
    |          8|       0|     3|Palsson, Master. ...|  male| 2.0|    3|    1|          349909| 21.075| null|       S|
    |          9|       1|     3|Johnson, Mrs. Osc...|female|27.0|    0|    2|          347742|11.1333| null|       S|
    |         10|       1|     2|Nasser, Mrs. Nich...|female|14.0|    1|    0|          237736|30.0708| null|       C|
    |         11|       1|     3|Sandstrom, Miss. ...|female| 4.0|    1|    1|         PP 9549|   16.7|   G6|       S|
    |         12|       1|     1|Bonnell, Miss. El...|female|58.0|    0|    0|          113783|  26.55| C103|       S|
    |         13|       0|     3|Saundercock, Mr. ...|  male|20.0|    0|    0|       A/5. 2151|   8.05| null|       S|
    |         14|       0|     3|Andersson, Mr. An...|  male|39.0|    1|    5|          347082| 31.275| null|       S|
    |         15|       0|     3|Vestrom, Miss. Hu...|female|14.0|    0|    0|          350406| 7.8542| null|       S|
    |         16|       1|     2|Hewlett, Mrs. (Ma...|female|55.0|    0|    0|          248706|   16.0| null|       S|
    |         17|       0|     3|Rice, Master. Eugene|  male| 2.0|    4|    1|          382652| 29.125| null|       Q|
    |         18|       1|     2|Williams, Mr. Cha...|  male|null|    0|    0|          244373|   13.0| null|       S|
    |         19|       0|     3|Vander Planke, Mr...|female|31.0|    1|    0|          345763|   18.0| null|       S|
    |         20|       1|     3|Masselmani, Mrs. ...|female|null|    0|    0|            2649|  7.225| null|       C|
    +-----------+--------+------+--------------------+------+----+-----+-----+----------------+-------+-----+--------+
    only showing top 20 rows
    
    


```python
from langchain.agents import create_spark_dataframe_agent
from langchain.llms import OpenAI
import os

os.environ["OPENAI_API_KEY"] = "...input your openai api key here..."

agent = create_spark_dataframe_agent(llm=OpenAI(temperature=0), df=df, verbose=True)
```


```python
agent.run(
    """
who bought the most expensive ticket?
You can find all supported function types in https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/dataframe.html
"""
)
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3m
    Thought: I need to find the row with the highest fare
    Action: python_repl_ast
    Action Input: df.sort(df.Fare.desc()).first()[0m
    Observation: [36;1m[1;3mRow(PassengerId=259, Survived=1, Pclass=1, Name='Ward, Miss. Anna', Sex='female', Age=35.0, SibSp=0, Parch=0, Ticket='PC 17755', Fare=512.3292, Cabin=None, Embarked='C')[0m
    Thought:[32;1m[1;3m I now know the name of the person who bought the most expensive ticket
    Final Answer: Miss. Anna Ward[0m
    
    [1m> Finished chain.[0m
    




    'Miss. Anna Ward'




```python
spark.stop()
```
