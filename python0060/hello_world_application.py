import logging

from greeter import Greeter


class HelloWorldApplication:
    _log = logging.getLogger(__qualname__)

    def __init__(self, greeter: Greeter) -> None:
        self._greeter = greeter

    def run(self) -> None:
        message = self._greeter.greet("World")
        self._log.info(message)
