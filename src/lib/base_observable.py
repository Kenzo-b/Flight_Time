import functools
from abc import ABC

from src.lib.base_observer import BaseObserver


class BaseObservable(ABC):
    """ an abstract base class for observables (observer design patterns)"""

    def __init__(self):
        self._observers: set[BaseObserver] = set()

    def add_observer(self, observer: BaseObserver) -> None:
        """
        add an observer
        :param observer: an instance of BaseObserver subclass
        :type observer: BaseObserver
        """
        if not isinstance(observer, BaseObserver):
            raise TypeError(f"{observer=} must be an instance of BaseObserver: {type(observer).__name__} given")
        self._observers.add(observer)

    def remove_observer(self, observer: BaseObserver) -> None:
        """
        remove an observer
        :param observer: an instance of BaseObserver subclass
        :type observer: BaseObserver
        """
        if not isinstance(observer, BaseObserver):
            raise TypeError(f"{observer=} must be an instance of BaseObserver: {type(observer).__name__} given")
        self._observers.remove(observer)

    def notify_observers(self) -> None:
        """
        notify all observers related to this observable
        """
        for observer in self._observers:
            state = {key: value for key, value in self.__dict__.items() if not key.startswith('__') and not key.startswith('_')}
            observer.update(**state)


def notify(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):  # Add 'self' for instance methods
        result = func(self, *args, **kwargs)
        self.notify_observers()
        return result
    return wrapper
