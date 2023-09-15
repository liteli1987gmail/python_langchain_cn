# Data Augmented Question Answering

This notebook uses some generic prompts/language models to evaluate an question answering system that uses other sources of data besides what is in the model. For example, this can be used to evaluate a question answering system over your proprietary data.

## Setup
Let's set up an example with our favorite example - the state of the union address.


```python
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
```


```python
from langchain.document_loaders import TextLoader

loader = TextLoader("../../modules/state_of_the_union.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
docsearch = Chroma.from_documents(texts, embeddings)
qa = RetrievalQA.from_llm(llm=OpenAI(), retriever=docsearch.as_retriever())
```

    Running Chroma using direct local API.
    Using DuckDB in-memory for database. Data will be transient.
    

## Examples
Now we need some examples to evaluate. We can do this in two ways:

1. Hard code some examples ourselves
2. Generate examples automatically, using a language model


```python
# Hard-coded examples
examples = [
    {
        "query": "What did the president say about Ketanji Brown Jackson",
        "answer": "He praised her legal ability and said he nominated her for the supreme court.",
    },
    {"query": "What did the president say about Michael Jackson", "answer": "Nothing"},
]
```


```python
# Generated examples
from langchain.evaluation.qa import QAGenerateChain

example_gen_chain = QAGenerateChain.from_llm(OpenAI())
```


```python
new_examples = example_gen_chain.apply_and_parse([{"doc": t} for t in texts[:5]])
```


```python
new_examples
```




    [{'query': 'According to the document, what did Vladimir Putin miscalculate?',
      'answer': 'He miscalculated that he could roll into Ukraine and the world would roll over.'},
     {'query': 'Who is the Ukrainian Ambassador to the United States?',
      'answer': 'The Ukrainian Ambassador to the United States is here tonight.'},
     {'query': 'How many countries were part of the coalition formed to confront Putin?',
      'answer': '27 members of the European Union, France, Germany, Italy, the United Kingdom, Canada, Japan, Korea, Australia, New Zealand, and many others, even Switzerland.'},
     {'query': 'What action is the U.S. Department of Justice taking to target Russian oligarchs?',
      'answer': 'The U.S. Department of Justice is assembling a dedicated task force to go after the crimes of Russian oligarchs and joining with European allies to find and seize their yachts, luxury apartments, and private jets.'},
     {'query': 'How much direct assistance is the United States providing to Ukraine?',
      'answer': 'The United States is providing more than $1 Billion in direct assistance to Ukraine.'}]




```python
# Combine examples
examples += new_examples
```

## Evaluate
Now that we have examples, we can use the question answering evaluator to evaluate our question answering chain.


```python
from langchain.evaluation.qa import QAEvalChain
```


```python
predictions = qa.apply(examples)
```


```python
llm = OpenAI(temperature=0)
eval_chain = QAEvalChain.from_llm(llm)
```


```python
graded_outputs = eval_chain.evaluate(examples, predictions)
```


```python
for i, eg in enumerate(examples):
    print(f"Example {i}:")
    print("Question: " + predictions[i]["query"])
    print("Real Answer: " + predictions[i]["answer"])
    print("Predicted Answer: " + predictions[i]["result"])
    print("Predicted Grade: " + graded_outputs[i]["text"])
    print()
```

    Example 0:
    Question: What did the president say about Ketanji Brown Jackson
    Real Answer: He praised her legal ability and said he nominated her for the supreme court.
    Predicted Answer:  The president said that she is one of the nation's top legal minds, a former top litigator in private practice, a former federal public defender, and from a family of public school educators and police officers. He also said that she is a consensus builder and that she has received a broad range of support from the Fraternal Order of Police to former judges appointed by both Democrats and Republicans.
    Predicted Grade:  CORRECT
    
    Example 1:
    Question: What did the president say about Michael Jackson
    Real Answer: Nothing
    Predicted Answer:  The president did not mention Michael Jackson in this speech.
    Predicted Grade:  CORRECT
    
    Example 2:
    Question: According to the document, what did Vladimir Putin miscalculate?
    Real Answer: He miscalculated that he could roll into Ukraine and the world would roll over.
    Predicted Answer:  Putin miscalculated that the world would roll over when he rolled into Ukraine.
    Predicted Grade:  CORRECT
    
    Example 3:
    Question: Who is the Ukrainian Ambassador to the United States?
    Real Answer: The Ukrainian Ambassador to the United States is here tonight.
    Predicted Answer:  I don't know.
    Predicted Grade:  INCORRECT
    
    Example 4:
    Question: How many countries were part of the coalition formed to confront Putin?
    Real Answer: 27 members of the European Union, France, Germany, Italy, the United Kingdom, Canada, Japan, Korea, Australia, New Zealand, and many others, even Switzerland.
    Predicted Answer:  The coalition included freedom-loving nations from Europe and the Americas to Asia and Africa, 27 members of the European Union including France, Germany, Italy, the United Kingdom, Canada, Japan, Korea, Australia, New Zealand, and many others, even Switzerland.
    Predicted Grade:  INCORRECT
    
    Example 5:
    Question: What action is the U.S. Department of Justice taking to target Russian oligarchs?
    Real Answer: The U.S. Department of Justice is assembling a dedicated task force to go after the crimes of Russian oligarchs and joining with European allies to find and seize their yachts, luxury apartments, and private jets.
    Predicted Answer:  The U.S. Department of Justice is assembling a dedicated task force to go after the crimes of Russian oligarchs and to find and seize their yachts, luxury apartments, and private jets.
    Predicted Grade:  INCORRECT
    
    Example 6:
    Question: How much direct assistance is the United States providing to Ukraine?
    Real Answer: The United States is providing more than $1 Billion in direct assistance to Ukraine.
    Predicted Answer:  The United States is providing more than $1 billion in direct assistance to Ukraine.
    Predicted Grade:  CORRECT
    
    

## Evaluate with Other Metrics

In addition to predicting whether the answer is correct or incorrect using a language model, we can also use other metrics to get a more nuanced view on the quality of the answers. To do so, we can use the [Critique](https://docs.inspiredco.ai/critique/) library, which allows for simple calculation of various metrics over generated text.

First you can get an API key from the [Inspired Cognition Dashboard](https://dashboard.inspiredco.ai) and do some setup:

```bash
export INSPIREDCO_API_KEY="..."
pip install inspiredco
```


```python
import inspiredco.critique
import os

critique = inspiredco.critique.Critique(api_key=os.environ["INSPIREDCO_API_KEY"])
```

Then run the following code to set up the configuration and calculate the [ROUGE](https://docs.inspiredco.ai/critique/metric_rouge.html), [chrf](https://docs.inspiredco.ai/critique/metric_chrf.html), [BERTScore](https://docs.inspiredco.ai/critique/metric_bert_score.html), and [UniEval](https://docs.inspiredco.ai/critique/metric_uni_eval.html) (you can choose [other metrics](https://docs.inspiredco.ai/critique/metrics.html) too):


```python
metrics = {
    "rouge": {
        "metric": "rouge",
        "config": {"variety": "rouge_l"},
    },
    "chrf": {
        "metric": "chrf",
        "config": {},
    },
    "bert_score": {
        "metric": "bert_score",
        "config": {"model": "bert-base-uncased"},
    },
    "uni_eval": {
        "metric": "uni_eval",
        "config": {"task": "summarization", "evaluation_aspect": "relevance"},
    },
}
```


```python
critique_data = [
    {"target": pred["result"], "references": [pred["answer"]]} for pred in predictions
]
eval_results = {
    k: critique.evaluate(dataset=critique_data, metric=v["metric"], config=v["config"])
    for k, v in metrics.items()
}
```

Finally, we can print out the results. We can see that overall the scores are higher when the output is semantically correct, and also when the output closely matches with the gold-standard answer.


```python
for i, eg in enumerate(examples):
    score_string = ", ".join(
        [f"{k}={v['examples'][i]['value']:.4f}" for k, v in eval_results.items()]
    )
    print(f"Example {i}:")
    print("Question: " + predictions[i]["query"])
    print("Real Answer: " + predictions[i]["answer"])
    print("Predicted Answer: " + predictions[i]["result"])
    print("Predicted Scores: " + score_string)
    print()
```

    Example 0:
    Question: What did the president say about Ketanji Brown Jackson
    Real Answer: He praised her legal ability and said he nominated her for the supreme court.
    Predicted Answer:  The president said that she is one of the nation's top legal minds, a former top litigator in private practice, a former federal public defender, and from a family of public school educators and police officers. He also said that she is a consensus builder and that she has received a broad range of support from the Fraternal Order of Police to former judges appointed by both Democrats and Republicans.
    Predicted Scores: rouge=0.0941, chrf=0.2001, bert_score=0.5219, uni_eval=0.9043
    
    Example 1:
    Question: What did the president say about Michael Jackson
    Real Answer: Nothing
    Predicted Answer:  The president did not mention Michael Jackson in this speech.
    Predicted Scores: rouge=0.0000, chrf=0.1087, bert_score=0.3486, uni_eval=0.7802
    
    Example 2:
    Question: According to the document, what did Vladimir Putin miscalculate?
    Real Answer: He miscalculated that he could roll into Ukraine and the world would roll over.
    Predicted Answer:  Putin miscalculated that the world would roll over when he rolled into Ukraine.
    Predicted Scores: rouge=0.5185, chrf=0.6955, bert_score=0.8421, uni_eval=0.9578
    
    Example 3:
    Question: Who is the Ukrainian Ambassador to the United States?
    Real Answer: The Ukrainian Ambassador to the United States is here tonight.
    Predicted Answer:  I don't know.
    Predicted Scores: rouge=0.0000, chrf=0.0375, bert_score=0.3159, uni_eval=0.7493
    
    Example 4:
    Question: How many countries were part of the coalition formed to confront Putin?
    Real Answer: 27 members of the European Union, France, Germany, Italy, the United Kingdom, Canada, Japan, Korea, Australia, New Zealand, and many others, even Switzerland.
    Predicted Answer:  The coalition included freedom-loving nations from Europe and the Americas to Asia and Africa, 27 members of the European Union including France, Germany, Italy, the United Kingdom, Canada, Japan, Korea, Australia, New Zealand, and many others, even Switzerland.
    Predicted Scores: rouge=0.7419, chrf=0.8602, bert_score=0.8388, uni_eval=0.0669
    
    Example 5:
    Question: What action is the U.S. Department of Justice taking to target Russian oligarchs?
    Real Answer: The U.S. Department of Justice is assembling a dedicated task force to go after the crimes of Russian oligarchs and joining with European allies to find and seize their yachts, luxury apartments, and private jets.
    Predicted Answer:  The U.S. Department of Justice is assembling a dedicated task force to go after the crimes of Russian oligarchs and to find and seize their yachts, luxury apartments, and private jets.
    Predicted Scores: rouge=0.9412, chrf=0.8687, bert_score=0.9607, uni_eval=0.9718
    
    Example 6:
    Question: How much direct assistance is the United States providing to Ukraine?
    Real Answer: The United States is providing more than $1 Billion in direct assistance to Ukraine.
    Predicted Answer:  The United States is providing more than $1 billion in direct assistance to Ukraine.
    Predicted Scores: rouge=1.0000, chrf=0.9483, bert_score=1.0000, uni_eval=0.9734
    
    
