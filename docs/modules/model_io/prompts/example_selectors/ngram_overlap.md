## n-gram重叠选择法

`NGramOverlapExampleSelector`根据示例与输入之间的n-gram重叠程度选择和排序示例。n-gram重叠得分是一个在0.0到1.0之间（包括边界）的浮点数。

选择器允许设置阈值分数。n-gram重叠得分小于或等于阈值的示例将被排除在外。默认情况下，阈值设置为-1.0，因此不会排除任何示例，只会重新排序它们。将阈值设置为0.0将排除与输入没有n-gram重叠的示例。



```python
from langchain.prompts import PromptTemplate
from langchain.prompts.example_selector.ngram_overlap import NGramOverlapExampleSelector
from langchain.prompts import FewShotPromptTemplate, PromptTemplate

example_prompt = PromptTemplate(
    input_variables=["input", "output"],
    template="Input: {input}\nOutput: {output}",
)

# These are a lot of examples of a pretend task of creating antonyms.
examples = [
    {"input": "happy", "output": "sad"},
    {"input": "tall", "output": "short"},
    {"input": "energetic", "output": "lethargic"},
    {"input": "sunny", "output": "gloomy"},
    {"input": "windy", "output": "calm"},
]
```


```python
# These are examples of a fictional translation task.
examples = [
    {"input": "See Spot run.", "output": "Ver correr a Spot."},
    {"input": "My dog barks.", "output": "Mi perro ladra."},
    {"input": "Spot can run.", "output": "Spot puede correr."},
]
```


```python
example_prompt = PromptTemplate(
    input_variables=["input", "output"],
    template="Input: {input}\nOutput: {output}",
)
example_selector = NGramOverlapExampleSelector(
    # These are the examples it has available to choose from.
    examples=examples,
    # This is the PromptTemplate being used to format the examples.
    example_prompt=example_prompt,
    # This is the threshold, at which selector stops.
    # It is set to -1.0 by default.
    threshold=-1.0,
    # For negative threshold:
    # Selector sorts examples by ngram overlap score, and excludes none.
    # For threshold greater than 1.0:
    # Selector excludes all examples, and returns an empty list.
    # For threshold equal to 0.0:
    # Selector sorts examples by ngram overlap score,
    # and excludes those with no ngram overlap with input.
)
dynamic_prompt = FewShotPromptTemplate(
    # We provide an ExampleSelector instead of examples.
    example_selector=example_selector,
    example_prompt=example_prompt,
    prefix="Give the Spanish translation of every input",
    suffix="Input: {sentence}\nOutput:",
    input_variables=["sentence"],
)
```


```python
# An example input with large ngram overlap with "Spot can run."
# and no overlap with "My dog barks."
print(dynamic_prompt.format(sentence="Spot can run fast."))
```

    Give the Spanish translation of every input
    
    Input: Spot can run.
    Output: Spot puede correr.
    
    Input: See Spot run.
    Output: Ver correr a Spot.
    
    Input: My dog barks.
    Output: Mi perro ladra.
    
    Input: Spot can run fast.
    Output:
    


```python
# You can add examples to NGramOverlapExampleSelector as well.
new_example = {"input": "Spot plays fetch.", "output": "Spot juega a buscar."}

example_selector.add_example(new_example)
print(dynamic_prompt.format(sentence="Spot can run fast."))
```

    Give the Spanish translation of every input
    
    Input: Spot can run.
    Output: Spot puede correr.
    
    Input: See Spot run.
    Output: Ver correr a Spot.
    
    Input: Spot plays fetch.
    Output: Spot juega a buscar.
    
    Input: My dog barks.
    Output: Mi perro ladra.
    
    Input: Spot can run fast.
    Output:
    


```python
# You can set a threshold at which examples are excluded.
# For example, setting threshold equal to 0.0
# excludes examples with no ngram overlaps with input.
# Since "My dog barks." has no ngram overlaps with "Spot can run fast."
# it is excluded.
example_selector.threshold = 0.0
print(dynamic_prompt.format(sentence="Spot can run fast."))
```

    Give the Spanish translation of every input
    
    Input: Spot can run.
    Output: Spot puede correr.
    
    Input: See Spot run.
    Output: Ver correr a Spot.
    
    Input: Spot plays fetch.
    Output: Spot juega a buscar.
    
    Input: Spot can run fast.
    Output:
    


```python
# Setting small nonzero threshold
example_selector.threshold = 0.09
print(dynamic_prompt.format(sentence="Spot can play fetch."))
```

    Give the Spanish translation of every input
    
    Input: Spot can run.
    Output: Spot puede correr.
    
    Input: Spot plays fetch.
    Output: Spot juega a buscar.
    
    Input: Spot can play fetch.
    Output:
    


```python
# Setting threshold greater than 1.0
example_selector.threshold = 1.0 + 1e-9
print(dynamic_prompt.format(sentence="Spot can play fetch."))
```

    Give the Spanish translation of every input
    
    Input: Spot can play fetch.
    Output:
    


```python

```
