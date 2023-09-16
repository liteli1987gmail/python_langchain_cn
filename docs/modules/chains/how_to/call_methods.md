# 不同的调用方法

所有从 `Chain` 继承的类都提供了几种运行链逻辑的方式。最直接的一种是使用 `__call__`:


```python
chat = ChatOpenAI(temperature=0)
prompt_template = "Tell me a {adjective} joke"
llm_chain = LLMChain(llm=chat, prompt=PromptTemplate.from_template(prompt_template))

llm_chain(inputs={"adjective": "corny"})
```




    {'adjective': 'corny',
     'text': 'Why did the tomato turn red? Because it saw the salad dressing!'}



默认情况下，`__call__` 返回输入和输出键值。您可以通过将 `return_only_outputs` 设置为 `True` 来配置它仅返回输出键值。


```python
llm_chain("corny", return_only_outputs=True)
```




    {'text': 'Why did the tomato turn red? Because it saw the salad dressing!'}



如果 `Chain` 只输出一个输出键（即其 `output_keys` 中只有一个元素），则可以使用 `run` 方法。注意，`run` 输出的是字符串而不是字典。


```python
# llm_chain 只有一个输出键，所以我们可以使用 run
llm_chain.output_keys
```




    ['text']




```python
llm_chain.run({"adjective": "corny"})
```




    'Why did the tomato turn red? Because it saw the salad dressing!'



在只有一个输入键的情况下，您可以直接输入字符串而不指定输入映射。


```python
# 这两种方式是等效的
llm_chain.run({"adjective": "corny"})
llm_chain.run("corny")

# 这两种方式也是等效的
llm_chain("corny")
llm_chain({"adjective": "corny"})
```




    {'adjective': 'corny',
     'text': 'Why did the tomato turn red? Because it saw the salad dressing!'}



提示：您可以通过其 `run` 方法轻松地将 `Chain` 对象作为 `Agent` 中的 `Tool` 集成。在此处查看一个示例 [here](../agents/tools/custom_tools.html)。
