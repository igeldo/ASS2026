from pydantic import BaseModel


class GreetingRequest(BaseModel):
    name: str
