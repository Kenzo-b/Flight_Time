from abc import ABCMeta, abstractmethod

class BaseObserver(object, metaclass=ABCMeta):
    """ base observer interface (observer design pattern)"""

    @abstractmethod
    def update(self, **kwargs) -> None: pass
