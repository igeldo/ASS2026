from fastapi import FastAPI

from greeter_service import GreeterService
from hello_world_router import HelloWorldRouter

app = FastAPI()
app.include_router(HelloWorldRouter(GreeterService()).router)
