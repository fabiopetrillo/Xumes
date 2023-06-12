Xumes

## Installation
```python
pip install -i https://test.pypi.org/simple/ xumes
```

It's possible that certain dependencies will not be found on test.pypi.org so you may have to install them yourself.

## Schema
..image:: schema.jpg

## Future work
- [ ] Add observable wrapper on game class attribut in order to get only the small changes and not all the object state.
- [ ] Add render mode with the same use as Gym.
- [ ] Remove the observers list in the TestRunner class.
- [ ] Add a Logger that contains GameServices and handles their changing state and their saving.
