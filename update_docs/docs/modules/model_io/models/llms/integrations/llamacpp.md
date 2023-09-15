# Llama-cpp

[llama-cpp](https://github.com/abetlen/llama-cpp-python) is a Python binding for [llama.cpp](https://github.com/ggerganov/llama.cpp). 
It supports [several LLMs](https://github.com/ggerganov/llama.cpp).

This notebook goes over how to run `llama-cpp` within LangChain.

## Installation

There is a banch of options how to install the llama-cpp package: 
- only CPU usage
- CPU + GPU (using one of many BLAS backends)

### CPU only installation


```python
!pip install llama-cpp-python
```

### Installation with OpenBLAS / cuBLAS / CLBlast

`lama.cpp` supports multiple BLAS backends for faster processing. Use the `FORCE_CMAKE=1` environment variable to force the use of cmake and install the pip package for the desired BLAS backend ([source](https://github.com/abetlen/llama-cpp-python#installation-with-openblas--cublas--clblast)).

Example installation with cuBLAS backend:


```python
!CMAKE_ARGS="-DLLAMA_CUBLAS=on" FORCE_CMAKE=1 pip install llama-cpp-python
```

**IMPORTANT**: If you have already installed a cpu only version of the package, you need to reinstall it from scratch: condiser the following command: 


```python
!CMAKE_ARGS="-DLLAMA_CUBLAS=on" FORCE_CMAKE=1 pip install --upgrade --force-reinstall llama-cpp-python
```

## Usage

Make sure you are following all instructions to [install all necessary model files](https://github.com/ggerganov/llama.cpp).

You don't need an `API_TOKEN`!


```python
from langchain.llms import LlamaCpp
from langchain import PromptTemplate, LLMChain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
```

**Consider using a template that suits your model! Check the models page on HuggingFace etc. to get a correct prompting template.**


```python
template = """Question: {question}

Answer: Let's work this out in a step by step way to be sure we have the right answer."""

prompt = PromptTemplate(template=template, input_variables=["question"])
```


```python
# Callbacks support token-wise streaming
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
# Verbose is required to pass to the callback manager
```

### CPU


```python
# Make sure the model path is correct for your system!
llm = LlamaCpp(
    model_path="./ggml-model-q4_0.bin", callback_manager=callback_manager, verbose=True
)
```


```python
llm_chain = LLMChain(prompt=prompt, llm=llm)
```


```python
question = "What NFL team won the Super Bowl in the year Justin Bieber was born?"

llm_chain.run(question)
```

    
    
    1. First, find out when Justin Bieber was born.
    2. We know that Justin Bieber was born on March 1, 1994.
    3. Next, we need to look up when the Super Bowl was played in that year.
    4. The Super Bowl was played on January 28, 1995.
    5. Finally, we can use this information to answer the question. The NFL team that won the Super Bowl in the year Justin Bieber was born is the San Francisco 49ers.

    
    llama_print_timings:        load time =   434.15 ms
    llama_print_timings:      sample time =    41.81 ms /   121 runs   (    0.35 ms per token)
    llama_print_timings: prompt eval time =  2523.78 ms /    48 tokens (   52.58 ms per token)
    llama_print_timings:        eval time = 23971.57 ms /   121 runs   (  198.11 ms per token)
    llama_print_timings:       total time = 28945.95 ms
    




    '\n\n1. First, find out when Justin Bieber was born.\n2. We know that Justin Bieber was born on March 1, 1994.\n3. Next, we need to look up when the Super Bowl was played in that year.\n4. The Super Bowl was played on January 28, 1995.\n5. Finally, we can use this information to answer the question. The NFL team that won the Super Bowl in the year Justin Bieber was born is the San Francisco 49ers.'



### GPU

If the installation with BLAS backend was correct, you will see an `BLAS = 1` indicator in model properties.

Two of the most important parameters for use with GPU are:

- `n_gpu_layers` - determines how many layers of the model are offloaded to your GPU.
- `n_batch` - how many tokens are processed in parallel. 

Setting these parameters correctly will dramatically improve the evaluation speed (see [wrapper code](https://github.com/mmagnesium/langchain/blob/master/langchain/llms/llamacpp.py) for more details).


```python
n_gpu_layers = 40  # Change this value based on your model and your GPU VRAM pool.
n_batch = 512  # Should be between 1 and n_ctx, consider the amount of VRAM in your GPU.

# Make sure the model path is correct for your system!
llm = LlamaCpp(
    model_path="./ggml-model-q4_0.bin",
    n_gpu_layers=n_gpu_layers,
    n_batch=n_batch,
    callback_manager=callback_manager,
    verbose=True,
)
```


```python
llm_chain = LLMChain(prompt=prompt, llm=llm)
```


```python
question = "What NFL team won the Super Bowl in the year Justin Bieber was born?"

llm_chain.run(question)
```

     We are looking for an NFL team that won the Super Bowl when Justin Bieber (born March 1, 1994) was born. 
    
    First, let's look up which year is closest to when Justin Bieber was born:
    
    * The year before he was born: 1993
    * The year of his birth: 1994
    * The year after he was born: 1995
    
    We want to know what NFL team won the Super Bowl in the year that is closest to when Justin Bieber was born. Therefore, we should look up the NFL team that won the Super Bowl in either 1993 or 1994.
    
    Now let's find out which NFL team did win the Super Bowl in either of those years:
    
    * In 1993, the San Francisco 49ers won the Super Bowl against the Dallas Cowboys by a score of 20-16.
    * In 1994, the San Francisco 49ers won the Super Bowl again, this time against the San Diego Chargers by a score of 49-26.
    

    
    llama_print_timings:        load time =   238.10 ms
    llama_print_timings:      sample time =    84.23 ms /   256 runs   (    0.33 ms per token)
    llama_print_timings: prompt eval time =   238.04 ms /    49 tokens (    4.86 ms per token)
    llama_print_timings:        eval time = 10391.96 ms /   255 runs   (   40.75 ms per token)
    llama_print_timings:       total time = 15664.80 ms
    




    " We are looking for an NFL team that won the Super Bowl when Justin Bieber (born March 1, 1994) was born. \n\nFirst, let's look up which year is closest to when Justin Bieber was born:\n\n* The year before he was born: 1993\n* The year of his birth: 1994\n* The year after he was born: 1995\n\nWe want to know what NFL team won the Super Bowl in the year that is closest to when Justin Bieber was born. Therefore, we should look up the NFL team that won the Super Bowl in either 1993 or 1994.\n\nNow let's find out which NFL team did win the Super Bowl in either of those years:\n\n* In 1993, the San Francisco 49ers won the Super Bowl against the Dallas Cowboys by a score of 20-16.\n* In 1994, the San Francisco 49ers won the Super Bowl again, this time against the San Diego Chargers by a score of 49-26.\n"




```python

```
