from greeter import Greeter


class GreeterService(Greeter):
    def greet(self, name: str) -> str:
        return f"Hello, {name}!"
