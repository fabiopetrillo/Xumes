
# Game side

With the default observables implementation, you don't have to create game element observables.
I will just need to create a `TestRunner`.

## Create a TestRunner

To create a `TestRunner`, you need to create a class that inherits from `JsonTestRunner`.

```python
class MainTestRunner(JsonTestRunner):
```
    
Then, you need to implement the `__init__` method.

```python
    def __init__(self, observers, name):
        JsonTestRunner.__init__(self, observers=observers, name=name)
```

Finally, you need to implement the `run` method.

```python
    def run(self):
        for test_case in self.test_cases:
            self.run_test_case(test_case)
```