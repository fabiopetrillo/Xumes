import torch
from torch import nn
from typing import Tuple

from envs.hide_and_seek.params import ENV_NAME, TEST_NAME


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

        self.shared_net = nn.Sequential(
            nn.Linear(obs_space_dims, hidden_space1),
            nn.Tanh(),
            nn.Linear(hidden_space1, hidden_space2),
            nn.Tanh(),
        )

        # Policy Mean specific Linear Layer
        self.policy_mean_net = nn.Sequential(
            nn.Linear(hidden_space2, action_space_dims)
        )

        # Policy Std Dev specific Linear Layer
        self.policy_stddev_net = nn.Sequential(
            nn.Linear(hidden_space2, action_space_dims)
        )


    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """Conditioned on the observation, returns probability
         of a bernoulli distribution from which an action is sampled from.

        Args:
            x: Observation from the environment

        Returns:
            action_prob: predicted probability of the bernoulli distribution
        """
        shared_features = self.shared_net(x.float())

        action_means = self.policy_mean_net(shared_features)
        action_stddevs = torch.log(
            1 + torch.exp(self.policy_stddev_net(shared_features))
        )

        return action_means, action_stddevs


    def save(self):
        torch.save(self.state_dict(), f"./models/{ENV_NAME}-{TEST_NAME}")

    def save_dict(self, dict):
        torch.save(dict, f"./models/{ENV_NAME}-{TEST_NAME}-best_average" )