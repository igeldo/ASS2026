import logging


class HelloWorld:
    _log = logging.getLogger(__qualname__)

    def __init__(self, name: str) -> None:
        self._name = name

    def greeting(self) -> str:
        return f"Hello, {self._name}!"

    def run(self) -> None:
        message = self.greeting()
        self._log.info(message)
