import torch
from torch import nn
from typing import Tuple

from envs.params import ENV_NAME, TEST_NAME


class PolicyNetwork(nn.Module):
    """Parametrized Policy Network."""

    def __init__(self, obs_space_dims: int, action_space_dims: int):
        """Initializes a neural network that estimates the probability for bernoulli distribution
            from which an action is sampled from.

        Args:
            obs_space_dims: Dimension of the observation space
            action_space_dims: Dimension of the action space
        """
        super().__init__()

        hidden_space1 = 32
        hidden_space2 = 32

        self.network = nn.Sequential(
            nn.Linear(obs_space_dims, hidden_space1),
            nn.ReLU(),
            nn.Linear(hidden_space1, hidden_space2),
            nn.ReLU(),
            nn.Linear(hidden_space2, action_space_dims),
            nn.Sigmoid(),
        )


    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """Conditioned on the observation, returns probability
         of a bernoulli distribution from which an action is sampled from.

        Args:
            x: Observation from the environment

        Returns:
            action_prob: predicted probability of the bernoulli distribution
        """
        action_prob = self.network(x.float())

        return action_prob


    def save(self):
        torch.save(self.state_dict(), f"./models/{ENV_NAME}-{TEST_NAME}")

    def save_dict(self, dict):
        torch.save(dict, f"./models/{ENV_NAME}-{TEST_NAME}-best_average" )