# Evaluating an OpenAPI Chain

This notebook goes over ways to semantically evaluate an [OpenAPI Chain](openapi.html), which calls an endpoint defined by the OpenAPI specification using purely natural language.


```python
from langchain.tools import OpenAPISpec, APIOperation
from langchain.chains import OpenAPIEndpointChain, LLMChain
from langchain.requests import Requests
from langchain.llms import OpenAI
```

## Load the API Chain

Load a wrapper of the spec (so we can work with it more easily). You can load from a url or from a local file.


```python
# Load and parse the OpenAPI Spec
spec = OpenAPISpec.from_url(
    "https://www.klarna.com/us/shopping/public/openai/v0/api-docs/"
)
# Load a single endpoint operation
operation = APIOperation.from_openapi_spec(spec, "/public/openai/v0/products", "get")
verbose = False
# Select any LangChain LLM
llm = OpenAI(temperature=0, max_tokens=1000)
# Create the endpoint chain
api_chain = OpenAPIEndpointChain.from_api_operation(
    operation,
    llm,
    requests=Requests(),
    verbose=verbose,
    return_intermediate_steps=True,  # Return request and response text
)
```

    Attempting to load an OpenAPI 3.0.1 spec.  This may result in degraded performance. Convert your OpenAPI spec to 3.1.* spec for better support.
    

### *Optional*: Generate Input Questions and Request Ground Truth Queries

See [Generating Test Datasets](#Generating-Test-Datasets) at the end of this notebook for more details.


```python
# import re
# from langchain.prompts import PromptTemplate

# template = """Below is a service description:

# {spec}

# Imagine you're a new user trying to use {operation} through a search bar. What are 10 different things you want to request?
# Wants/Questions:
# 1. """

# prompt = PromptTemplate.from_template(template)

# generation_chain = LLMChain(llm=llm, prompt=prompt)

# questions_ = generation_chain.run(spec=operation.to_typescript(), operation=operation.operation_id).split('\n')
# # Strip preceding numeric bullets
# questions = [re.sub(r'^\d+\. ', '', q).strip() for q in questions_]
# questions
```


```python
# ground_truths = [
# {"q": ...} # What are the best queries for each input?
# ]
```

## Run the API Chain

The two simplest questions a user of the API Chain are:
- Did the chain succesfully access the endpoint?
- Did the action accomplish the correct result?



```python
from collections import defaultdict

# Collect metrics to report at completion
scores = defaultdict(list)
```


```python
from langchain.evaluation.loading import load_dataset

dataset = load_dataset("openapi-chain-klarna-products-get")
```

    Found cached dataset json (/Users/harrisonchase/.cache/huggingface/datasets/LangChainDatasets___json/LangChainDatasets--openapi-chain-klarna-products-get-5d03362007667626/0.0.0/0f7e3662623656454fcd2b650f34e886a7db4b9104504885bd462096cc7a9f51)
    


      0%|          | 0/1 [00:00<?, ?it/s]



```python
dataset
```




    [{'question': 'What iPhone models are available?',
      'expected_query': {'max_price': None, 'q': 'iPhone'}},
     {'question': 'Are there any budget laptops?',
      'expected_query': {'max_price': 300, 'q': 'laptop'}},
     {'question': 'Show me the cheapest gaming PC.',
      'expected_query': {'max_price': 500, 'q': 'gaming pc'}},
     {'question': 'Are there any tablets under $400?',
      'expected_query': {'max_price': 400, 'q': 'tablet'}},
     {'question': 'What are the best headphones?',
      'expected_query': {'max_price': None, 'q': 'headphones'}},
     {'question': 'What are the top rated laptops?',
      'expected_query': {'max_price': None, 'q': 'laptop'}},
     {'question': 'I want to buy some shoes. I like Adidas and Nike.',
      'expected_query': {'max_price': None, 'q': 'shoe'}},
     {'question': 'I want to buy a new skirt',
      'expected_query': {'max_price': None, 'q': 'skirt'}},
     {'question': 'My company is asking me to get a professional Deskopt PC - money is no object.',
      'expected_query': {'max_price': 10000, 'q': 'professional desktop PC'}},
     {'question': 'What are the best budget cameras?',
      'expected_query': {'max_price': 300, 'q': 'camera'}}]




```python
questions = [d["question"] for d in dataset]
```


```python
## Run the the API chain itself
raise_error = False  # Stop on first failed example - useful for development
chain_outputs = []
failed_examples = []
for question in questions:
    try:
        chain_outputs.append(api_chain(question))
        scores["completed"].append(1.0)
    except Exception as e:
        if raise_error:
            raise e
        failed_examples.append({"q": question, "error": e})
        scores["completed"].append(0.0)
```


```python
# If the chain failed to run, show the failing examples
failed_examples
```




    []




```python
answers = [res["output"] for res in chain_outputs]
answers
```




    ['There are currently 10 Apple iPhone models available: Apple iPhone 14 Pro Max 256GB, Apple iPhone 12 128GB, Apple iPhone 13 128GB, Apple iPhone 14 Pro 128GB, Apple iPhone 14 Pro 256GB, Apple iPhone 14 Pro Max 128GB, Apple iPhone 13 Pro Max 128GB, Apple iPhone 14 128GB, Apple iPhone 12 Pro 512GB, and Apple iPhone 12 mini 64GB.',
     'Yes, there are several budget laptops in the API response. For example, the HP 14-dq0055dx and HP 15-dw0083wm are both priced at $199.99 and $244.99 respectively.',
     'The cheapest gaming PC available is the Alarco Gaming PC (X_BLACK_GTX750) for $499.99. You can find more information about it here: https://www.klarna.com/us/shopping/pl/cl223/3203154750/Desktop-Computers/Alarco-Gaming-PC-%28X_BLACK_GTX750%29/?utm_source=openai&ref-site=openai_plugin',
     'Yes, there are several tablets under $400. These include the Apple iPad 10.2" 32GB (2019), Samsung Galaxy Tab A8 10.5 SM-X200 32GB, Samsung Galaxy Tab A7 Lite 8.7 SM-T220 32GB, Amazon Fire HD 8" 32GB (10th Generation), and Amazon Fire HD 10 32GB.',
     'It looks like you are looking for the best headphones. Based on the API response, it looks like the Apple AirPods Pro (2nd generation) 2022, Apple AirPods Max, and Bose Noise Cancelling Headphones 700 are the best options.',
     'The top rated laptops based on the API response are the Apple MacBook Pro (2021) M1 Pro 8C CPU 14C GPU 16GB 512GB SSD 14", Apple MacBook Pro (2022) M2 OC 10C GPU 8GB 256GB SSD 13.3", Apple MacBook Air (2022) M2 OC 8C GPU 8GB 256GB SSD 13.6", and Apple MacBook Pro (2023) M2 Pro OC 16C GPU 16GB 512GB SSD 14.2".',
     "I found several Nike and Adidas shoes in the API response. Here are the links to the products: Nike Dunk Low M - Black/White: https://www.klarna.com/us/shopping/pl/cl337/3200177969/Shoes/Nike-Dunk-Low-M-Black-White/?utm_source=openai&ref-site=openai_plugin, Nike Air Jordan 4 Retro M - Midnight Navy: https://www.klarna.com/us/shopping/pl/cl337/3202929835/Shoes/Nike-Air-Jordan-4-Retro-M-Midnight-Navy/?utm_source=openai&ref-site=openai_plugin, Nike Air Force 1 '07 M - White: https://www.klarna.com/us/shopping/pl/cl337/3979297/Shoes/Nike-Air-Force-1-07-M-White/?utm_source=openai&ref-site=openai_plugin, Nike Dunk Low W - White/Black: https://www.klarna.com/us/shopping/pl/cl337/3200134705/Shoes/Nike-Dunk-Low-W-White-Black/?utm_source=openai&ref-site=openai_plugin, Nike Air Jordan 1 Retro High M - White/University Blue/Black: https://www.klarna.com/us/shopping/pl/cl337/3200383658/Shoes/Nike-Air-Jordan-1-Retro-High-M-White-University-Blue-Black/?utm_source=openai&ref-site=openai_plugin, Nike Air Jordan 1 Retro High OG M - True Blue/Cement Grey/White: https://www.klarna.com/us/shopping/pl/cl337/3204655673/Shoes/Nike-Air-Jordan-1-Retro-High-OG-M-True-Blue-Cement-Grey-White/?utm_source=openai&ref-site=openai_plugin, Nike Air Jordan 11 Retro Cherry - White/Varsity Red/Black: https://www.klarna.com/us/shopping/pl/cl337/3202929696/Shoes/Nike-Air-Jordan-11-Retro-Cherry-White-Varsity-Red-Black/?utm_source=openai&ref-site=openai_plugin, Nike Dunk High W - White/Black: https://www.klarna.com/us/shopping/pl/cl337/3201956448/Shoes/Nike-Dunk-High-W-White-Black/?utm_source=openai&ref-site=openai_plugin, Nike Air Jordan 5 Retro M - Black/Taxi/Aquatone: https://www.klarna.com/us/shopping/pl/cl337/3204923084/Shoes/Nike-Air-Jordan-5-Retro-M-Black-Taxi-Aquatone/?utm_source=openai&ref-site=openai_plugin, Nike Court Legacy Lift W: https://www.klarna.com/us/shopping/pl/cl337/3202103728/Shoes/Nike-Court-Legacy-Lift-W/?utm_source=openai&ref-site=openai_plugin",
     "I found several skirts that may interest you. Please take a look at the following products: Avenue Plus Size Denim Stretch Skirt, LoveShackFancy Ruffled Mini Skirt - Antique White, Nike Dri-Fit Club Golf Skirt - Active Pink, Skims Soft Lounge Ruched Long Skirt, French Toast Girl's Front Pleated Skirt with Tabs, Alexia Admor Women's Harmonie Mini Skirt Pink Pink, Vero Moda Long Skirt, Nike Court Dri-FIT Victory Flouncy Tennis Skirt Women - White/Black, Haoyuan Mini Pleated Skirts W, and Zimmermann Lyre Midi Skirt.",
     'Based on the API response, you may want to consider the Skytech Archangel Gaming Computer PC Desktop, the CyberPowerPC Gamer Master Gaming Desktop, or the ASUS ROG Strix G10DK-RS756, as they all offer powerful processors and plenty of RAM.',
     'Based on the API response, the best budget cameras are the DJI Mini 2 Dog Camera ($448.50), Insta360 Sphere with Landing Pad ($429.99), DJI FPV Gimbal Camera ($121.06), Parrot Camera & Body ($36.19), and DJI FPV Air Unit ($179.00).']



## Evaluate the requests chain

The API Chain has two main components:
1. Translate the user query to an API request (request synthesizer)
2. Translate the API response to a natural language response

Here, we construct an evaluation chain to grade the request synthesizer against selected human queries 


```python
import json

truth_queries = [json.dumps(data["expected_query"]) for data in dataset]
```


```python
# Collect the API queries generated by the chain
predicted_queries = [
    output["intermediate_steps"]["request_args"] for output in chain_outputs
]
```


```python
from langchain.prompts import PromptTemplate

template = """You are trying to answer the following question by querying an API:

> Question: {question}

The query you know you should be executing against the API is:

> Query: {truth_query}

Is the following predicted query semantically the same (eg likely to produce the same answer)?

> Predicted Query: {predict_query}

Please give the Predicted Query a grade of either an A, B, C, D, or F, along with an explanation of why. End the evaluation with 'Final Grade: <the letter>'

> Explanation: Let's think step by step."""

prompt = PromptTemplate.from_template(template)

eval_chain = LLMChain(llm=llm, prompt=prompt, verbose=verbose)
```


```python
request_eval_results = []
for question, predict_query, truth_query in list(
    zip(questions, predicted_queries, truth_queries)
):
    eval_output = eval_chain.run(
        question=question,
        truth_query=truth_query,
        predict_query=predict_query,
    )
    request_eval_results.append(eval_output)
request_eval_results
```




    [' The original query is asking for all iPhone models, so the "q" parameter is correct. The "max_price" parameter is also correct, as it is set to null, meaning that no maximum price is set. The predicted query adds two additional parameters, "size" and "min_price". The "size" parameter is not necessary, as it is not relevant to the question being asked. The "min_price" parameter is also not necessary, as it is not relevant to the question being asked and it is set to 0, which is the default value. Therefore, the predicted query is not semantically the same as the original query and is not likely to produce the same answer. Final Grade: D',
     ' The original query is asking for laptops with a maximum price of 300. The predicted query is asking for laptops with a minimum price of 0 and a maximum price of 500. This means that the predicted query is likely to return more results than the original query, as it is asking for a wider range of prices. Therefore, the predicted query is not semantically the same as the original query, and it is not likely to produce the same answer. Final Grade: F',
     " The first two parameters are the same, so that's good. The third parameter is different, but it's not necessary for the query, so that's not a problem. The fourth parameter is the problem. The original query specifies a maximum price of 500, while the predicted query specifies a maximum price of null. This means that the predicted query will not limit the results to the cheapest gaming PCs, so it is not semantically the same as the original query. Final Grade: F",
     ' The original query is asking for tablets under $400, so the first two parameters are correct. The predicted query also includes the parameters "size" and "min_price", which are not necessary for the original query. The "size" parameter is not relevant to the question, and the "min_price" parameter is redundant since the original query already specifies a maximum price. Therefore, the predicted query is not semantically the same as the original query and is not likely to produce the same answer. Final Grade: D',
     ' The original query is asking for headphones with no maximum price, so the predicted query is not semantically the same because it has a maximum price of 500. The predicted query also has a size of 10, which is not specified in the original query. Therefore, the predicted query is not semantically the same as the original query. Final Grade: F',
     " The original query is asking for the top rated laptops, so the 'size' parameter should be set to 10 to get the top 10 results. The 'min_price' parameter should be set to 0 to get results from all price ranges. The 'max_price' parameter should be set to null to get results from all price ranges. The 'q' parameter should be set to 'laptop' to get results related to laptops. All of these parameters are present in the predicted query, so it is semantically the same as the original query. Final Grade: A",
     ' The original query is asking for shoes, so the predicted query is asking for the same thing. The original query does not specify a size, so the predicted query is not adding any additional information. The original query does not specify a price range, so the predicted query is adding additional information that is not necessary. Therefore, the predicted query is not semantically the same as the original query and is likely to produce different results. Final Grade: D',
     ' The original query is asking for a skirt, so the predicted query is asking for the same thing. The predicted query also adds additional parameters such as size and price range, which could help narrow down the results. However, the size parameter is not necessary for the query to be successful, and the price range is too narrow. Therefore, the predicted query is not as effective as the original query. Final Grade: C',
     ' The first part of the query is asking for a Desktop PC, which is the same as the original query. The second part of the query is asking for a size of 10, which is not relevant to the original query. The third part of the query is asking for a minimum price of 0, which is not relevant to the original query. The fourth part of the query is asking for a maximum price of null, which is not relevant to the original query. Therefore, the Predicted Query does not semantically match the original query and is not likely to produce the same answer. Final Grade: F',
     ' The original query is asking for cameras with a maximum price of 300. The predicted query is asking for cameras with a maximum price of 500. This means that the predicted query is likely to return more results than the original query, which may include cameras that are not within the budget range. Therefore, the predicted query is not semantically the same as the original query and does not answer the original question. Final Grade: F']




```python
import re
from typing import List


# Parse the evaluation chain responses into a rubric
def parse_eval_results(results: List[str]) -> List[float]:
    rubric = {"A": 1.0, "B": 0.75, "C": 0.5, "D": 0.25, "F": 0}
    return [rubric[re.search(r"Final Grade: (\w+)", res).group(1)] for res in results]


parsed_results = parse_eval_results(request_eval_results)
# Collect the scores for a final evaluation table
scores["request_synthesizer"].extend(parsed_results)
```

## Evaluate the Response Chain

The second component translated the structured API response to a natural language response.
Evaluate this against the user's original question.


```python
from langchain.prompts import PromptTemplate

template = """You are trying to answer the following question by querying an API:

> Question: {question}

The API returned a response of:

> API result: {api_response}

Your response to the user: {answer}

Please evaluate the accuracy and utility of your response to the user's original question, conditioned on the information available.
Give a letter grade of either an A, B, C, D, or F, along with an explanation of why. End the evaluation with 'Final Grade: <the letter>'

> Explanation: Let's think step by step."""

prompt = PromptTemplate.from_template(template)

eval_chain = LLMChain(llm=llm, prompt=prompt, verbose=verbose)
```


```python
# Extract the API responses from the chain
api_responses = [
    output["intermediate_steps"]["response_text"] for output in chain_outputs
]
```


```python
# Run the grader chain
response_eval_results = []
for question, api_response, answer in list(zip(questions, api_responses, answers)):
    request_eval_results.append(
        eval_chain.run(question=question, api_response=api_response, answer=answer)
    )
request_eval_results
```




    [' The original query is asking for all iPhone models, so the "q" parameter is correct. The "max_price" parameter is also correct, as it is set to null, meaning that no maximum price is set. The predicted query adds two additional parameters, "size" and "min_price". The "size" parameter is not necessary, as it is not relevant to the question being asked. The "min_price" parameter is also not necessary, as it is not relevant to the question being asked and it is set to 0, which is the default value. Therefore, the predicted query is not semantically the same as the original query and is not likely to produce the same answer. Final Grade: D',
     ' The original query is asking for laptops with a maximum price of 300. The predicted query is asking for laptops with a minimum price of 0 and a maximum price of 500. This means that the predicted query is likely to return more results than the original query, as it is asking for a wider range of prices. Therefore, the predicted query is not semantically the same as the original query, and it is not likely to produce the same answer. Final Grade: F',
     " The first two parameters are the same, so that's good. The third parameter is different, but it's not necessary for the query, so that's not a problem. The fourth parameter is the problem. The original query specifies a maximum price of 500, while the predicted query specifies a maximum price of null. This means that the predicted query will not limit the results to the cheapest gaming PCs, so it is not semantically the same as the original query. Final Grade: F",
     ' The original query is asking for tablets under $400, so the first two parameters are correct. The predicted query also includes the parameters "size" and "min_price", which are not necessary for the original query. The "size" parameter is not relevant to the question, and the "min_price" parameter is redundant since the original query already specifies a maximum price. Therefore, the predicted query is not semantically the same as the original query and is not likely to produce the same answer. Final Grade: D',
     ' The original query is asking for headphones with no maximum price, so the predicted query is not semantically the same because it has a maximum price of 500. The predicted query also has a size of 10, which is not specified in the original query. Therefore, the predicted query is not semantically the same as the original query. Final Grade: F',
     " The original query is asking for the top rated laptops, so the 'size' parameter should be set to 10 to get the top 10 results. The 'min_price' parameter should be set to 0 to get results from all price ranges. The 'max_price' parameter should be set to null to get results from all price ranges. The 'q' parameter should be set to 'laptop' to get results related to laptops. All of these parameters are present in the predicted query, so it is semantically the same as the original query. Final Grade: A",
     ' The original query is asking for shoes, so the predicted query is asking for the same thing. The original query does not specify a size, so the predicted query is not adding any additional information. The original query does not specify a price range, so the predicted query is adding additional information that is not necessary. Therefore, the predicted query is not semantically the same as the original query and is likely to produce different results. Final Grade: D',
     ' The original query is asking for a skirt, so the predicted query is asking for the same thing. The predicted query also adds additional parameters such as size and price range, which could help narrow down the results. However, the size parameter is not necessary for the query to be successful, and the price range is too narrow. Therefore, the predicted query is not as effective as the original query. Final Grade: C',
     ' The first part of the query is asking for a Desktop PC, which is the same as the original query. The second part of the query is asking for a size of 10, which is not relevant to the original query. The third part of the query is asking for a minimum price of 0, which is not relevant to the original query. The fourth part of the query is asking for a maximum price of null, which is not relevant to the original query. Therefore, the Predicted Query does not semantically match the original query and is not likely to produce the same answer. Final Grade: F',
     ' The original query is asking for cameras with a maximum price of 300. The predicted query is asking for cameras with a maximum price of 500. This means that the predicted query is likely to return more results than the original query, which may include cameras that are not within the budget range. Therefore, the predicted query is not semantically the same as the original query and does not answer the original question. Final Grade: F',
     ' The user asked a question about what iPhone models are available, and the API returned a response with 10 different models. The response provided by the user accurately listed all 10 models, so the accuracy of the response is A+. The utility of the response is also A+ since the user was able to get the exact information they were looking for. Final Grade: A+',
     " The API response provided a list of laptops with their prices and attributes. The user asked if there were any budget laptops, and the response provided a list of laptops that are all priced under $500. Therefore, the response was accurate and useful in answering the user's question. Final Grade: A",
     " The API response provided the name, price, and URL of the product, which is exactly what the user asked for. The response also provided additional information about the product's attributes, which is useful for the user to make an informed decision. Therefore, the response is accurate and useful. Final Grade: A",
     " The API response provided a list of tablets that are under $400. The response accurately answered the user's question. Additionally, the response provided useful information such as the product name, price, and attributes. Therefore, the response was accurate and useful. Final Grade: A",
     " The API response provided a list of headphones with their respective prices and attributes. The user asked for the best headphones, so the response should include the best headphones based on the criteria provided. The response provided a list of headphones that are all from the same brand (Apple) and all have the same type of headphone (True Wireless, In-Ear). This does not provide the user with enough information to make an informed decision about which headphones are the best. Therefore, the response does not accurately answer the user's question. Final Grade: F",
     ' The API response provided a list of laptops with their attributes, which is exactly what the user asked for. The response provided a comprehensive list of the top rated laptops, which is what the user was looking for. The response was accurate and useful, providing the user with the information they needed. Final Grade: A',
     ' The API response provided a list of shoes from both Adidas and Nike, which is exactly what the user asked for. The response also included the product name, price, and attributes for each shoe, which is useful information for the user to make an informed decision. The response also included links to the products, which is helpful for the user to purchase the shoes. Therefore, the response was accurate and useful. Final Grade: A',
     " The API response provided a list of skirts that could potentially meet the user's needs. The response also included the name, price, and attributes of each skirt. This is a great start, as it provides the user with a variety of options to choose from. However, the response does not provide any images of the skirts, which would have been helpful for the user to make a decision. Additionally, the response does not provide any information about the availability of the skirts, which could be important for the user. \n\nFinal Grade: B",
     ' The user asked for a professional desktop PC with no budget constraints. The API response provided a list of products that fit the criteria, including the Skytech Archangel Gaming Computer PC Desktop, the CyberPowerPC Gamer Master Gaming Desktop, and the ASUS ROG Strix G10DK-RS756. The response accurately suggested these three products as they all offer powerful processors and plenty of RAM. Therefore, the response is accurate and useful. Final Grade: A',
     " The API response provided a list of cameras with their prices, which is exactly what the user asked for. The response also included additional information such as features and memory cards, which is not necessary for the user's question but could be useful for further research. The response was accurate and provided the user with the information they needed. Final Grade: A"]




```python
# Reusing the rubric from above, parse the evaluation chain responses
parsed_response_results = parse_eval_results(request_eval_results)
# Collect the scores for a final evaluation table
scores["result_synthesizer"].extend(parsed_response_results)
```


```python
# Print out Score statistics for the evaluation session
header = "{:<20}\t{:<10}\t{:<10}\t{:<10}".format("Metric", "Min", "Mean", "Max")
print(header)
for metric, metric_scores in scores.items():
    mean_scores = (
        sum(metric_scores) / len(metric_scores)
        if len(metric_scores) > 0
        else float("nan")
    )
    row = "{:<20}\t{:<10.2f}\t{:<10.2f}\t{:<10.2f}".format(
        metric, min(metric_scores), mean_scores, max(metric_scores)
    )
    print(row)
```

    Metric              	Min       	Mean      	Max       
    completed           	1.00      	1.00      	1.00      
    request_synthesizer 	0.00      	0.23      	1.00      
    result_synthesizer  	0.00      	0.55      	1.00      
    


```python
# Re-show the examples for which the chain failed to complete
failed_examples
```




    []



## Generating Test Datasets

To evaluate a chain against your own endpoint, you'll want to generate a test dataset that's conforms to the API.

This section provides an overview of how to bootstrap the process.

First, we'll parse the OpenAPI Spec. For this example, we'll [Speak](https://www.speak.com/)'s OpenAPI specification.


```python
# Load and parse the OpenAPI Spec
spec = OpenAPISpec.from_url("https://api.speak.com/openapi.yaml")
```

    Attempting to load an OpenAPI 3.0.1 spec.  This may result in degraded performance. Convert your OpenAPI spec to 3.1.* spec for better support.
    Attempting to load an OpenAPI 3.0.1 spec.  This may result in degraded performance. Convert your OpenAPI spec to 3.1.* spec for better support.
    


```python
# List the paths in the OpenAPI Spec
paths = sorted(spec.paths.keys())
paths
```




    ['/v1/public/openai/explain-phrase',
     '/v1/public/openai/explain-task',
     '/v1/public/openai/translate']




```python
# See which HTTP Methods are available for a given path
methods = spec.get_methods_for_path("/v1/public/openai/explain-task")
methods
```




    ['post']




```python
# Load a single endpoint operation
operation = APIOperation.from_openapi_spec(
    spec, "/v1/public/openai/explain-task", "post"
)

# The operation can be serialized as typescript
print(operation.to_typescript())
```

    type explainTask = (_: {
    /* Description of the task that the user wants to accomplish or do. For example, "tell the waiter they messed up my order" or "compliment someone on their shirt" */
      task_description?: string,
    /* The foreign language that the user is learning and asking about. The value can be inferred from question - for example, if the user asks "how do i ask a girl out in mexico city", the value should be "Spanish" because of Mexico City. Always use the full name of the language (e.g. Spanish, French). */
      learning_language?: string,
    /* The user's native language. Infer this value from the language the user asked their question in. Always use the full name of the language (e.g. Spanish, French). */
      native_language?: string,
    /* A description of any additional context in the user's question that could affect the explanation - e.g. setting, scenario, situation, tone, speaking style and formality, usage notes, or any other qualifiers. */
      additional_context?: string,
    /* Full text of the user's question. */
      full_query?: string,
    }) => any;
    


```python
# Compress the service definition to avoid leaking too much input structure to the sample data
template = """In 20 words or less, what does this service accomplish?
{spec}

Function: It's designed to """
prompt = PromptTemplate.from_template(template)
generation_chain = LLMChain(llm=llm, prompt=prompt)
purpose = generation_chain.run(spec=operation.to_typescript())
```


```python
template = """Write a list of {num_to_generate} unique messages users might send to a service designed to{purpose} They must each be completely unique.

1."""


def parse_list(text: str) -> List[str]:
    # Match lines starting with a number then period
    # Strip leading and trailing whitespace
    matches = re.findall(r"^\d+\. ", text)
    return [re.sub(r"^\d+\. ", "", q).strip().strip('"') for q in text.split("\n")]


num_to_generate = 10  # How many examples to use for this test set.
prompt = PromptTemplate.from_template(template)
generation_chain = LLMChain(llm=llm, prompt=prompt)
text = generation_chain.run(purpose=purpose, num_to_generate=num_to_generate)
# Strip preceding numeric bullets
queries = parse_list(text)
queries
```




    ["Can you explain how to say 'hello' in Spanish?",
     "I need help understanding the French word for 'goodbye'.",
     "Can you tell me how to say 'thank you' in German?",
     "I'm trying to learn the Italian word for 'please'.",
     "Can you help me with the pronunciation of 'yes' in Portuguese?",
     "I'm looking for the Dutch word for 'no'.",
     "Can you explain the meaning of 'hello' in Japanese?",
     "I need help understanding the Russian word for 'thank you'.",
     "Can you tell me how to say 'goodbye' in Chinese?",
     "I'm trying to learn the Arabic word for 'please'."]




```python
# Define the generation chain to get hypotheses
api_chain = OpenAPIEndpointChain.from_api_operation(
    operation,
    llm,
    requests=Requests(),
    verbose=verbose,
    return_intermediate_steps=True,  # Return request and response text
)

predicted_outputs = [api_chain(query) for query in queries]
request_args = [
    output["intermediate_steps"]["request_args"] for output in predicted_outputs
]

# Show the generated request
request_args
```




    ['{"task_description": "say \'hello\'", "learning_language": "Spanish", "native_language": "English", "full_query": "Can you explain how to say \'hello\' in Spanish?"}',
     '{"task_description": "understanding the French word for \'goodbye\'", "learning_language": "French", "native_language": "English", "full_query": "I need help understanding the French word for \'goodbye\'."}',
     '{"task_description": "say \'thank you\'", "learning_language": "German", "native_language": "English", "full_query": "Can you tell me how to say \'thank you\' in German?"}',
     '{"task_description": "Learn the Italian word for \'please\'", "learning_language": "Italian", "native_language": "English", "full_query": "I\'m trying to learn the Italian word for \'please\'."}',
     '{"task_description": "Help with pronunciation of \'yes\' in Portuguese", "learning_language": "Portuguese", "native_language": "English", "full_query": "Can you help me with the pronunciation of \'yes\' in Portuguese?"}',
     '{"task_description": "Find the Dutch word for \'no\'", "learning_language": "Dutch", "native_language": "English", "full_query": "I\'m looking for the Dutch word for \'no\'."}',
     '{"task_description": "Explain the meaning of \'hello\' in Japanese", "learning_language": "Japanese", "native_language": "English", "full_query": "Can you explain the meaning of \'hello\' in Japanese?"}',
     '{"task_description": "understanding the Russian word for \'thank you\'", "learning_language": "Russian", "native_language": "English", "full_query": "I need help understanding the Russian word for \'thank you\'."}',
     '{"task_description": "say goodbye", "learning_language": "Chinese", "native_language": "English", "full_query": "Can you tell me how to say \'goodbye\' in Chinese?"}',
     '{"task_description": "Learn the Arabic word for \'please\'", "learning_language": "Arabic", "native_language": "English", "full_query": "I\'m trying to learn the Arabic word for \'please\'."}']




```python
## AI Assisted Correction
correction_template = """Correct the following API request based on the user's feedback. If the user indicates no changes are needed, output the original without making any changes.

REQUEST: {request}

User Feedback / requested changes: {user_feedback}

Finalized Request: """

prompt = PromptTemplate.from_template(correction_template)
correction_chain = LLMChain(llm=llm, prompt=prompt)
```


```python
ground_truth = []
for query, request_arg in list(zip(queries, request_args)):
    feedback = input(f"Query: {query}\nRequest: {request_arg}\nRequested changes: ")
    if feedback == "n" or feedback == "none" or not feedback:
        ground_truth.append(request_arg)
        continue
    resolved = correction_chain.run(request=request_arg, user_feedback=feedback)
    ground_truth.append(resolved.strip())
    print("Updated request:", resolved)
```

    Query: Can you explain how to say 'hello' in Spanish?
    Request: {"task_description": "say 'hello'", "learning_language": "Spanish", "native_language": "English", "full_query": "Can you explain how to say 'hello' in Spanish?"}
    Requested changes: 
    Query: I need help understanding the French word for 'goodbye'.
    Request: {"task_description": "understanding the French word for 'goodbye'", "learning_language": "French", "native_language": "English", "full_query": "I need help understanding the French word for 'goodbye'."}
    Requested changes: 
    Query: Can you tell me how to say 'thank you' in German?
    Request: {"task_description": "say 'thank you'", "learning_language": "German", "native_language": "English", "full_query": "Can you tell me how to say 'thank you' in German?"}
    Requested changes: 
    Query: I'm trying to learn the Italian word for 'please'.
    Request: {"task_description": "Learn the Italian word for 'please'", "learning_language": "Italian", "native_language": "English", "full_query": "I'm trying to learn the Italian word for 'please'."}
    Requested changes: 
    Query: Can you help me with the pronunciation of 'yes' in Portuguese?
    Request: {"task_description": "Help with pronunciation of 'yes' in Portuguese", "learning_language": "Portuguese", "native_language": "English", "full_query": "Can you help me with the pronunciation of 'yes' in Portuguese?"}
    Requested changes: 
    Query: I'm looking for the Dutch word for 'no'.
    Request: {"task_description": "Find the Dutch word for 'no'", "learning_language": "Dutch", "native_language": "English", "full_query": "I'm looking for the Dutch word for 'no'."}
    Requested changes: 
    Query: Can you explain the meaning of 'hello' in Japanese?
    Request: {"task_description": "Explain the meaning of 'hello' in Japanese", "learning_language": "Japanese", "native_language": "English", "full_query": "Can you explain the meaning of 'hello' in Japanese?"}
    Requested changes: 
    Query: I need help understanding the Russian word for 'thank you'.
    Request: {"task_description": "understanding the Russian word for 'thank you'", "learning_language": "Russian", "native_language": "English", "full_query": "I need help understanding the Russian word for 'thank you'."}
    Requested changes: 
    Query: Can you tell me how to say 'goodbye' in Chinese?
    Request: {"task_description": "say goodbye", "learning_language": "Chinese", "native_language": "English", "full_query": "Can you tell me how to say 'goodbye' in Chinese?"}
    Requested changes: 
    Query: I'm trying to learn the Arabic word for 'please'.
    Request: {"task_description": "Learn the Arabic word for 'please'", "learning_language": "Arabic", "native_language": "English", "full_query": "I'm trying to learn the Arabic word for 'please'."}
    Requested changes: 
    

**Now you can use the `ground_truth` as shown above in [Evaluate the Requests Chain](#Evaluate-the-requests-chain)!**


```python
# Now you have a new ground truth set to use as shown above!
ground_truth
```




    ['{"task_description": "say \'hello\'", "learning_language": "Spanish", "native_language": "English", "full_query": "Can you explain how to say \'hello\' in Spanish?"}',
     '{"task_description": "understanding the French word for \'goodbye\'", "learning_language": "French", "native_language": "English", "full_query": "I need help understanding the French word for \'goodbye\'."}',
     '{"task_description": "say \'thank you\'", "learning_language": "German", "native_language": "English", "full_query": "Can you tell me how to say \'thank you\' in German?"}',
     '{"task_description": "Learn the Italian word for \'please\'", "learning_language": "Italian", "native_language": "English", "full_query": "I\'m trying to learn the Italian word for \'please\'."}',
     '{"task_description": "Help with pronunciation of \'yes\' in Portuguese", "learning_language": "Portuguese", "native_language": "English", "full_query": "Can you help me with the pronunciation of \'yes\' in Portuguese?"}',
     '{"task_description": "Find the Dutch word for \'no\'", "learning_language": "Dutch", "native_language": "English", "full_query": "I\'m looking for the Dutch word for \'no\'."}',
     '{"task_description": "Explain the meaning of \'hello\' in Japanese", "learning_language": "Japanese", "native_language": "English", "full_query": "Can you explain the meaning of \'hello\' in Japanese?"}',
     '{"task_description": "understanding the Russian word for \'thank you\'", "learning_language": "Russian", "native_language": "English", "full_query": "I need help understanding the Russian word for \'thank you\'."}',
     '{"task_description": "say goodbye", "learning_language": "Chinese", "native_language": "English", "full_query": "Can you tell me how to say \'goodbye\' in Chinese?"}',
     '{"task_description": "Learn the Arabic word for \'please\'", "learning_language": "Arabic", "native_language": "English", "full_query": "I\'m trying to learn the Arabic word for \'please\'."}']




```python

```
