import logging

from fastapi import FastAPI

from greeter_service import GreeterService
from models import GreetingRequest

_log = logging.getLogger(__name__)

app = FastAPI()
_greeter = GreeterService()


@app.get("/api/hello")
def say_hello(name: str) -> str:
    message = _greeter.greet(name)
    _log.info("response: %s", message)
    return message


@app.get("/api/hello/{name}")
def say_hello_with_path_variable(name: str) -> str:
    return say_hello(name)


@app.post("/api/hello")
def create_greeting(request: GreetingRequest) -> str:
    message = _greeter.greet(request.name)
    _log.info("response: %s", message)
    return message
