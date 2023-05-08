# Reinforcement learning applied to Flappy bird
Use of Policy gradient algorithm on a game made with pygame.

# Description
I create a gym environmnent used as interface between the policy grandient algorithm and the pygame game.
- ./gym_pygame/envs/v0/src contains pygame sources
- ./gym_pygame/envs/v0/rl_flappy.py is the gym environment
- ./learning contains the policy gradient algorithm and models saved

# Rewards
- + 1 for scoring a point
- - 1 when dying

# Model
- 8 X 32 with ReLU activation
- 32 X 32 with ReLU activation
- 32 X 1 with Sigmoïd activation

I trained the model on 5000 episodes, using the Adam optimizer with a learning rate of 1e-4, a discount factor of gamma = 0.99, a negative loss and a Bernoulli distribution to compute the action.

![alt text](https://github.com/mastainvin/rl_flappy/master/learning/graphs/RLFlappy-v0-easy-reward.png)

