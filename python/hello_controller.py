from fastapi import APIRouter


class HelloController:
    def __init__(self):
        self._router = APIRouter()
        self._router.add_api_route("/api/hello", self.hello, methods=["GET"])

    @property
    def router(self):
        return self._router

    def hello(self, name: str = None):
        if not name:
            return "Hello World!"
        return f"Hello {name}!"
