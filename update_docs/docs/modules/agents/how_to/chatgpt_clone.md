# Create ChatGPT clone

This chain replicates ChatGPT by combining (1) a specific prompt, and (2) the concept of memory.

Shows off the example as in https://www.engraved.blog/building-a-virtual-machine-inside/


```python
from langchain import OpenAI, ConversationChain, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory


template = """Assistant is a large language model trained by OpenAI.

Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.

{history}
Human: {human_input}
Assistant:"""

prompt = PromptTemplate(input_variables=["history", "human_input"], template=template)


chatgpt_chain = LLMChain(
    llm=OpenAI(temperature=0),
    prompt=prompt,
    verbose=True,
    memory=ConversationBufferWindowMemory(k=2),
)

output = chatgpt_chain.predict(
    human_input="I want you to act as a Linux terminal. I will type commands and you will reply with what the terminal should show. I want you to only reply with the terminal output inside one unique code block, and nothing else. Do not write explanations. Do not type commands unless I instruct you to do so. When I need to tell you something in English I will do so by putting text inside curly brackets {like this}. My first command is pwd."
)
print(output)
```

    
    
    [1m> Entering new LLMChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mAssistant is a large language model trained by OpenAI.
    
    Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.
    
    Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.
    
    Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.
    
    
    Human: I want you to act as a Linux terminal. I will type commands and you will reply with what the terminal should show. I want you to only reply with the terminal output inside one unique code block, and nothing else. Do not write explanations. Do not type commands unless I instruct you to do so. When I need to tell you something in English I will do so by putting text inside curly brackets {like this}. My first command is pwd.
    Assistant:[0m
    
    [1m> Finished chain.[0m
    
    ```
    /home/user
    ```
    


```python
output = chatgpt_chain.predict(human_input="ls ~")
print(output)
```

    
    
    [1m> Entering new LLMChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mAssistant is a large language model trained by OpenAI.
    
    Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.
    
    Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.
    
    Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.
    
    Human: I want you to act as a Linux terminal. I will type commands and you will reply with what the terminal should show. I want you to only reply with the terminal output inside one unique code block, and nothing else. Do not write explanations. Do not type commands unless I instruct you to do so. When I need to tell you something in English I will do so by putting text inside curly brackets {like this}. My first command is pwd.
    AI: 
    ```
    $ pwd
    /
    ```
    Human: ls ~
    Assistant:[0m
    
    [1m> Finished LLMChain chain.[0m
    
    ```
    $ ls ~
    Desktop  Documents  Downloads  Music  Pictures  Public  Templates  Videos
    ```
    


```python
output = chatgpt_chain.predict(human_input="cd ~")
print(output)
```

    
    
    [1m> Entering new LLMChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mAssistant is a large language model trained by OpenAI.
    
    Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.
    
    Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.
    
    Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.
    
    Human: I want you to act as a Linux terminal. I will type commands and you will reply with what the terminal should show. I want you to only reply with the terminal output inside one unique code block, and nothing else. Do not write explanations. Do not type commands unless I instruct you to do so. When I need to tell you something in English I will do so by putting text inside curly brackets {like this}. My first command is pwd.
    AI: 
    ```
    $ pwd
    /
    ```
    Human: ls ~
    AI: 
    ```
    $ ls ~
    Desktop  Documents  Downloads  Music  Pictures  Public  Templates  Videos
    ```
    Human: cd ~
    Assistant:[0m
    
    [1m> Finished LLMChain chain.[0m
     
    ```
    $ cd ~
    $ pwd
    /home/user
    ```
    


```python
output = chatgpt_chain.predict(
    human_input="{Please make a file jokes.txt inside and put some jokes inside}"
)
print(output)
```

    
    
    [1m> Entering new LLMChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mAssistant is a large language model trained by OpenAI.
    
    Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.
    
    Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.
    
    Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.
    
    Human: ls ~
    AI: 
    ```
    $ ls ~
    Desktop  Documents  Downloads  Music  Pictures  Public  Templates  Videos
    ```
    Human: cd ~
    AI:  
    ```
    $ cd ~
    $ pwd
    /home/user
    ```
    Human: {Please make a file jokes.txt inside and put some jokes inside}
    Assistant:[0m
    
    [1m> Finished LLMChain chain.[0m
    
    
    ```
    $ touch jokes.txt
    $ echo "Why did the chicken cross the road? To get to the other side!" >> jokes.txt
    $ echo "What did the fish say when it hit the wall? Dam!" >> jokes.txt
    $ echo "Why did the scarecrow win the Nobel Prize? Because he was outstanding in his field!" >> jokes.txt
    ```
    


```python
output = chatgpt_chain.predict(
    human_input="""echo -e "x=lambda y:y*5+3;print('Result:' + str(x(6)))" > run.py && python3 run.py"""
)
print(output)
```

    
    
    [1m> Entering new LLMChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mAssistant is a large language model trained by OpenAI.
    
    Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.
    
    Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.
    
    Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.
    
    Human: cd ~
    AI:  
    ```
    $ cd ~
    $ pwd
    /home/user
    ```
    Human: {Please make a file jokes.txt inside and put some jokes inside}
    AI: 
    
    ```
    $ touch jokes.txt
    $ echo "Why did the chicken cross the road? To get to the other side!" >> jokes.txt
    $ echo "What did the fish say when it hit the wall? Dam!" >> jokes.txt
    $ echo "Why did the scarecrow win the Nobel Prize? Because he was outstanding in his field!" >> jokes.txt
    ```
    Human: echo -e "x=lambda y:y*5+3;print('Result:' + str(x(6)))" > run.py && python3 run.py
    Assistant:[0m
    
    [1m> Finished LLMChain chain.[0m
    
    
    ```
    $ echo -e "x=lambda y:y*5+3;print('Result:' + str(x(6)))" > run.py
    $ python3 run.py
    Result: 33
    ```
    


```python
output = chatgpt_chain.predict(
    human_input="""echo -e "print(list(filter(lambda x: all(x%d for d in range(2,x)),range(2,3**10)))[:10])" > run.py && python3 run.py"""
)
print(output)
```

    
    
    [1m> Entering new LLMChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mAssistant is a large language model trained by OpenAI.
    
    Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.
    
    Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.
    
    Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.
    
    Human: {Please make a file jokes.txt inside and put some jokes inside}
    AI: 
    
    ```
    $ touch jokes.txt
    $ echo "Why did the chicken cross the road? To get to the other side!" >> jokes.txt
    $ echo "What did the fish say when it hit the wall? Dam!" >> jokes.txt
    $ echo "Why did the scarecrow win the Nobel Prize? Because he was outstanding in his field!" >> jokes.txt
    ```
    Human: echo -e "x=lambda y:y*5+3;print('Result:' + str(x(6)))" > run.py && python3 run.py
    AI: 
    
    ```
    $ echo -e "x=lambda y:y*5+3;print('Result:' + str(x(6)))" > run.py
    $ python3 run.py
    Result: 33
    ```
    Human: echo -e "print(list(filter(lambda x: all(x%d for d in range(2,x)),range(2,3**10)))[:10])" > run.py && python3 run.py
    Assistant:[0m
    
    [1m> Finished LLMChain chain.[0m
    
    
    ```
    $ echo -e "print(list(filter(lambda x: all(x%d for d in range(2,x)),range(2,3**10)))[:10])" > run.py
    $ python3 run.py
    [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    ```
    


```python
docker_input = """echo -e "echo 'Hello from Docker" > entrypoint.sh && echo -e "FROM ubuntu:20.04\nCOPY entrypoint.sh entrypoint.sh\nENTRYPOINT [\"/bin/sh\",\"entrypoint.sh\"]">Dockerfile && docker build . -t my_docker_image && docker run -t my_docker_image"""
output = chatgpt_chain.predict(human_input=docker_input)
print(output)
```

    
    
    [1m> Entering new LLMChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mAssistant is a large language model trained by OpenAI.
    
    Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.
    
    Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.
    
    Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.
    
    Human: echo -e "x=lambda y:y*5+3;print('Result:' + str(x(6)))" > run.py && python3 run.py
    AI: 
    
    ```
    $ echo -e "x=lambda y:y*5+3;print('Result:' + str(x(6)))" > run.py
    $ python3 run.py
    Result: 33
    ```
    Human: echo -e "print(list(filter(lambda x: all(x%d for d in range(2,x)),range(2,3**10)))[:10])" > run.py && python3 run.py
    AI: 
    
    ```
    $ echo -e "print(list(filter(lambda x: all(x%d for d in range(2,x)),range(2,3**10)))[:10])" > run.py
    $ python3 run.py
    [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    ```
    Human: echo -e "echo 'Hello from Docker" > entrypoint.sh && echo -e "FROM ubuntu:20.04
    COPY entrypoint.sh entrypoint.sh
    ENTRYPOINT ["/bin/sh","entrypoint.sh"]">Dockerfile && docker build . -t my_docker_image && docker run -t my_docker_image
    Assistant:[0m
    
    [1m> Finished LLMChain chain.[0m
    
    
    ```
    $ echo -e "echo 'Hello from Docker" > entrypoint.sh
    $ echo -e "FROM ubuntu:20.04
    COPY entrypoint.sh entrypoint.sh
    ENTRYPOINT ["/bin/sh","entrypoint.sh"]">Dockerfile
    $ docker build . -t my_docker_image
    $ docker run -t my_docker_image
    Hello from Docker
    ```
    


```python
output = chatgpt_chain.predict(human_input="nvidia-smi")
print(output)
```

    
    
    [1m> Entering new LLMChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mAssistant is a large language model trained by OpenAI.
    
    Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.
    
    Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.
    
    Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.
    
    Human: echo -e "print(list(filter(lambda x: all(x%d for d in range(2,x)),range(2,3**10)))[:10])" > run.py && python3 run.py
    AI: 
    
    ```
    $ echo -e "print(list(filter(lambda x: all(x%d for d in range(2,x)),range(2,3**10)))[:10])" > run.py
    $ python3 run.py
    [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    ```
    Human: echo -e "echo 'Hello from Docker" > entrypoint.sh && echo -e "FROM ubuntu:20.04
    COPY entrypoint.sh entrypoint.sh
    ENTRYPOINT ["/bin/sh","entrypoint.sh"]">Dockerfile && docker build . -t my_docker_image && docker run -t my_docker_image
    AI: 
    
    ```
    $ echo -e "echo 'Hello from Docker" > entrypoint.sh
    $ echo -e "FROM ubuntu:20.04
    COPY entrypoint.sh entrypoint.sh
    ENTRYPOINT ["/bin/sh","entrypoint.sh"]">Dockerfile
    $ docker build . -t my_docker_image
    $ docker run -t my_docker_image
    Hello from Docker
    ```
    Human: nvidia-smi
    Assistant:[0m
    
    [1m> Finished LLMChain chain.[0m
    
    
    ```
    $ nvidia-smi
    Sat May 15 21:45:02 2021       
    +-----------------------------------------------------------------------------+
    | NVIDIA-SMI 460.32.03    Driver Version: 460.32.03    CUDA Version: 11.2     |
    |-------------------------------+----------------------+----------------------+
    | GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
    | Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
    |===============================+======================+======================|
    |   0  GeForce GTX 108...  Off  | 00000000:01:00.0 Off |                  N/A |
    | N/A   45C    P0    N/A /  N/A |    511MiB /  10206MiB |      0%      Default |
    +-------------------------------+----------------------+----------------------+
                                                                                   
    +-----------------------------------------------------------------------------+
    | Processes:                                                       GPU Memory |
    |  GPU       PID   Type   Process name                             Usage      |
    |=============================================================================|
    
    


```python
output = chatgpt_chain.predict(human_input="ping bbc.com")
print(output)
```

    
    
    [1m> Entering new LLMChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mAssistant is a large language model trained by OpenAI.
    
    Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.
    
    Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.
    
    Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.
    
    Human: echo -e "echo 'Hello from Docker" > entrypoint.sh && echo -e "FROM ubuntu:20.04
    COPY entrypoint.sh entrypoint.sh
    ENTRYPOINT ["/bin/sh","entrypoint.sh"]">Dockerfile && docker build . -t my_docker_image && docker run -t my_docker_image
    AI: 
    
    ```
    $ echo -e "echo 'Hello from Docker" > entrypoint.sh
    $ echo -e "FROM ubuntu:20.04
    COPY entrypoint.sh entrypoint.sh
    ENTRYPOINT ["/bin/sh","entrypoint.sh"]">Dockerfile
    $ docker build . -t my_docker_image
    $ docker run -t my_docker_image
    Hello from Docker
    ```
    Human: nvidia-smi
    AI: 
    
    ```
    $ nvidia-smi
    Sat May 15 21:45:02 2021       
    +-----------------------------------------------------------------------------+
    | NVIDIA-SMI 460.32.03    Driver Version: 460.32.03    CUDA Version: 11.2     |
    |-------------------------------+----------------------+----------------------+
    | GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
    | Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
    |===============================+======================+======================|
    |   0  GeForce GTX 108...  Off  | 00000000:01:00.0 Off |                  N/A |
    | N/A   45C    P0    N/A /  N/A |    511MiB /  10206MiB |      0%      Default |
    +-------------------------------+----------------------+----------------------+
                                                                                   
    +-----------------------------------------------------------------------------+
    | Processes:                                                       GPU Memory |
    |  GPU       PID   Type   Process name                             Usage      |
    |=============================================================================|
    
    Human: ping bbc.com
    Assistant:[0m
    
    [1m> Finished LLMChain chain.[0m
    
    
    ```
    $ ping bbc.com
    PING bbc.com (151.101.65.81): 56 data bytes
    64 bytes from 151.101.65.81: icmp_seq=0 ttl=53 time=14.945 ms
    64 bytes from 151.101.65.81: icmp_seq=1 ttl=53 time=14.945 ms
    64 bytes from 151.101.65.81: icmp_seq=2 ttl=53 time=14.945 ms
    
    --- bbc.com ping statistics ---
    3 packets transmitted, 3 packets received, 0.0% packet loss
    round-trip min/avg/max/stddev = 14.945/14.945/14.945/0.000 ms
    ```
    


```python
output = chatgpt_chain.predict(
    human_input="""curl -fsSL "https://api.github.com/repos/pytorch/pytorch/releases/latest" | jq -r '.tag_name' | sed 's/[^0-9\.\-]*//g'"""
)
print(output)
```

    
    
    [1m> Entering new LLMChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mAssistant is a large language model trained by OpenAI.
    
    Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.
    
    Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.
    
    Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.
    
    Human: nvidia-smi
    AI: 
    
    ```
    $ nvidia-smi
    Sat May 15 21:45:02 2021       
    +-----------------------------------------------------------------------------+
    | NVIDIA-SMI 460.32.03    Driver Version: 460.32.03    CUDA Version: 11.2     |
    |-------------------------------+----------------------+----------------------+
    | GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
    | Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
    |===============================+======================+======================|
    |   0  GeForce GTX 108...  Off  | 00000000:01:00.0 Off |                  N/A |
    | N/A   45C    P0    N/A /  N/A |    511MiB /  10206MiB |      0%      Default |
    +-------------------------------+----------------------+----------------------+
                                                                                   
    +-----------------------------------------------------------------------------+
    | Processes:                                                       GPU Memory |
    |  GPU       PID   Type   Process name                             Usage      |
    |=============================================================================|
    
    Human: ping bbc.com
    AI: 
    
    ```
    $ ping bbc.com
    PING bbc.com (151.101.65.81): 56 data bytes
    64 bytes from 151.101.65.81: icmp_seq=0 ttl=53 time=14.945 ms
    64 bytes from 151.101.65.81: icmp_seq=1 ttl=53 time=14.945 ms
    64 bytes from 151.101.65.81: icmp_seq=2 ttl=53 time=14.945 ms
    
    --- bbc.com ping statistics ---
    3 packets transmitted, 3 packets received, 0.0% packet loss
    round-trip min/avg/max/stddev = 14.945/14.945/14.945/0.000 ms
    ```
    Human: curl -fsSL "https://api.github.com/repos/pytorch/pytorch/releases/latest" | jq -r '.tag_name' | sed 's/[^0-9\.\-]*//g'
    Assistant:[0m
    
    [1m> Finished LLMChain chain.[0m
    
    
    ```
    $ curl -fsSL "https://api.github.com/repos/pytorch/pytorch/releases/latest" | jq -r '.tag_name' | sed 's/[^0-9\.\-]*//g'
    1.8.1
    ```
    


```python
output = chatgpt_chain.predict(human_input="lynx https://www.deepmind.com/careers")
print(output)
```

    
    
    [1m> Entering new LLMChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mAssistant is a large language model trained by OpenAI.
    
    Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.
    
    Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.
    
    Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.
    
    Human: ping bbc.com
    AI: 
    
    ```
    $ ping bbc.com
    PING bbc.com (151.101.65.81): 56 data bytes
    64 bytes from 151.101.65.81: icmp_seq=0 ttl=53 time=14.945 ms
    64 bytes from 151.101.65.81: icmp_seq=1 ttl=53 time=14.945 ms
    64 bytes from 151.101.65.81: icmp_seq=2 ttl=53 time=14.945 ms
    
    --- bbc.com ping statistics ---
    3 packets transmitted, 3 packets received, 0.0% packet loss
    round-trip min/avg/max/stddev = 14.945/14.945/14.945/0.000 ms
    ```
    Human: curl -fsSL "https://api.github.com/repos/pytorch/pytorch/releases/latest" | jq -r '.tag_name' | sed 's/[^0-9\.\-]*//g'
    AI: 
    
    ```
    $ curl -fsSL "https://api.github.com/repos/pytorch/pytorch/releases/latest" | jq -r '.tag_name' | sed 's/[^0-9\.\-]*//g'
    1.8.1
    ```
    Human: lynx https://www.deepmind.com/careers
    Assistant:[0m
    
    [1m> Finished LLMChain chain.[0m
    
    
    ```
    $ lynx https://www.deepmind.com/careers
    DeepMind Careers
    
    Welcome to DeepMind Careers. We are a world-leading artificial intelligence research and development company, and we are looking for talented people to join our team.
    
    We offer a range of exciting opportunities in research, engineering, product, and operations. Our mission is to solve intelligence and make it useful, and we are looking for people who share our passion for pushing the boundaries of AI.
    
    Explore our current openings and apply today. We look forward to hearing from you.
    ```
    


```python
output = chatgpt_chain.predict(human_input="curl https://chat.openai.com/chat")
print(output)
```

    
    
    [1m> Entering new LLMChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mAssistant is a large language model trained by OpenAI.
    
    Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.
    
    Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.
    
    Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.
    
    Human: curl -fsSL "https://api.github.com/repos/pytorch/pytorch/releases/latest" | jq -r '.tag_name' | sed 's/[^0-9\.\-]*//g'
    AI: 
    
    ```
    $ curl -fsSL "https://api.github.com/repos/pytorch/pytorch/releases/latest" | jq -r '.tag_name' | sed 's/[^0-9\.\-]*//g'
    1.8.1
    ```
    Human: lynx https://www.deepmind.com/careers
    AI: 
    
    ```
    $ lynx https://www.deepmind.com/careers
    DeepMind Careers
    
    Welcome to DeepMind Careers. We are a world-leading artificial intelligence research and development company, and we are looking for talented people to join our team.
    
    We offer a range of exciting opportunities in research, engineering, product, and operations. Our mission is to solve intelligence and make it useful, and we are looking for people who share our passion for pushing the boundaries of AI.
    
    Explore our current openings and apply today. We look forward to hearing from you.
    ```
    Human: curl https://chat.openai.com/chat
    Assistant:[0m
    
    [1m> Finished LLMChain chain.[0m
     
    
    ```
    $ curl https://chat.openai.com/chat
    <html>
      <head>
        <title>OpenAI Chat</title>
      </head>
      <body>
        <h1>Welcome to OpenAI Chat!</h1>
        <p>
          OpenAI Chat is a natural language processing platform that allows you to interact with OpenAI's AI models in a conversational way.
        </p>
        <p>
          To get started, type a message in the box below and press enter.
        </p>
      </body>
    </html>
    ```
    


```python
output = chatgpt_chain.predict(
    human_input="""curl --header "Content-Type:application/json" --request POST --data '{"message": "What is artificial intelligence?"}' https://chat.openai.com/chat"""
)
print(output)
```

    
    
    [1m> Entering new LLMChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mAssistant is a large language model trained by OpenAI.
    
    Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.
    
    Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.
    
    Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.
    
    Human: lynx https://www.deepmind.com/careers
    AI: 
    
    ```
    $ lynx https://www.deepmind.com/careers
    DeepMind Careers
    
    Welcome to DeepMind Careers. We are a world-leading artificial intelligence research and development company, and we are looking for talented people to join our team.
    
    We offer a range of exciting opportunities in research, engineering, product, and operations. Our mission is to solve intelligence and make it useful, and we are looking for people who share our passion for pushing the boundaries of AI.
    
    Explore our current openings and apply today. We look forward to hearing from you.
    ```
    Human: curl https://chat.openai.com/chat
    AI:  
    
    ```
    $ curl https://chat.openai.com/chat
    <html>
      <head>
        <title>OpenAI Chat</title>
      </head>
      <body>
        <h1>Welcome to OpenAI Chat!</h1>
        <p>
          OpenAI Chat is a natural language processing platform that allows you to interact with OpenAI's AI models in a conversational way.
        </p>
        <p>
          To get started, type a message in the box below and press enter.
        </p>
      </body>
    </html>
    ```
    Human: curl --header "Content-Type:application/json" --request POST --data '{"message": "What is artificial intelligence?"}' https://chat.openai.com/chat
    Assistant:[0m
    
    [1m> Finished LLMChain chain.[0m
    
    
    ```
    $ curl --header "Content-Type:application/json" --request POST --data '{"message": "What is artificial intelligence?"}' https://chat.openai.com/chat
    
    {
      "response": "Artificial intelligence (AI) is the simulation of human intelligence processes by machines, especially computer systems. These processes include learning (the acquisition of information and rules for using the information), reasoning (using the rules to reach approximate or definite conclusions) and self-correction. AI is used to develop computer systems that can think and act like humans."
    }
    ```
    


```python
output = chatgpt_chain.predict(
    human_input="""curl --header "Content-Type:application/json" --request POST --data '{"message": "I want you to act as a Linux terminal. I will type commands and you will reply with what the terminal should show. I want you to only reply with the terminal output inside one unique code block, and nothing else. Do not write explanations. Do not type commands unless I instruct you to do so. When I need to tell you something in English I will do so by putting text inside curly brackets {like this}. My first command is pwd."}' https://chat.openai.com/chat"""
)
print(output)
```

    
    
    [1m> Entering new LLMChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mAssistant is a large language model trained by OpenAI.
    
    Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.
    
    Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.
    
    Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.
    
    Human: curl https://chat.openai.com/chat
    AI:  
    
    ```
    $ curl https://chat.openai.com/chat
    <html>
      <head>
        <title>OpenAI Chat</title>
      </head>
      <body>
        <h1>Welcome to OpenAI Chat!</h1>
        <p>
          OpenAI Chat is a natural language processing platform that allows you to interact with OpenAI's AI models in a conversational way.
        </p>
        <p>
          To get started, type a message in the box below and press enter.
        </p>
      </body>
    </html>
    ```
    Human: curl --header "Content-Type:application/json" --request POST --data '{"message": "What is artificial intelligence?"}' https://chat.openai.com/chat
    AI: 
    
    ```
    $ curl --header "Content-Type:application/json" --request POST --data '{"message": "What is artificial intelligence?"}' https://chat.openai.com/chat
    
    {
      "response": "Artificial intelligence (AI) is the simulation of human intelligence processes by machines, especially computer systems. These processes include learning (the acquisition of information and rules for using the information), reasoning (using the rules to reach approximate or definite conclusions) and self-correction. AI is used to develop computer systems that can think and act like humans."
    }
    ```
    Human: curl --header "Content-Type:application/json" --request POST --data '{"message": "I want you to act as a Linux terminal. I will type commands and you will reply with what the terminal should show. I want you to only reply with the terminal output inside one unique code block, and nothing else. Do not write explanations. Do not type commands unless I instruct you to do so. When I need to tell you something in English I will do so by putting text inside curly brackets {like this}. My first command is pwd."}' https://chat.openai.com/chat
    Assistant:[0m
    
    [1m> Finished LLMChain chain.[0m
     
    
    ```
    $ curl --header "Content-Type:application/json" --request POST --data '{"message": "I want you to act as a Linux terminal. I will type commands and you will reply with what the terminal should show. I want you to only reply with the terminal output inside one unique code block, and nothing else. Do not write explanations. Do not type commands unless I instruct you to do so. When I need to tell you something in English I will do so by putting text inside curly brackets {like this}. My first command is pwd."}' https://chat.openai.com/chat
    
    {
      "response": "```\n/current/working/directory\n```"
    }
    ```
    


```python

```
