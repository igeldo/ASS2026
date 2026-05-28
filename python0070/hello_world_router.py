import logging

from fastapi import APIRouter

from greeter import Greeter


class HelloWorldRouter:
    _log = logging.getLogger(__qualname__)

    def __init__(self, greeter: Greeter) -> None:
        self._greeter = greeter
        self.router = APIRouter()
        self.router.add_api_route("/api/hello", self.say_hello, methods=["GET"])

    def say_hello(self) -> str:
        message = self._greeter.greet("World")
        self._log.info("response: %s", message)
        return message
