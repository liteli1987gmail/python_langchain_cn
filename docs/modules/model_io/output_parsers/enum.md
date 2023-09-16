# 枚举解析器

本笔记本演示如何使用枚举输出解析器。


```python
from langchain.output_parsers.enum import EnumOutputParser
```


```python
from enum import Enum


class Colors(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"
```


```python
parser = EnumOutputParser(enum=Colors)
```


```python
parser.parse("red")
```




    <Colors.RED: 'red'>




```python
# Can handle spaces
parser.parse(" green")
```




    <Colors.GREEN: 'green'>




```python
# And new lines
parser.parse("blue\n")
```




    <Colors.BLUE: 'blue'>




```python
# And raises errors when appropriate
parser.parse("yellow")
```


    ---------------------------------------------------------------------------

    ValueError                                Traceback (most recent call last)

    File ~/workplace/langchain/langchain/output_parsers/enum.py:25, in EnumOutputParser.parse(self, response)
         24 try:
    ---> 25     return self.enum(response.strip())
         26 except ValueError:
    

    File ~/.pyenv/versions/3.9.1/lib/python3.9/enum.py:315, in EnumMeta.__call__(cls, value, names, module, qualname, type, start)
        314 if names is None:  # simple value lookup
    --> 315     return cls.__new__(cls, value)
        316 # otherwise, functional API: we're creating a new Enum type
    

    File ~/.pyenv/versions/3.9.1/lib/python3.9/enum.py:611, in Enum.__new__(cls, value)
        610 if result is None and exc is None:
    --> 611     raise ve_exc
        612 elif exc is None:
    

    ValueError: 'yellow' is not a valid Colors

    
    During handling of the above exception, another exception occurred:
    

    OutputParserException                     Traceback (most recent call last)

    Cell In[8], line 2
          1 # And raises errors when appropriate
    ----> 2 parser.parse("yellow")
    

    File ~/workplace/langchain/langchain/output_parsers/enum.py:27, in EnumOutputParser.parse(self, response)
         25     return self.enum(response.strip())
         26 except ValueError:
    ---> 27     raise OutputParserException(
         28         f"Response '{response}' is not one of the "
         29         f"expected values: {self._valid_values}"
         30     )
    

    OutputParserException: Response 'yellow' is not one of the expected values: ['red', 'green', 'blue']



```python

```
