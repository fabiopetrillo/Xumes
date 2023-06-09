

class IGameEvent:

    def press(self) -> None:
        """
        Method used to adapt the press function of a button.
        """
        raise NotImplementedError

    def release(self) -> None:
        """
        Method used to adapt the release function of a button.
        """
        raise NotImplementedError

