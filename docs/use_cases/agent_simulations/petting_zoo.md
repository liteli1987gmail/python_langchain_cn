# Multi-Agent Simulated Environment: Petting Zoo

In this example, we show how to define multi-agent simulations with simulated environments. Like [ours single-agent example with Gymnasium](https://python.langchain.com/en/latest/use_cases/agent_simulations/gymnasium.html), we create an agent-environment loop with an externally defined environment. The main difference is that we now implement this kind of interaction loop with multiple agents instead. We will use the [Petting Zoo](https://pettingzoo.farama.org/) library, which is the multi-agent counterpart to [Gymnasium](https://gymnasium.farama.org/).

## Install `pettingzoo` and other dependencies


```python
!pip install pettingzoo pygame rlcard
```

## Import modules


```python
import collections
import inspect
import tenacity

from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    HumanMessage,
    SystemMessage,
)
from langchain.output_parsers import RegexParser
```

## `GymnasiumAgent`
Here we reproduce the same `GymnasiumAgent` defined from [our Gymnasium example](https://python.langchain.com/en/latest/use_cases/agent_simulations/gymnasium.html). If after multiple retries it does not take a valid action, it simply takes a random action. 


```python
class GymnasiumAgent:
    @classmethod
    def get_docs(cls, env):
        return env.unwrapped.__doc__

    def __init__(self, model, env):
        self.model = model
        self.env = env
        self.docs = self.get_docs(env)

        self.instructions = """
Your goal is to maximize your return, i.e. the sum of the rewards you receive.
I will give you an observation, reward, terminiation flag, truncation flag, and the return so far, formatted as:

Observation: <observation>
Reward: <reward>
Termination: <termination>
Truncation: <truncation>
Return: <sum_of_rewards>

You will respond with an action, formatted as:

Action: <action>

where you replace <action> with your actual action.
Do nothing else but return the action.
"""
        self.action_parser = RegexParser(
            regex=r"Action: (.*)", output_keys=["action"], default_output_key="action"
        )

        self.message_history = []
        self.ret = 0

    def random_action(self):
        action = self.env.action_space.sample()
        return action

    def reset(self):
        self.message_history = [
            SystemMessage(content=self.docs),
            SystemMessage(content=self.instructions),
        ]

    def observe(self, obs, rew=0, term=False, trunc=False, info=None):
        self.ret += rew

        obs_message = f"""
Observation: {obs}
Reward: {rew}
Termination: {term}
Truncation: {trunc}
Return: {self.ret}
        """
        self.message_history.append(HumanMessage(content=obs_message))
        return obs_message

    def _act(self):
        act_message = self.model(self.message_history)
        self.message_history.append(act_message)
        action = int(self.action_parser.parse(act_message.content)["action"])
        return action

    def act(self):
        try:
            for attempt in tenacity.Retrying(
                stop=tenacity.stop_after_attempt(2),
                wait=tenacity.wait_none(),  # No waiting time between retries
                retry=tenacity.retry_if_exception_type(ValueError),
                before_sleep=lambda retry_state: print(
                    f"ValueError occurred: {retry_state.outcome.exception()}, retrying..."
                ),
            ):
                with attempt:
                    action = self._act()
        except tenacity.RetryError as e:
            action = self.random_action()
        return action
```

## Main loop


```python
def main(agents, env):
    env.reset()

    for name, agent in agents.items():
        agent.reset()

    for agent_name in env.agent_iter():
        observation, reward, termination, truncation, info = env.last()
        obs_message = agents[agent_name].observe(
            observation, reward, termination, truncation, info
        )
        print(obs_message)
        if termination or truncation:
            action = None
        else:
            action = agents[agent_name].act()
        print(f"Action: {action}")
        env.step(action)
    env.close()
```

## `PettingZooAgent`

The `PettingZooAgent` extends the `GymnasiumAgent` to the multi-agent setting. The main differences are:
- `PettingZooAgent` takes in a `name` argument to identify it among multiple agents
- the function `get_docs` is implemented differently because the `PettingZoo` repo structure is structured differently from the `Gymnasium` repo


```python
class PettingZooAgent(GymnasiumAgent):
    @classmethod
    def get_docs(cls, env):
        return inspect.getmodule(env.unwrapped).__doc__

    def __init__(self, name, model, env):
        super().__init__(model, env)
        self.name = name

    def random_action(self):
        action = self.env.action_space(self.name).sample()
        return action
```

## Rock, Paper, Scissors
We can now run a simulation of a multi-agent rock, paper, scissors game using the `PettingZooAgent`.


```python
from pettingzoo.classic import rps_v2

env = rps_v2.env(max_cycles=3, render_mode="human")
agents = {
    name: PettingZooAgent(name=name, model=ChatOpenAI(temperature=1), env=env)
    for name in env.possible_agents
}
main(agents, env)
```

    
    Observation: 3
    Reward: 0
    Termination: False
    Truncation: False
    Return: 0
            
    Action: 1
    
    Observation: 3
    Reward: 0
    Termination: False
    Truncation: False
    Return: 0
            
    Action: 1
    
    Observation: 1
    Reward: 0
    Termination: False
    Truncation: False
    Return: 0
            
    Action: 2
    
    Observation: 1
    Reward: 0
    Termination: False
    Truncation: False
    Return: 0
            
    Action: 1
    
    Observation: 1
    Reward: 1
    Termination: False
    Truncation: False
    Return: 1
            
    Action: 0
    
    Observation: 2
    Reward: -1
    Termination: False
    Truncation: False
    Return: -1
            
    Action: 0
    
    Observation: 0
    Reward: 0
    Termination: False
    Truncation: True
    Return: 1
            
    Action: None
    
    Observation: 0
    Reward: 0
    Termination: False
    Truncation: True
    Return: -1
            
    Action: None
    

## `ActionMaskAgent`

Some `PettingZoo` environments provide an `action_mask` to tell the agent which actions are valid. The `ActionMaskAgent` subclasses `PettingZooAgent` to use information from the `action_mask` to select actions.


```python
class ActionMaskAgent(PettingZooAgent):
    def __init__(self, name, model, env):
        super().__init__(name, model, env)
        self.obs_buffer = collections.deque(maxlen=1)

    def random_action(self):
        obs = self.obs_buffer[-1]
        action = self.env.action_space(self.name).sample(obs["action_mask"])
        return action

    def reset(self):
        self.message_history = [
            SystemMessage(content=self.docs),
            SystemMessage(content=self.instructions),
        ]

    def observe(self, obs, rew=0, term=False, trunc=False, info=None):
        self.obs_buffer.append(obs)
        return super().observe(obs, rew, term, trunc, info)

    def _act(self):
        valid_action_instruction = "Generate a valid action given by the indices of the `action_mask` that are not 0, according to the action formatting rules."
        self.message_history.append(HumanMessage(content=valid_action_instruction))
        return super()._act()
```

## Tic-Tac-Toe
Here is an example of a Tic-Tac-Toe game that uses the `ActionMaskAgent`.


```python
from pettingzoo.classic import tictactoe_v3

env = tictactoe_v3.env(render_mode="human")
agents = {
    name: ActionMaskAgent(name=name, model=ChatOpenAI(temperature=0.2), env=env)
    for name in env.possible_agents
}
main(agents, env)
```

    
    Observation: {'observation': array([[[0, 0],
            [0, 0],
            [0, 0]],
    
           [[0, 0],
            [0, 0],
            [0, 0]],
    
           [[0, 0],
            [0, 0],
            [0, 0]]], dtype=int8), 'action_mask': array([1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=int8)}
    Reward: 0
    Termination: False
    Truncation: False
    Return: 0
            
    Action: 0
         |     |     
      X  |  -  |  -  
    _____|_____|_____
         |     |     
      -  |  -  |  -  
    _____|_____|_____
         |     |     
      -  |  -  |  -  
         |     |     
    
    Observation: {'observation': array([[[0, 1],
            [0, 0],
            [0, 0]],
    
           [[0, 0],
            [0, 0],
            [0, 0]],
    
           [[0, 0],
            [0, 0],
            [0, 0]]], dtype=int8), 'action_mask': array([0, 1, 1, 1, 1, 1, 1, 1, 1], dtype=int8)}
    Reward: 0
    Termination: False
    Truncation: False
    Return: 0
            
    Action: 1
         |     |     
      X  |  -  |  -  
    _____|_____|_____
         |     |     
      O  |  -  |  -  
    _____|_____|_____
         |     |     
      -  |  -  |  -  
         |     |     
    
    Observation: {'observation': array([[[1, 0],
            [0, 1],
            [0, 0]],
    
           [[0, 0],
            [0, 0],
            [0, 0]],
    
           [[0, 0],
            [0, 0],
            [0, 0]]], dtype=int8), 'action_mask': array([0, 0, 1, 1, 1, 1, 1, 1, 1], dtype=int8)}
    Reward: 0
    Termination: False
    Truncation: False
    Return: 0
            
    Action: 2
         |     |     
      X  |  -  |  -  
    _____|_____|_____
         |     |     
      O  |  -  |  -  
    _____|_____|_____
         |     |     
      X  |  -  |  -  
         |     |     
    
    Observation: {'observation': array([[[0, 1],
            [1, 0],
            [0, 1]],
    
           [[0, 0],
            [0, 0],
            [0, 0]],
    
           [[0, 0],
            [0, 0],
            [0, 0]]], dtype=int8), 'action_mask': array([0, 0, 0, 1, 1, 1, 1, 1, 1], dtype=int8)}
    Reward: 0
    Termination: False
    Truncation: False
    Return: 0
            
    Action: 3
         |     |     
      X  |  O  |  -  
    _____|_____|_____
         |     |     
      O  |  -  |  -  
    _____|_____|_____
         |     |     
      X  |  -  |  -  
         |     |     
    
    Observation: {'observation': array([[[1, 0],
            [0, 1],
            [1, 0]],
    
           [[0, 1],
            [0, 0],
            [0, 0]],
    
           [[0, 0],
            [0, 0],
            [0, 0]]], dtype=int8), 'action_mask': array([0, 0, 0, 0, 1, 1, 1, 1, 1], dtype=int8)}
    Reward: 0
    Termination: False
    Truncation: False
    Return: 0
            
    Action: 4
         |     |     
      X  |  O  |  -  
    _____|_____|_____
         |     |     
      O  |  X  |  -  
    _____|_____|_____
         |     |     
      X  |  -  |  -  
         |     |     
    
    Observation: {'observation': array([[[0, 1],
            [1, 0],
            [0, 1]],
    
           [[1, 0],
            [0, 1],
            [0, 0]],
    
           [[0, 0],
            [0, 0],
            [0, 0]]], dtype=int8), 'action_mask': array([0, 0, 0, 0, 0, 1, 1, 1, 1], dtype=int8)}
    Reward: 0
    Termination: False
    Truncation: False
    Return: 0
            
    Action: 5
         |     |     
      X  |  O  |  -  
    _____|_____|_____
         |     |     
      O  |  X  |  -  
    _____|_____|_____
         |     |     
      X  |  O  |  -  
         |     |     
    
    Observation: {'observation': array([[[1, 0],
            [0, 1],
            [1, 0]],
    
           [[0, 1],
            [1, 0],
            [0, 1]],
    
           [[0, 0],
            [0, 0],
            [0, 0]]], dtype=int8), 'action_mask': array([0, 0, 0, 0, 0, 0, 1, 1, 1], dtype=int8)}
    Reward: 0
    Termination: False
    Truncation: False
    Return: 0
            
    Action: 6
         |     |     
      X  |  O  |  X  
    _____|_____|_____
         |     |     
      O  |  X  |  -  
    _____|_____|_____
         |     |     
      X  |  O  |  -  
         |     |     
    
    Observation: {'observation': array([[[0, 1],
            [1, 0],
            [0, 1]],
    
           [[1, 0],
            [0, 1],
            [1, 0]],
    
           [[0, 1],
            [0, 0],
            [0, 0]]], dtype=int8), 'action_mask': array([0, 0, 0, 0, 0, 0, 0, 1, 1], dtype=int8)}
    Reward: -1
    Termination: True
    Truncation: False
    Return: -1
            
    Action: None
    
    Observation: {'observation': array([[[1, 0],
            [0, 1],
            [1, 0]],
    
           [[0, 1],
            [1, 0],
            [0, 1]],
    
           [[1, 0],
            [0, 0],
            [0, 0]]], dtype=int8), 'action_mask': array([0, 0, 0, 0, 0, 0, 0, 1, 1], dtype=int8)}
    Reward: 1
    Termination: True
    Truncation: False
    Return: 1
            
    Action: None
    

## Texas Hold'em No Limit
Here is an example of a Texas Hold'em No Limit game that uses the `ActionMaskAgent`.


```python
from pettingzoo.classic import texas_holdem_no_limit_v6

env = texas_holdem_no_limit_v6.env(num_players=4, render_mode="human")
agents = {
    name: ActionMaskAgent(name=name, model=ChatOpenAI(temperature=0.2), env=env)
    for name in env.possible_agents
}
main(agents, env)
```

    
    Observation: {'observation': array([0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
           0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
           0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 0., 1., 0., 0., 0., 0.,
           0., 0., 2.], dtype=float32), 'action_mask': array([1, 1, 0, 1, 1], dtype=int8)}
    Reward: 0
    Termination: False
    Truncation: False
    Return: 0
            
    Action: 1
    
    Observation: {'observation': array([0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
           0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
           0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 0.,
           0., 0., 2.], dtype=float32), 'action_mask': array([1, 1, 0, 1, 1], dtype=int8)}
    Reward: 0
    Termination: False
    Truncation: False
    Return: 0
            
    Action: 1
    
    Observation: {'observation': array([0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
           0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 0., 1.,
           0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
           0., 1., 2.], dtype=float32), 'action_mask': array([1, 1, 1, 1, 1], dtype=int8)}
    Reward: 0
    Termination: False
    Truncation: False
    Return: 0
            
    Action: 1
    
    Observation: {'observation': array([0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0.,
           0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
           0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
           0., 2., 2.], dtype=float32), 'action_mask': array([1, 1, 1, 1, 1], dtype=int8)}
    Reward: 0
    Termination: False
    Truncation: False
    Return: 0
            
    Action: 0
    
    Observation: {'observation': array([0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
           0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 0., 1.,
           0., 0., 0., 0., 0., 1., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0.,
           0., 2., 2.], dtype=float32), 'action_mask': array([1, 1, 1, 1, 1], dtype=int8)}
    Reward: 0
    Termination: False
    Truncation: False
    Return: 0
            
    Action: 2
    
    Observation: {'observation': array([0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
           0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
           0., 0., 0., 0., 0., 1., 0., 0., 1., 1., 0., 0., 1., 0., 0., 0., 0.,
           0., 2., 6.], dtype=float32), 'action_mask': array([1, 1, 1, 1, 1], dtype=int8)}
    Reward: 0
    Termination: False
    Truncation: False
    Return: 0
            
    Action: 2
    
    Observation: {'observation': array([0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
           0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
           0., 0., 0., 0., 0., 1., 0., 0., 1., 0., 0., 0., 0., 0., 1., 0., 0.,
           0., 2., 8.], dtype=float32), 'action_mask': array([1, 1, 1, 1, 1], dtype=int8)}
    Reward: 0
    Termination: False
    Truncation: False
    Return: 0
            
    Action: 3
    
    Observation: {'observation': array([ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
            0.,  0.,  0.,  0.,  0.,  0.,  1.,  0.,  0.,  0.,  0.,  0.,  0.,
            0.,  0.,  0.,  0.,  1.,  0.,  0.,  1.,  0.,  0.,  0.,  0.,  0.,
            1.,  0.,  0.,  1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
            6., 20.], dtype=float32), 'action_mask': array([1, 1, 1, 1, 1], dtype=int8)}
    Reward: 0
    Termination: False
    Truncation: False
    Return: 0
            
    Action: 4
    
    Observation: {'observation': array([  0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
             0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   1.,   0.,   0.,
             0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
             0.,   0.,   0.,   0.,   0.,   0.,   1.,   0.,   0.,   1.,   1.,
             0.,   0.,   1.,   0.,   0.,   0.,   0.,   0.,   8., 100.],
          dtype=float32), 'action_mask': array([1, 1, 0, 0, 0], dtype=int8)}
    Reward: 0
    Termination: False
    Truncation: False
    Return: 0
            
    Action: 4
    [WARNING]: Illegal move made, game terminating with current player losing. 
    obs['action_mask'] contains a mask of all legal moves that can be chosen.
    
    Observation: {'observation': array([  0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
             0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   1.,   0.,   0.,
             0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
             0.,   0.,   0.,   0.,   0.,   0.,   1.,   0.,   0.,   1.,   1.,
             0.,   0.,   1.,   0.,   0.,   0.,   0.,   0.,   8., 100.],
          dtype=float32), 'action_mask': array([1, 1, 0, 0, 0], dtype=int8)}
    Reward: -1.0
    Termination: True
    Truncation: True
    Return: -1.0
            
    Action: None
    
    Observation: {'observation': array([  0.,   0.,   1.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
             0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   1.,   0.,   0.,
             0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
             0.,   0.,   0.,   0.,   0.,   0.,   1.,   0.,   0.,   1.,   0.,
             0.,   0.,   0.,   0.,   1.,   0.,   0.,   0.,  20., 100.],
          dtype=float32), 'action_mask': array([1, 1, 0, 0, 0], dtype=int8)}
    Reward: 0
    Termination: True
    Truncation: True
    Return: 0
            
    Action: None
    
    Observation: {'observation': array([  0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
             0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   1.,   0.,   0.,
             0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   1.,   0.,   0.,
             1.,   0.,   0.,   0.,   0.,   0.,   1.,   0.,   0.,   1.,   0.,
             0.,   0.,   0.,   0.,   0.,   0.,   0.,   0., 100., 100.],
          dtype=float32), 'action_mask': array([1, 1, 0, 0, 0], dtype=int8)}
    Reward: 0
    Termination: True
    Truncation: True
    Return: 0
            
    Action: None
    
    Observation: {'observation': array([  0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   1.,   0.,   0.,
             0.,   0.,   0.,   0.,   0.,   0.,   0.,   1.,   1.,   0.,   0.,
             0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
             0.,   0.,   0.,   0.,   0.,   0.,   1.,   0.,   0.,   1.,   0.,
             0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   2., 100.],
          dtype=float32), 'action_mask': array([1, 1, 0, 0, 0], dtype=int8)}
    Reward: 0
    Termination: True
    Truncation: True
    Return: 0
            
    Action: None
    
