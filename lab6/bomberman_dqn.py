import gymnasium as gym
from gymnasium import spaces
import numpy as np
import math
import random
import matplotlib
from collections import namedtuple, deque
from itertools import count

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from bomberman_game import GameScene

NUM_OF_ACTIONS = 6  # Up down left rigth bomb nothing
OBSERVATION_SPACE_SIZE = 20  # 20 x 20 grid


class BombermanEnv(gym.Env):
    def __init__(self):
        super().__init__()

        self.observation_space = spaces.Box(low=0, high=3, shape=(OBSERVATION_SPACE_SIZE, OBSERVATION_SPACE_SIZE, 5),
                                            dtype=np.uint8)

        self.action_space = spaces.Discrete(6)

        self.game = GameScene(OBSERVATION_SPACE_SIZE, OBSERVATION_SPACE_SIZE, 0.05,
                                          0.15, 0.15)

    def step(self, action):
        next_state, reward, done = self.game.update_scene(action)

        return next_state, reward, done, {}

    def reset(self):
        # Obtain the games initial state
        initial_state = self.game.obtain_state()

        return initial_state

    def render(self, mode='human'):
        # Render the game visually (if implemented)
        self.game.render()


# Define the Q-Network
class QNetwork(nn.Module):
    def __init__(self, state_size, action_size):
        super(QNetwork, self).__init__()
        self.fc1 = nn.Linear(state_size, 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, action_size)

    def forward(self, state):
        x = torch.relu(self.fc1(state))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)


# Define the DQN agent
class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size

        self.q_network = QNetwork(state_size, action_size)
        self.target_network = QNetwork(state_size, action_size)
        self.optimizer = optim.Adam(self.q_network.parameters())

        self.memory = deque(maxlen=10000)
        self.batch_size = 64
        self.gamma = 0.99
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if random.random() <= self.epsilon:
            return random.randrange(self.action_size)
        state = torch.tensor(state, dtype=torch.float32).unsqueeze(0)
        action_values = self.q_network(state)
        return torch.argmax(action_values).item()

    def replay(self):
        if len(self.memory) < self.batch_size:
            return

        batch = random.sample(self.memory, self.batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)

        states = torch.tensor(states, dtype=torch.float32)
        actions = torch.tensor(actions, dtype=torch.int64).unsqueeze(1)
        rewards = torch.tensor(rewards, dtype=torch.float32)
        next_states = torch.tensor(next_states, dtype=torch.float32)
        dones = torch.tensor(dones, dtype=torch.bool)

        current_q_values = self.q_network(states).gather(1, actions)
        next_q_values = self.target_network(next_states).max(1)[0].detach()
        target_q_values = rewards + (1 - dones) * self.gamma * next_q_values

        loss = nn.functional.mse_loss(current_q_values, target_q_values.unsqueeze(1))
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

    def update_target_network(self):
        self.target_network.load_state_dict(self.q_network.state_dict())


# Training the DQN agent
def train_dqn(env, agent, episodes=1000):
    for episode in range(episodes):
        state = env.reset()
        done = False
        while not done:
            action = agent.act(state)
            next_state, reward, done, _ = env.step(action)
            agent.remember(state, action, reward, next_state, done)
            state = next_state

            agent.replay()

        agent.update_target_network()

        if episode % 100 == 0:
            print(f"Episode: {episode}")

# Create the custom environment for the Bomberman game
env = BombermanEnv()

# Get the state and action sizes from the environment
state_size = np.prod(env.observation_space.shape)
action_size = env.action_space.n

# Initialize the DQN agent
agent = DQNAgent(state_size, action_size)

# Train the agent
train_dqn(env, agent, episodes=1000)

# Save the trained model
torch.save(agent.q_network.state_dict(), "bomberman_dqn.pt")