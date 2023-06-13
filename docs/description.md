# Description

## What's Xumes?
Xumes is a game testing tool, made to be use on the top of game without the necessity to modificate the game sources.

## Framework architecture
The framework is contains to main components: "Game side" and "Training side", you will find them in the python package with the snames `game_module` and `training_module`.
So you will need to write two separate python executables one for each component.

![framework schema](schema.png)

### Game side
The game side is in contact with the game. The responsibility of this part is to interact with the game (send state to the trainer and get actions from the trainer) and log the global game state.
As you can see this part extends directly the game.

[How to implement the game side?](game_side.md)

### Training side
This part has the responsibility to predict actions from game states. It's coming with a `stablebaselines` implementation in order to implement a large panel of RL algorithms.

[How to implement the training side?](training_side.md)
