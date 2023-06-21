
# Game side

With the default observables implementation, you don't have to create game element observables.
I will just need to create a `TestRunner`.

## Create a TestRunner

To create a `TestRunner`, you need to create a class that inherits from `TestRunner`.

```python
class MainTestRunner(TestRunner):
```
    
Then, you need to implement the `__init__` method.

```python
    def __init__(self):
        super().__init__()
```

Then inside the `__init__` method, you will need to `bind` your game state objects.

```python
        self.game_object1 = self.bind(self.game_object1, "name_game_object1", state)
```

The `bind` method takes as parameters the game object, the name of the game object and a state.

name is the name of the game object. You will need to use this name in the training side.

### State 

The goal of the state is to represent the state of the game object.
The state is a Composite pattern. It means that the state can contain other states.
The state tree needs to reach primitive types (int, float, str, bool, list of primitives...).


Here is a simple state that will retrieve the attribute `a` of the game object.

```python
State("a")
```

Here is a more complex state that will retrieve the attribute `a` of the game object and the attribute `b` of the attribute `c` of the `a` object.

```python
State("a", [State("c"), State("b")])
```

### methods_to_observe

When you create a `State` you can pass a list of methods to observe. A method to observe is a method inside the game object that will change the state.

```python
self.obj = self.bind(self.obj, "obj", State("a", methods_to_observe=["method"]))
```

In the example, when the self.obj.method is called, the state "a" will be updated.

You can be more precise. You can pass a list of methods to observe for each state.

```python
self.obj = self.bind(self.obj, "obj", State("a", State("b", methods_to_observe=["method"])))
```

Here, when the self.obj.method is called, the state "b" will be updated.


### func

You can also pass a function to the `State` object. This function will be called on his representation when the state is updated.

```python
self.obj = self.bind(self.obj, "obj", State("a", func=lambda x: x + 1))
```

Here, when the state "a" is updated, the value will be incremented by 1 on his representation.

### Different types of attributes

