from pydantic import BaseModel


class PersonRequest(BaseModel):
    vorname: str
    name: str


class Person(BaseModel):
    id: int
    vorname: str
    name: str
