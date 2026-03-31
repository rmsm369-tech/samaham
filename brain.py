import torch
import torch.nn as nn

class AwarenessDecayNetwork(nn.Module):
    def __init__(self, input_size=2, hidden_size=2, output_size=1):
        super().__init__()
        self.primary_network = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, output_size)
        )
        self.meta_observer = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.Sigmoid()
        )
        self.gamma = 0.05
        self.threshold = nn.Parameter(torch.tensor(0.3))

    def forward(self, x):
        urge_to_act = self.meta_observer(x).mean()
        threshold = self.threshold
        if urge_to_act < threshold:
            return torch.zeros(1, self.primary_network[-1].out_features), urge_to_act, True
        action = self.primary_network(x)
        return action, urge_to_act, False