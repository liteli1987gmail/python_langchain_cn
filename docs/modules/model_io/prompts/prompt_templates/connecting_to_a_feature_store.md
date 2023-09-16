# 连接特征存储

特征存储是传统机器学习中的一个概念，确保输入模型的数据是最新的且相关的。有关更多信息，请参见[此处](https://www.tecton.ai/blog/what-is-a-feature-store/)。

在考虑将LLM应用程序投入生产时，这个概念非常重要。为了个性化LLM应用程序，您可能希望将LLMs与有关特定用户的最新信息相结合。特征存储可以是保持数据新鲜的好方法，并且LangChain提供了一种将这些数据与LLMs结合的简单方法。

在本笔记本中，我们将展示如何将提示模板与特征存储连接起来。基本思想是在提示模板内部调用特征存储以检索值，然后将其格式化为提示。

## Feast

首先，我们将使用流行的开源特征存储框架[Feast](https://github.com/feast-dev/feast)。

这假设您已经按照入门指南中的步骤运行过了。我们将基于该入门示例，并创建一个LLMChain，用于向特定驱动程序写入关于其最新统计数据的备注。

### 加载 Feast 存储

同样，这应该按照 Feast 自述文件中的说明进行设置。

```python
from feast import FeatureStore

# 根据存储位置更新路径
feast_repo_path = "../../../../../my_feature_repo/feature_repo/"
store = FeatureStore(repo_path=feast_repo_path)
```

### Prompt

在这里，我们将设置一个自定义的 FeastPromptTemplate。这个提示模板将接受一个驱动程序 ID，查找他们的统计数据，并将这些统计数据格式化为提示。

请注意，此提示模板的输入只是`driver_id`，因为那是用户定义的唯一部分（其他所有变量都在提示模板内部查找）。


```python
from langchain.prompts import PromptTemplate, StringPromptTemplate
```


```python
template = """Given the driver's up to date stats, write them note relaying those stats to them.
If they have a conversation rate above .5, give them a compliment. Otherwise, make a silly joke about chickens at the end to make them feel better

Here are the drivers stats:
Conversation rate: {conv_rate}
Acceptance rate: {acc_rate}
Average Daily Trips: {avg_daily_trips}

Your response:"""
prompt = PromptTemplate.from_template(template)
```


```python
class FeastPromptTemplate(StringPromptTemplate):
    def format(self, **kwargs) -> str:
        driver_id = kwargs.pop("driver_id")
        feature_vector = store.get_online_features(
            features=[
                "driver_hourly_stats:conv_rate",
                "driver_hourly_stats:acc_rate",
                "driver_hourly_stats:avg_daily_trips",
            ],
            entity_rows=[{"driver_id": driver_id}],
        ).to_dict()
        kwargs["conv_rate"] = feature_vector["conv_rate"][0]
        kwargs["acc_rate"] = feature_vector["acc_rate"][0]
        kwargs["avg_daily_trips"] = feature_vector["avg_daily_trips"][0]
        return prompt.format(**kwargs)
```


```python
prompt_template = FeastPromptTemplate(input_variables=["driver_id"])
```


```python
print(prompt_template.format(driver_id=1001))
```

    Given the driver's up to date stats, write them note relaying those stats to them.
    If they have a conversation rate above .5, give them a compliment. Otherwise, make a silly joke about chickens at the end to make them feel better
    
    Here are the drivers stats:
    Conversation rate: 0.4745151400566101
    Acceptance rate: 0.055561766028404236
    Average Daily Trips: 936
    
    Your response:
    

### 在链中使用

现在我们可以将其用于链中，成功创建一个由特征存储支持的个性化链。


```python
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
```


```python
chain = LLMChain(llm=ChatOpenAI(), prompt=prompt_template)
```


```python
chain.run(1001)
```




    "Hi there! I wanted to update you on your current stats. Your acceptance rate is 0.055561766028404236 and your average daily trips are 936. While your conversation rate is currently 0.4745151400566101, I have no doubt that with a little extra effort, you'll be able to exceed that .5 mark! Keep up the great work! And remember, even chickens can't always cross the road, but they still give it their best shot."




```python

```

## Tecton

在上面，我们展示了如何将 Feast（一种流行的开源自托管特征存储）与 LangChain 配合使用。下面的示例将展示如何使用 Tecton 进行类似的集成。Tecton 是一个完全托管的特征平台，专为协调完整的 ML 特征生命周期而构建，包括从转换到在线服务的全过程，并提供企业级的 SLA。

### 先决条件

* Tecton 部署（在[https://tecton.ai](https://tecton.ai)上注册）
* `TECTON_API_KEY` 环境变量设置为有效的服务帐户密钥

### 定义和加载特征

我们将使用[Tecton 教程](https://docs.tecton.ai/docs/tutorials/tecton-fundamentals)中的 user_transaction_counts 特征视图作为特征服务的一部分。为简单起见，我们只使用一个特征视图；然而，更复杂的应用程序可能需要更多的特征视图来检索其提示所需的特征。

```python
user_transaction_metrics = FeatureService(
    name = "user_transaction_metrics",
    features = [user_transaction_counts]
)
```

上述特征服务预计将被[应用于实时工作空间](https://docs.tecton.ai/docs/applying-feature-repository-changes-to-a-workspace)。在本示例中，我们将使用"prod"工作空间。

```python
import tecton

workspace = tecton.get_workspace("prod")
feature_service = workspace.get_feature_service("user_transaction_metrics")
```

### Prompts

在这里，我们将设置一个自定义的 TectonPromptTemplate。该提示模板将接受一个 user_id，并查找他们的统计数据，然后将这些统计数据格式化为提示。

请注意，此提示模板的输入只是 `user_id`，因为这是用户定义的唯一部分（所有其他变量都在提示模板内部查找）。

```python
from langchain.prompts import PromptTemplate, StringPromptTemplate
```


```python
template = """Given the vendor's up to date transaction stats, write them a note based on the following rules:

1. If they had a transaction in the last day, write a short congratulations message on their recent sales
2. If no transaction in the last day, but they had a transaction in the last 30 days, playfully encourage them to sell more.
3. Always add a silly joke about chickens at the end

Here are the vendor's stats:
Number of Transactions Last Day: {transaction_count_1d}
Number of Transactions Last 30 Days: {transaction_count_30d}

Your response:"""
prompt = PromptTemplate.from_template(template)
```


```python
class TectonPromptTemplate(StringPromptTemplate):
    def format(self, **kwargs) -> str:
        user_id = kwargs.pop("user_id")
        feature_vector = feature_service.get_online_features(
            join_keys={"user_id": user_id}
        ).to_dict()
        kwargs["transaction_count_1d"] = feature_vector[
            "user_transaction_counts.transaction_count_1d_1d"
        ]
        kwargs["transaction_count_30d"] = feature_vector[
            "user_transaction_counts.transaction_count_30d_1d"
        ]
        return prompt.format(**kwargs)
```


```python
prompt_template = TectonPromptTemplate(input_variables=["user_id"])
```


```python
print(prompt_template.format(user_id="user_469998441571"))
```

    Given the vendor's up to date transaction stats, write them a note based on the following rules:
    
    1. If they had a transaction in the last day, write a short congratulations message on their recent sales
    2. If no transaction in the last day, but they had a transaction in the last 30 days, playfully encourage them to sell more.
    3. Always add a silly joke about chickens at the end
    
    Here are the vendor's stats:
    Number of Transactions Last Day: 657
    Number of Transactions Last 30 Days: 20326
    
    Your response:
    

### 在链中使用

现在我们可以将其用于链中，成功创建一个基于Tecton特征平台支持的个性化链。


```python
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
```


```python
chain = LLMChain(llm=ChatOpenAI(), prompt=prompt_template)
```


```python
chain.run("user_469998441571")
```




    'Wow, congratulations on your recent sales! Your business is really soaring like a chicken on a hot air balloon! Keep up the great work!'




```python

```
## Featureform

最后，我们将使用[Featureform](https://github.com/featureform/featureform)，一个开源的、企业级的特征存储，来运行相同的示例。Featureform允许您使用像Spark或本地环境这样的基础架构来定义特征转换。

### 初始化 Featureform

您可以按照自述文件中的说明，在Featureform中初始化您的转换和特征。

```python
import featureform as ff

client = ff.Client(host="demo.featureform.com")
```

### Prompts

在这里，我们将设置一个自定义的FeatureformPromptTemplate。该提示模板将接受用户每次交易的平均支付金额。

请注意，此提示模板的输入只是 `avg_transaction`，因为这是用户定义的唯一部分（所有其他变量都在提示模板内部查找）。

```python
from langchain.prompts import PromptTemplate, StringPromptTemplate
```


```python
template = """Given the amount a user spends on average per transaction, let them know if they are a high roller. Otherwise, make a silly joke about chickens at the end to make them feel better

Here are the user's stats:
Average Amount per Transaction: ${avg_transcation}

Your response:"""
prompt = PromptTemplate.from_template(template)
```


```python
class FeatureformPromptTemplate(StringPromptTemplate):
    def format(self, **kwargs) -> str:
        user_id = kwargs.pop("user_id")
        fpf = client.features([("avg_transactions", "quickstart")], {"user": user_id})
        return prompt.format(**kwargs)
```


```python
prompt_template = FeatureformPrompTemplate(input_variables=["user_id"])
```


```python
print(prompt_template.format(user_id="C1410926"))
```
### 在链中使用

现在我们可以将其用于链中，成功创建一个基于Featureform特征平台支持的个性化链。


```python
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
```


```python
chain = LLMChain(llm=ChatOpenAI(), prompt=prompt_template)
```


```python
chain.run("C1410926")
```
