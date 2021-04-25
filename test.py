import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import walker
import display

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)

class Actor(nn.Module):
        def __init__(self):
                super(Actor, self).__init__()
                self.l1 = nn.Linear(60, 256)
                self.l2 = nn.Linear(256, 256)
                self.l3 = nn.Linear(256, 4)

        def forward(self, state):
                a = F.relu(self.l1(state))
                a = F.relu(self.l2(a))
                return torch.tanh(self.l3(a))

        def select_action(self, state):
                state = torch.FloatTensor(state.reshape(1, -1)).to(device)
                return self(state).cpu().data.numpy().flatten()
        
env = walker.Walker()
d = display.Display(60)

actor = Actor()
actor.load_state_dict(torch.load(f"./models/TD3_walk_targets_actor"))

s, done, reward = env.reset(), False, 0
for _ in range(10000):
        act = np.random.random(4)*2 - 1
        d.render(env)
        act = actor.select_action(s)
        s, r, done = env.step(act)
        reward += r
        if done:
                s, done, reward = env.reset(), False, 0

