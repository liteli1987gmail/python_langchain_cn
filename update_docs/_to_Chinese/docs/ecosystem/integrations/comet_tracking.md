# 彗星

![](https://user-images.githubusercontent.com/7529846/230328046-a8b18c51-12e3-4617-9b39-97614a571a2d.png)

在本指南中，我们将演示如何使用[Comet](https://www.comet.com/site/?utm_source=langchain&utm_medium=referral&utm_campaign=comet_notebook) 跟踪您的Langchain实验、评估指标和LLM会话。

<a target="_blank" href="https://colab.research.google.com/github/hwchase17/langchain/blob/master/docs/ecosystem/comet_tracking.html">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="在Colab中打开"/>
</a>

**示例项目：** [Comet与LangChain](https://www.comet.com/examples/comet-example-langchain/view/b5ZThK6OFdhKWVSP3fDfRtrNF/panels?utm_source=langchain&utm_medium=referral&utm_campaign=comet_notebook)

![](https://user-images.githubusercontent.com/7529846/230326720-a9711435-9c6f-4edb-a707-94b67271ab25.png)


### 安装Comet和依赖


```python
%pip install comet_ml langchain openai google-search-results spacy textstat pandas

import sys

!{sys.executable} -m spacy download en_core_web_sm
```

### 初始化Comet并设置您的凭证

您可以在此处获取您的[Comet API密钥](https://www.comet.com/signup?utm_source=langchain&utm_medium=referral&utm_campaign=comet_notebook)，或在初始化Comet后单击链接


```python
import comet_ml

comet_ml.init(project_name="comet-example-langchain")
```

### 设置OpenAI和SerpAPI凭据

您需要一个[OpenAI API密钥](https://platform.openai.com/account/api-keys)和一个[SerpAPI API密钥](https://serpapi.com/dashboard)来运行以下示例


```python
import os

os.environ["OPENAI_API_KEY"] = "..."
# os.environ["OPENAI_ORGANIZATION"] = "..."
os.environ["SERPAPI_API_KEY"] = "..."
```

### 场景1：仅使用LLM


```python
from datetime import datetime

from langchain.callbacks import CometCallbackHandler, StdOutCallbackHandler
from langchain.llms import OpenAI

comet_callback = CometCallbackHandler(
    project_name="comet-example-langchain",
    complexity_metrics=True,
    stream_logs=True,
    tags=["llm"],
    visualizations=["dep"],
)
callbacks = [StdOutCallbackHandler(), comet_callback]
llm = OpenAI(temperature=0.9, callbacks=callbacks, verbose=True)

llm_result = llm.generate(["Tell me a joke", "Tell me a poem", "Tell me a fact"] * 3)
print("LLM result", llm_result)
comet_callback.flush_tracker(llm, finish=True)
```

### 场景2：在链中使用LLM


```python
from langchain.callbacks import CometCallbackHandler, StdOutCallbackHandler
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

comet_callback = CometCallbackHandler(
    complexity_metrics=True,
    project_name="comet-example-langchain",
    stream_logs=True,
    tags=["synopsis-chain"],
)
callbacks = [StdOutCallbackHandler(), comet_callback]
llm = OpenAI(temperature=0.9, callbacks=callbacks)

template = """You are a playwright. Given the title of play, it is your job to write a synopsis for that title.
Title: {title}
Playwright: This is a synopsis for the above play:"""
prompt_template = PromptTemplate(input_variables=["title"], template=template)
synopsis_chain = LLMChain(llm=llm, prompt=prompt_template, callbacks=callbacks)

test_prompts = [{"title": "Documentary about Bigfoot in Paris"}]
print(synopsis_chain.apply(test_prompts))
comet_callback.flush_tracker(synopsis_chain, finish=True)
```

### 场景3：使用具备工具的代理


```python
from langchain.agents import initialize_agent, load_tools
from langchain.callbacks import CometCallbackHandler, StdOutCallbackHandler
from langchain.llms import OpenAI

comet_callback = CometCallbackHandler(
    project_name="comet-example-langchain",
    complexity_metrics=True,
    stream_logs=True,
    tags=["agent"],
)
callbacks = [StdOutCallbackHandler(), comet_callback]
llm = OpenAI(temperature=0.9, callbacks=callbacks)

tools = load_tools(["serpapi", "llm-math"], llm=llm, callbacks=callbacks)
agent = initialize_agent(
    tools,
    llm,
    agent="zero-shot-react-description",
    callbacks=callbacks,
    verbose=True,
)
agent.run(
    "Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?"
)
comet_callback.flush_tracker(agent, finish=True)
```

### 场景4：使用自定义评估指标

`CometCallbackManager`还允许您定义和使用自定义评估指标来评估模型生成的输出质量。让我们看看这是如何工作的。 


在下面的代码段中，我们将使用[ROUGE](https://huggingface.co/spaces/evaluate-metric/rouge)指标来评估生成的摘要的质量。 


```python
%pip install rouge-score
```


```python
from rouge_score import rouge_scorer

from langchain.callbacks import CometCallbackHandler, StdOutCallbackHandler
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate


class Rouge:
    def __init__(self, reference):
        self.reference = reference
        self.scorer = rouge_scorer.RougeScorer(["rougeLsum"], use_stemmer=True)

    def compute_metric(self, generation, prompt_idx, gen_idx):
        prediction = generation.text
        results = self.scorer.score(target=self.reference, prediction=prediction)

        return {
            "rougeLsum_score": results["rougeLsum"].fmeasure,
            "reference": self.reference,
        }


reference = """
The tower is 324 metres (1,063 ft) tall, about the same height as an 81-storey building.
It was the first structure to reach a height of 300 metres.

It is now taller than the Chrysler Building in New York City by 5.2 metres (17 ft)
Excluding transmitters, the Eiffel Tower is the second tallest free-standing structure in France .
"""
rouge_score = Rouge(reference=reference)

template = """Given the following article, it is your job to write a summary.
Article:
{article}
Summary: This is the summary for the above article:"""
prompt_template = PromptTemplate(input_variables=["article"], template=template)

comet_callback = CometCallbackHandler(
    project_name="comet-example-langchain",
    complexity_metrics=False,
    stream_logs=True,
    tags=["custom_metrics"],
    custom_metrics=rouge_score.compute_metric,
)
callbacks = [StdOutCallbackHandler(), comet_callback]
llm = OpenAI(temperature=0.9)

synopsis_chain = LLMChain(llm=llm, prompt=prompt_template)

test_prompts = [
    {
        "article": """
                 The tower is 324 metres (1,063 ft) tall, about the same height as
                 an 81-storey building, and the tallest structure in Paris. Its base is square,
                 measuring 125 metres (410 ft) on each side.
                 During its construction, the Eiffel Tower surpassed the
                 Washington Monument to become the tallest man-made structure in the world,
                 a title it held for 41 years until the Chrysler Building
                 in New York City was finished in 1930.

                 It was the first structure to reach a height of 300 metres.
                 Due to the addition of a broadcasting aerial at the top of the tower in 1957,
                 it is now taller than the Chrysler Building by 5.2 metres (17 ft).

                 Excluding transmitters, the Eiffel Tower is the second tallest
                 free-standing structure in France after the Millau Viaduct.
                 """
    }
]
print(synopsis_chain.apply(test_prompts, callbacks=callbacks))
comet_callback.flush_tracker(synopsis_chain, finish=True)
```
