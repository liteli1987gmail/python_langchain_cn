# 自定义提示模板

假设我们希望LLM根据函数名生成英语语言的函数解释。为了实现这个任务，我们将创建一个自定义的提示模板，它以函数名作为输入，并格式化提示模板以提供函数的源代码。

## 为什么需要自定义提示模板？

LangChain提供了一组默认的提示模板，可以用于生成各种任务的提示。然而，可能会有一些情况，其中默认的提示模板无法满足您的需求。例如，您可能希望创建一个具有特定动态指令的提示模板，以适应您的语言模型。在这种情况下，您可以创建一个自定义提示模板。

在[这里](../getting_started.md)查看当前的默认提示模板集合。

## 创建自定义提示模板

基本上有两种不同的提示模板可用-字符串提示模板和聊天提示模板。字符串提示模板提供一个简单的字符串格式提示，而聊天提示模板生成一个更结构化的提示，可用于与聊天API一起使用。

在本指南中，我们将使用字符串提示模板创建自定义提示。

要创建一个自定义的字符串提示模板，需要满足两个要求：
1. 它具有input_variables属性，公开了提示模板预期的输入变量。
2. 它公开了一个format方法，该方法接受与预期的input_variables相对应的关键字参数，并返回格式化后的提示。

我们将创建一个自定义的提示模板，它以函数名作为输入，并格式化提示以提供函数的源代码。为了实现这一点，让我们首先创建一个根据函数名返回函数源代码的函数。


```python
import inspect


def get_source_code(function_name):
    # Get the source code of the function
    return inspect.getsource(function_name)
```

Next, we'll create a custom prompt template that takes in the function name as input, and formats the prompt template to provide the source code of the function.



```python
from langchain.prompts import StringPromptTemplate
from pydantic import BaseModel, validator


class FunctionExplainerPromptTemplate(StringPromptTemplate, BaseModel):
    """A custom prompt template that takes in the function name as input, and formats the prompt template to provide the source code of the function."""

    @validator("input_variables")
    def validate_input_variables(cls, v):
        """Validate that the input variables are correct."""
        if len(v) != 1 or "function_name" not in v:
            raise ValueError("function_name must be the only input_variable.")
        return v

    def format(self, **kwargs) -> str:
        # Get the source code of the function
        source_code = get_source_code(kwargs["function_name"])

        # Generate the prompt to be sent to the language model
        prompt = f"""
        Given the function name and source code, generate an English language explanation of the function.
        Function Name: {kwargs["function_name"].__name__}
        Source Code:
        {source_code}
        Explanation:
        """
        return prompt

    def _prompt_type(self):
        return "function-explainer"
```
## 使用自定义提示模板

现在我们已经创建了一个自定义提示模板，我们可以使用它来为我们的任务生成提示。

```python
fn_explainer = FunctionExplainerPromptTemplate(input_variables=["function_name"])

# 为函数"get_source_code"生成一个提示
prompt = fn_explainer.format(function_name=get_source_code)
print(prompt)
```

    
            给定函数名和源代码，生成该函数的英语语言解释。
            函数名：get_source_code
            源代码：
            def get_source_code(function_name):
        # 获取函数的源代码
        return inspect.getsource(function_name)
    
            解释：
            
    


```python

```