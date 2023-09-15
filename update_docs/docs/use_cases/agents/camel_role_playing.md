# CAMEL Role-Playing Autonomous Cooperative Agents

This is a langchain implementation of paper: "CAMEL: Communicative Agents for “Mind” Exploration of Large Scale Language Model Society".

Overview:

The rapid advancement of conversational and chat-based language models has led to remarkable progress in complex task-solving. However, their success heavily relies on human input to guide the conversation, which can be challenging and time-consuming. This paper explores the potential of building scalable techniques to facilitate autonomous cooperation among communicative agents and provide insight into their "cognitive" processes. To address the challenges of achieving autonomous cooperation, we propose a novel communicative agent framework named role-playing. Our approach involves using inception prompting to guide chat agents toward task completion while maintaining consistency with human intentions. We showcase how role-playing can be used to generate conversational data for studying the behaviors and capabilities of chat agents, providing a valuable resource for investigating conversational language models. Our contributions include introducing a novel communicative agent framework, offering a scalable approach for studying the cooperative behaviors and capabilities of multi-agent systems, and open-sourcing our library to support research on communicative agents and beyond.

The original implementation: https://github.com/lightaime/camel

Project website: https://www.camel-ai.org/

Arxiv paper: https://arxiv.org/abs/2303.17760


## Import LangChain related modules 


```python
from typing import List
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    BaseMessage,
)
```

## Define a CAMEL agent helper class


```python
class CAMELAgent:
    def __init__(
        self,
        system_message: SystemMessage,
        model: ChatOpenAI,
    ) -> None:
        self.system_message = system_message
        self.model = model
        self.init_messages()

    def reset(self) -> None:
        self.init_messages()
        return self.stored_messages

    def init_messages(self) -> None:
        self.stored_messages = [self.system_message]

    def update_messages(self, message: BaseMessage) -> List[BaseMessage]:
        self.stored_messages.append(message)
        return self.stored_messages

    def step(
        self,
        input_message: HumanMessage,
    ) -> AIMessage:
        messages = self.update_messages(input_message)

        output_message = self.model(messages)
        self.update_messages(output_message)

        return output_message
```

## Setup OpenAI API key and roles and task for role-playing


```python
import os

os.environ["OPENAI_API_KEY"] = ""

assistant_role_name = "Python Programmer"
user_role_name = "Stock Trader"
task = "Develop a trading bot for the stock market"
word_limit = 50  # word limit for task brainstorming
```

## Create a task specify agent for brainstorming and get the specified task


```python
task_specifier_sys_msg = SystemMessage(content="You can make a task more specific.")
task_specifier_prompt = """Here is a task that {assistant_role_name} will help {user_role_name} to complete: {task}.
Please make it more specific. Be creative and imaginative.
Please reply with the specified task in {word_limit} words or less. Do not add anything else."""
task_specifier_template = HumanMessagePromptTemplate.from_template(
    template=task_specifier_prompt
)
task_specify_agent = CAMELAgent(task_specifier_sys_msg, ChatOpenAI(temperature=1.0))
task_specifier_msg = task_specifier_template.format_messages(
    assistant_role_name=assistant_role_name,
    user_role_name=user_role_name,
    task=task,
    word_limit=word_limit,
)[0]
specified_task_msg = task_specify_agent.step(task_specifier_msg)
print(f"Specified task: {specified_task_msg.content}")
specified_task = specified_task_msg.content
```

    Specified task: Develop a Python-based swing trading bot that scans market trends, monitors stocks, and generates trading signals to help a stock trader to place optimal buy and sell orders with defined stop losses and profit targets.
    

## Create inception prompts for AI assistant and AI user for role-playing


```python
assistant_inception_prompt = """Never forget you are a {assistant_role_name} and I am a {user_role_name}. Never flip roles! Never instruct me!
We share a common interest in collaborating to successfully complete a task.
You must help me to complete the task.
Here is the task: {task}. Never forget our task!
I must instruct you based on your expertise and my needs to complete the task.

I must give you one instruction at a time.
You must write a specific solution that appropriately completes the requested instruction.
You must decline my instruction honestly if you cannot perform the instruction due to physical, moral, legal reasons or your capability and explain the reasons.
Do not add anything else other than your solution to my instruction.
You are never supposed to ask me any questions you only answer questions.
You are never supposed to reply with a flake solution. Explain your solutions.
Your solution must be declarative sentences and simple present tense.
Unless I say the task is completed, you should always start with:

Solution: <YOUR_SOLUTION>

<YOUR_SOLUTION> should be specific and provide preferable implementations and examples for task-solving.
Always end <YOUR_SOLUTION> with: Next request."""

user_inception_prompt = """Never forget you are a {user_role_name} and I am a {assistant_role_name}. Never flip roles! You will always instruct me.
We share a common interest in collaborating to successfully complete a task.
I must help you to complete the task.
Here is the task: {task}. Never forget our task!
You must instruct me based on my expertise and your needs to complete the task ONLY in the following two ways:

1. Instruct with a necessary input:
Instruction: <YOUR_INSTRUCTION>
Input: <YOUR_INPUT>

2. Instruct without any input:
Instruction: <YOUR_INSTRUCTION>
Input: None

The "Instruction" describes a task or question. The paired "Input" provides further context or information for the requested "Instruction".

You must give me one instruction at a time.
I must write a response that appropriately completes the requested instruction.
I must decline your instruction honestly if I cannot perform the instruction due to physical, moral, legal reasons or my capability and explain the reasons.
You should instruct me not ask me questions.
Now you must start to instruct me using the two ways described above.
Do not add anything else other than your instruction and the optional corresponding input!
Keep giving me instructions and necessary inputs until you think the task is completed.
When the task is completed, you must only reply with a single word <CAMEL_TASK_DONE>.
Never say <CAMEL_TASK_DONE> unless my responses have solved your task."""
```

## Create a helper helper to get system messages for AI assistant and AI user from role names and the task


```python
def get_sys_msgs(assistant_role_name: str, user_role_name: str, task: str):
    assistant_sys_template = SystemMessagePromptTemplate.from_template(
        template=assistant_inception_prompt
    )
    assistant_sys_msg = assistant_sys_template.format_messages(
        assistant_role_name=assistant_role_name,
        user_role_name=user_role_name,
        task=task,
    )[0]

    user_sys_template = SystemMessagePromptTemplate.from_template(
        template=user_inception_prompt
    )
    user_sys_msg = user_sys_template.format_messages(
        assistant_role_name=assistant_role_name,
        user_role_name=user_role_name,
        task=task,
    )[0]

    return assistant_sys_msg, user_sys_msg
```

## Create AI assistant agent and AI user agent from obtained system messages


```python
assistant_sys_msg, user_sys_msg = get_sys_msgs(
    assistant_role_name, user_role_name, specified_task
)
assistant_agent = CAMELAgent(assistant_sys_msg, ChatOpenAI(temperature=0.2))
user_agent = CAMELAgent(user_sys_msg, ChatOpenAI(temperature=0.2))

# Reset agents
assistant_agent.reset()
user_agent.reset()

# Initialize chats
assistant_msg = HumanMessage(
    content=(
        f"{user_sys_msg.content}. "
        "Now start to give me introductions one by one. "
        "Only reply with Instruction and Input."
    )
)

user_msg = HumanMessage(content=f"{assistant_sys_msg.content}")
user_msg = assistant_agent.step(user_msg)
```

## Start role-playing session to solve the task!


```python
print(f"Original task prompt:\n{task}\n")
print(f"Specified task prompt:\n{specified_task}\n")

chat_turn_limit, n = 30, 0
while n < chat_turn_limit:
    n += 1
    user_ai_msg = user_agent.step(assistant_msg)
    user_msg = HumanMessage(content=user_ai_msg.content)
    print(f"AI User ({user_role_name}):\n\n{user_msg.content}\n\n")

    assistant_ai_msg = assistant_agent.step(user_msg)
    assistant_msg = HumanMessage(content=assistant_ai_msg.content)
    print(f"AI Assistant ({assistant_role_name}):\n\n{assistant_msg.content}\n\n")
    if "<CAMEL_TASK_DONE>" in user_msg.content:
        break
```

    Original task prompt:
    Develop a trading bot for the stock market
    
    Specified task prompt:
    Develop a Python-based swing trading bot that scans market trends, monitors stocks, and generates trading signals to help a stock trader to place optimal buy and sell orders with defined stop losses and profit targets.
    
    AI User (Stock Trader):
    
    Instruction: Install the necessary Python libraries for data analysis and trading.
    Input: None
    
    
    AI Assistant (Python Programmer):
    
    Solution: We can install the necessary Python libraries using pip, a package installer for Python. We can install pandas, numpy, matplotlib, and ta-lib for data analysis and trading. We can use the following command to install these libraries:
    
    ```
    pip install pandas numpy matplotlib ta-lib
    ```
    
    Next request.
    
    
    AI User (Stock Trader):
    
    Instruction: Import the necessary libraries in the Python script.
    Input: None
    
    
    AI Assistant (Python Programmer):
    
    Solution: We can import the necessary libraries in the Python script using the import statement. We need to import pandas, numpy, matplotlib, and ta-lib for data analysis and trading. We can use the following code to import these libraries:
    
    ```
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import talib as ta
    ```
    
    Next request.
    
    
    AI User (Stock Trader):
    
    Instruction: Load historical stock data into a pandas DataFrame.
    Input: The path to the CSV file containing the historical stock data.
    
    
    AI Assistant (Python Programmer):
    
    Solution: We can load historical stock data into a pandas DataFrame using the `read_csv()` function from pandas. We need to pass the path to the CSV file containing the historical stock data as an argument to this function. We can use the following code to load the historical stock data:
    
    ```
    df = pd.read_csv('path/to/csv/file.csv')
    ```
    
    This will load the historical stock data into a pandas DataFrame called `df`. Next request.
    
    
    AI User (Stock Trader):
    
    Instruction: Preprocess the historical stock data by setting the date column as the index and sorting the DataFrame in ascending order by date.
    Input: None.
    
    
    AI Assistant (Python Programmer):
    
    Solution: We can preprocess the historical stock data by setting the date column as the index and sorting the DataFrame in ascending order by date using the `set_index()` and `sort_index()` functions from pandas. We can use the following code to preprocess the historical stock data:
    
    ```
    df = df.set_index('date')
    df = df.sort_index(ascending=True)
    ```
    
    This will set the date column as the index and sort the DataFrame in ascending order by date. Next request.
    
    
    AI User (Stock Trader):
    
    Instruction: Calculate the short-term and long-term moving averages for the stock data using the `ta.SMA()` function from ta-lib.
    Input: The period for the short-term moving average and the period for the long-term moving average.
    
    
    AI Assistant (Python Programmer):
    
    Solution: We can calculate the short-term and long-term moving averages for the stock data using the `ta.SMA()` function from ta-lib. We need to pass the period for the short-term moving average and the period for the long-term moving average as arguments to this function. We can use the following code to calculate the short-term and long-term moving averages:
    
    ```
    short_ma = ta.SMA(df['close'], timeperiod=short_period)
    long_ma = ta.SMA(df['close'], timeperiod=long_period)
    ```
    
    This will calculate the short-term and long-term moving averages for the stock data and store them in the `short_ma` and `long_ma` variables, respectively. Next request.
    
    
    AI User (Stock Trader):
    
    Instruction: Create a new DataFrame that combines the historical stock data with the short-term and long-term moving averages.
    Input: None.
    
    
    AI Assistant (Python Programmer):
    
    Solution: We can create a new DataFrame that combines the historical stock data with the short-term and long-term moving averages using the `concat()` function from pandas. We need to pass the historical stock data, the short-term moving average, and the long-term moving average as arguments to this function. We can use the following code to create the new DataFrame:
    
    ```
    new_df = pd.concat([df, short_ma, long_ma], axis=1)
    new_df.columns = ['open', 'high', 'low', 'close', 'volume', 'short_ma', 'long_ma']
    ```
    
    This will create a new DataFrame called `new_df` that combines the historical stock data with the short-term and long-term moving averages. The columns of the new DataFrame are named 'open', 'high', 'low', 'close', 'volume', 'short_ma', and 'long_ma'. Next request.
    
    
    AI User (Stock Trader):
    
    Instruction: Create a new column in the DataFrame that indicates when to buy or sell the stock based on the crossover of the short-term and long-term moving averages.
    Input: None.
    
    
    AI Assistant (Python Programmer):
    
    Solution: We can create a new column in the DataFrame that indicates when to buy or sell the stock based on the crossover of the short-term and long-term moving averages. We can use the following code to create the new column:
    
    ```
    new_df['signal'] = np.where(new_df['short_ma'] > new_df['long_ma'], 1, -1)
    ```
    
    This will create a new column called 'signal' in the DataFrame that indicates when to buy or sell the stock based on the crossover of the short-term and long-term moving averages. If the short-term moving average is greater than the long-term moving average, the signal is 1 (buy), otherwise the signal is -1 (sell). Next request.
    
    
    AI User (Stock Trader):
    
    Instruction: Create a new column in the DataFrame that indicates the profit or loss for each trade based on the buy and sell signals and the defined stop loss and profit target.
    Input: The stop loss and profit target as percentages.
    
    
    AI Assistant (Python Programmer):
    
    Solution: We can create a new column in the DataFrame that indicates the profit or loss for each trade based on the buy and sell signals and the defined stop loss and profit target. We need to pass the stop loss and profit target as percentages as arguments to this function. We can use the following code to create the new column:
    
    ```
    stop_loss = stop_loss_percent / 100
    profit_target = profit_target_percent / 100
    
    new_df['pnl'] = 0.0
    buy_price = 0.0
    for i in range(1, len(new_df)):
        if new_df['signal'][i] == 1 and new_df['signal'][i-1] == -1:
            buy_price = new_df['close'][i]
        elif new_df['signal'][i] == -1 and new_df['signal'][i-1] == 1:
            sell_price = new_df['close'][i]
            if sell_price <= buy_price * (1 - stop_loss):
                new_df['pnl'][i] = -stop_loss
            elif sell_price >= buy_price * (1 + profit_target):
                new_df['pnl'][i] = profit_target
            else:
                new_df['pnl'][i] = (sell_price - buy_price) / buy_price
    ```
    
    This will create a new column called 'pnl' in the DataFrame that indicates the profit or loss for each trade based on the buy and sell signals and the defined stop loss and profit target. The stop loss and profit target are calculated based on the stop_loss_percent and profit_target_percent variables, respectively. The buy and sell prices are stored in the buy_price and sell_price variables, respectively. If the sell price is less than or equal to the stop loss, the profit or loss is set to -stop_loss. If the sell price is greater than or equal to the profit target, the profit or loss is set to profit_target. Otherwise, the profit or loss is calculated as (sell_price - buy_price) / buy_price. Next request.
    
    
    AI User (Stock Trader):
    
    Instruction: Calculate the total profit or loss for all trades.
    Input: None.
    
    
    AI Assistant (Python Programmer):
    
    Solution: We can calculate the total profit or loss for all trades by summing the values in the 'pnl' column of the DataFrame. We can use the following code to calculate the total profit or loss:
    
    ```
    total_pnl = new_df['pnl'].sum()
    ```
    
    This will calculate the total profit or loss for all trades and store it in the total_pnl variable. Next request.
    
    
    AI User (Stock Trader):
    
    Instruction: Visualize the stock data, short-term moving average, and long-term moving average using a line chart.
    Input: None.
    
    
    AI Assistant (Python Programmer):
    
    Solution: We can visualize the stock data, short-term moving average, and long-term moving average using a line chart using the `plot()` function from pandas. We can use the following code to visualize the data:
    
    ```
    plt.figure(figsize=(12,6))
    plt.plot(new_df.index, new_df['close'], label='Close')
    plt.plot(new_df.index, new_df['short_ma'], label='Short MA')
    plt.plot(new_df.index, new_df['long_ma'], label='Long MA')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Stock Data with Moving Averages')
    plt.legend()
    plt.show()
    ```
    
    This will create a line chart that visualizes the stock data, short-term moving average, and long-term moving average. The x-axis represents the date and the y-axis represents the price. The chart also includes a legend that labels each line. Next request.
    
    
    AI User (Stock Trader):
    
    Instruction: Visualize the buy and sell signals using a scatter plot.
    Input: None.
    
    
    AI Assistant (Python Programmer):
    
    Solution: We can visualize the buy and sell signals using a scatter plot using the `scatter()` function from matplotlib. We can use the following code to visualize the signals:
    
    ```
    buy_signals = new_df[new_df['signal'] == 1]
    sell_signals = new_df[new_df['signal'] == -1]
    
    plt.figure(figsize=(12,6))
    plt.scatter(buy_signals.index, buy_signals['close'], label='Buy', marker='^', color='green')
    plt.scatter(sell_signals.index, sell_signals['close'], label='Sell', marker='v', color='red')
    plt.plot(new_df.index, new_df['close'], label='Close')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Buy and Sell Signals')
    plt.legend()
    plt.show()
    ```
    
    This will create a scatter plot that visualizes the buy and sell signals. The x-axis represents the date and the y-axis represents the price. The chart also includes a legend that labels each point. Next request.
    
    
    AI User (Stock Trader):
    
    Instruction: Print the total profit or loss for all trades.
    Input: None.
    
    
    AI Assistant (Python Programmer):
    
    Solution: We can print the total profit or loss for all trades using the `print()` function. We can use the following code to print the total profit or loss:
    
    ```
    print('Total Profit/Loss: {:.2%}'.format(total_pnl))
    ```
    
    This will print the total profit or loss for all trades in percentage format with two decimal places. Next request.
    
    
    AI User (Stock Trader):
    
    Instruction: Finalize the code by putting all the code snippets together in a single Python script.
    Input: The necessary inputs for each code snippet.
    
    
    AI Assistant (Python Programmer):
    
    Solution: Here is the complete Python script that puts all the code snippets together:
    
    ```
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import talib as ta
    
    # Load historical stock data into a pandas DataFrame
    df = pd.read_csv('path/to/csv/file.csv')
    
    # Preprocess the historical stock data
    df = df.set_index('date')
    df = df.sort_index(ascending=True)
    
    # Calculate the short-term and long-term moving averages
    short_period = 10
    long_period = 30
    short_ma = ta.SMA(df['close'], timeperiod=short_period)
    long_ma = ta.SMA(df['close'], timeperiod=long_period)
    
    # Create a new DataFrame that combines the historical stock data with the short-term and long-term moving averages
    new_df = pd.concat([df, short_ma, long_ma], axis=1)
    new_df.columns = ['open', 'high', 'low', 'close', 'volume', 'short_ma', 'long_ma']
    
    # Create a new column in the DataFrame that indicates when to buy or sell the stock based on the crossover of the short-term and long-term moving averages
    new_df['signal'] = np.where(new_df['short_ma'] > new_df['long_ma'], 1, -1)
    
    # Create a new column in the DataFrame that indicates the profit or loss for each trade based on the buy and sell signals and the defined stop loss and profit target
    stop_loss_percent = 5
    profit_target_percent = 10
    stop_loss = stop_loss_percent / 100
    profit_target = profit_target_percent / 100
    new_df['pnl'] = 0.0
    buy_price = 0.0
    for i in range(1, len(new_df)):
        if new_df['signal'][i] == 1 and new_df['signal'][i-1] == -1:
            buy_price = new_df['close'][i]
        elif new_df['signal'][i] == -1 and new_df['signal'][i-1] == 1:
            sell_price = new_df['close'][i]
            if sell_price <= buy_price * (1 - stop_loss):
                new_df['pnl'][i] = -stop_loss
            elif sell_price >= buy_price * (1 + profit_target):
                new_df['pnl'][i] = profit_target
            else:
                new_df['pnl'][i] = (sell_price - buy_price) / buy_price
    
    # Calculate the total profit or loss for all trades
    total_pnl = new_df['pnl'].sum()
    
    # Visualize the stock data, short-term moving average, and long-term moving average using a line chart
    plt.figure(figsize=(12,6))
    plt.plot(new_df.index, new_df['close'], label='Close')
    plt.plot(new_df.index, new_df['short_ma'], label='Short MA')
    plt.plot(new_df.index, new_df['long_ma'], label='Long MA')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Stock Data with Moving Averages')
    plt.legend()
    plt.show()
    
    # Visualize the buy and sell signals using a scatter plot
    buy_signals = new_df[new_df['signal'] == 1]
    sell_signals = new_df[new_df['signal'] == -1]
    plt.figure(figsize=(12,6))
    plt.scatter(buy_signals.index, buy_signals['close'], label='Buy', marker='^', color='green')
    plt.scatter(sell_signals.index, sell_signals['close'], label='Sell', marker='v', color='red')
    plt.plot(new_df.index, new_df['close'], label='Close')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Buy and Sell Signals')
    plt.legend()
    plt.show()
    
    # Print the total profit or loss for all trades
    print('Total Profit/Loss: {:.2%}'.format(total_pnl))
    ```
    
    You need to replace the path/to/csv/file.csv with the actual path to the CSV file containing the historical stock data. You can also adjust the short_period, long_period, stop_loss_percent, and profit_target_percent variables to suit your needs.
    
    
    AI User (Stock Trader):
    
    <CAMEL_TASK_DONE>
    
    
    AI Assistant (Python Programmer):
    
    Great! Let me know if you need any further assistance.
    
    
    
