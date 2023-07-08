
Start tester
============

When you have implemented you `.features` file and you `steps` files, you can start the tester.

To start the tester you need to run the following command:

```bash
python -m xumes tester [options]
```

The options are:

```bash
--train: To use the train mode. The number of steps will be decided by the training side.
--test: To use the test mode. You have to pass the number of steps and/or number of iterations to perform.
--timesteps -t: The number of steps to perform.
--iterations -i: The number of iterations to perform. (Number of game plays)
--path: The path to the folder where the tests are located.
--ip: The ip of the training server.
--port: The port of the training server.
--debug: If you want to see the debug messages.
--info: If you want to see the info messages.
--render: If you want to render the game.
```

### Option 1
<font color="blue">**Description :** Description brève de l'option 1 et de ce qu'elle fait.</font>

<font color="green">**Exemple :**

