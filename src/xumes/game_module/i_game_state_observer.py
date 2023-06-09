from typing import Generic, TypeVar

ST = TypeVar("ST")


class IGameStateObserver(Generic[ST]):

    def update_state(self, obs) -> None:
        """
        Update or add an observable inside the observer.
        If the observation has not changed we don't update the
        collection.
        :param obs: StateObservable object.
        """
        raise NotImplementedError

    def remove_state(self, obs) -> None:
        """
        Remove an observable of the collection.
        :param obs: StateObservable object.
        """
        raise NotImplementedError

    def get_state(self) -> ST:
        """
        Get the changes between the last time we retrieve the
        state and now.
        """
        raise NotImplementedError

    def __hash__(self):
        """
        Every game state observer has to be hashable.
        :return: A hash of the object
        """
        raise NotImplementedError



