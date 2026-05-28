import logging

from fastapi import FastAPI

from greeter_service import GreeterService

_log = logging.getLogger(__name__)

app = FastAPI()
_greeter = GreeterService()


@app.get("/api/hello")
def say_hello() -> str:
    message = _greeter.greet("World")
    _log.info("response: %s", message)
    return message
