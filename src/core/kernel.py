from typing import final
from src.lib.autoloader import AutoLoader
from src.core.application import Application

@final
class Kernel:
    """
    the core class of the application
    """

    def __init__(self, main_view):
        AutoLoader.load()
        Application(main_view).mainloop()