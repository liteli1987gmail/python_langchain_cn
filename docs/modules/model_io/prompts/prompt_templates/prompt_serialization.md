# 序列化 （Serialization）

通常最好将提示存储为文件而不是Python代码。这样可以方便地共享、存储和版本化提示。本笔记本将介绍如何在LangChain中进行序列化，同时介绍了不同类型的提示和不同的序列化选项。

在高层次上，序列化遵循以下设计原则：

1. 支持JSON和YAML。我们希望支持人类在磁盘上可读的序列化方法，而YAML和JSON是其中最流行的方法之一。请注意，此规则适用于提示。对于其他资产，如示例，可能支持不同的序列化方法。

2. 我们支持将所有内容都存储在一个文件中，或者将不同的组件（模板、示例等）存储在不同的文件中并进行引用。对于某些情况，将所有内容存储在一个文件中是最合理的，但对于其他情况，最好拆分一些资产（长模板、大型示例、可复用组件）。LangChain同时支持两种方式。

还有一个单一入口点可以从磁盘加载提示，这样可以轻松加载任何类型的提示。

```python
# 所有的提示都通过`load_prompt`函数加载。
from langchain.prompts import load_prompt
```

## PromptTemplate

本部分涵盖了加载PromptTemplate的示例。

### 从YAML加载
下面是从YAML加载PromptTemplate的示例。


```python
!cat simple_prompt.yaml
```

    _type: prompt

    input_variables:

        ["adjective", "content"]

    template: 

        Tell me a {adjective} joke about {content}.




```python
prompt = load_prompt("simple_prompt.yaml")
print(prompt.format(adjective="funny", content="chickens"))
```

    Tell me a funny joke about chickens.
    

### Loading from JSON
This shows an example of loading a PromptTemplate from JSON.


```python
!cat simple_prompt.json
```

    {

        "_type": "prompt",

        "input_variables": ["adjective", "content"],

        "template": "Tell me a {adjective} joke about {content}."

    }




```python
prompt = load_prompt("simple_prompt.json")
print(prompt.format(adjective="funny", content="chickens"))
```

Tell me a funny joke about chickens.

### Loading Template from a File
This shows an example of storing the template in a separate file and then referencing it in the config. Notice that the key changes from `template` to `template_path`.


```python
!cat simple_template.txt
```

    Tell me a {adjective} joke about {content}.


```python
!cat simple_prompt_with_template_file.json
```

    {

        "_type": "prompt",

        "input_variables": ["adjective", "content"],

        "template_path": "simple_template.txt"

    }




```python
prompt = load_prompt("simple_prompt_with_template_file.json")
print(prompt.format(adjective="funny", content="chickens"))
```

    Tell me a funny joke about chickens.
    

## FewShotPromptTemplate

This section covers examples for loading few shot prompt templates.

### Examples
This shows an example of what examples stored as json might look like.


```python
!cat examples.json
```

    [

        {"input": "happy", "output": "sad"},

        {"input": "tall", "output": "short"}

    ]



And here is what the same examples stored as yaml might look like.


```python
!cat examples.yaml
```

    - input: happy

      output: sad

    - input: tall

      output: short



### Loading from YAML
This shows an example of loading a few shot example from YAML.


```python
!cat few_shot_prompt.yaml
```

    _type: few_shot

    input_variables:

        ["adjective"]

    prefix: 

        Write antonyms for the following words.

    example_prompt:

        _type: prompt

        input_variables:

            ["input", "output"]

        template:

            "Input: {input}\nOutput: {output}"

    examples:

        examples.json

    suffix:

        "Input: {adjective}\nOutput:"




```python
prompt = load_prompt("few_shot_prompt.yaml")
print(prompt.format(adjective="funny"))
```

    Write antonyms for the following words.
    
    Input: happy
    Output: sad
    
    Input: tall
    Output: short
    
    Input: funny
    Output:
    

The same would work if you loaded examples from the yaml file.


```python
!cat few_shot_prompt_yaml_examples.yaml
```

    _type: few_shot

    input_variables:

        ["adjective"]

    prefix: 

        Write antonyms for the following words.

    example_prompt:

        _type: prompt

        input_variables:

            ["input", "output"]

        template:

            "Input: {input}\nOutput: {output}"

    examples:

        examples.yaml

    suffix:

        "Input: {adjective}\nOutput:"




```python
prompt = load_prompt("few_shot_prompt_yaml_examples.yaml")
print(prompt.format(adjective="funny"))
```

    Write antonyms for the following words.
    
    Input: happy
    Output: sad
    
    Input: tall
    Output: short
    
    Input: funny
    Output:
    

### Loading from JSON
This shows an example of loading a few shot example from JSON.


```python
!cat few_shot_prompt.json
```

    {

        "_type": "few_shot",

        "input_variables": ["adjective"],

        "prefix": "Write antonyms for the following words.",

        "example_prompt": {

            "_type": "prompt",

            "input_variables": ["input", "output"],

            "template": "Input: {input}\nOutput: {output}"

        },

        "examples": "examples.json",

        "suffix": "Input: {adjective}\nOutput:"

    }   




```python
prompt = load_prompt("few_shot_prompt.json")
print(prompt.format(adjective="funny"))
```

    Write antonyms for the following words.
    
    Input: happy
    Output: sad
    
    Input: tall
    Output: short
    
    Input: funny
    Output:
    

### Examples in the Config
This shows an example of referencing the examples directly in the config.


```python
!cat few_shot_prompt_examples_in.json
```

    {

        "_type": "few_shot",

        "input_variables": ["adjective"],

        "prefix": "Write antonyms for the following words.",

        "example_prompt": {

            "_type": "prompt",

            "input_variables": ["input", "output"],

            "template": "Input: {input}\nOutput: {output}"

        },

        "examples": [

            {"input": "happy", "output": "sad"},

            {"input": "tall", "output": "short"}

        ],

        "suffix": "Input: {adjective}\nOutput:"

    }   




```python
prompt = load_prompt("few_shot_prompt_examples_in.json")
print(prompt.format(adjective="funny"))
```

    Write antonyms for the following words.
    
    Input: happy
    Output: sad
    
    Input: tall
    Output: short
    
    Input: funny
    Output:
    

### Example Prompt from a File
This shows an example of loading the PromptTemplate that is used to format the examples from a separate file. Note that the key changes from `example_prompt` to `example_prompt_path`.


```python
!cat example_prompt.json
```

    {

        "_type": "prompt",

        "input_variables": ["input", "output"],

        "template": "Input: {input}\nOutput: {output}" 

    }




```python
!cat few_shot_prompt_example_prompt.json
```

    {

        "_type": "few_shot",

        "input_variables": ["adjective"],

        "prefix": "Write antonyms for the following words.",

        "example_prompt_path": "example_prompt.json",

        "examples": "examples.json",

        "suffix": "Input: {adjective}\nOutput:"

    }   




```python
prompt = load_prompt("few_shot_prompt_example_prompt.json")
print(prompt.format(adjective="funny"))
```

    Write antonyms for the following words.
    
    Input: happy
    Output: sad
    
    Input: tall
    Output: short
    
    Input: funny
    Output:
    

## PromptTempalte with OutputParser
This shows an example of loading a prompt along with an OutputParser from a file.


```python
! cat prompt_with_output_parser.json
```

    {

        "input_variables": [

            "question",

            "student_answer"

        ],

        "output_parser": {

            "regex": "(.*?)\\nScore: (.*)",

            "output_keys": [

                "answer",

                "score"

            ],

            "default_output_key": null,

            "_type": "regex_parser"

        },

        "partial_variables": {},

        "template": "Given the following question and student answer, provide a correct answer and score the student answer.\nQuestion: {question}\nStudent Answer: {student_answer}\nCorrect Answer:",

        "template_format": "f-string",

        "validate_template": true,

        "_type": "prompt"

    }


```python
prompt = load_prompt("prompt_with_output_parser.json")
```


```python
prompt.output_parser.parse(
    "George Washington was born in 1732 and died in 1799.\nScore: 1/2"
)
```




    {'answer': 'George Washington was born in 1732 and died in 1799.',
     'score': '1/2'}


