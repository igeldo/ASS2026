import logging
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from database import get_session
from models import Person, PersonRequest
from person_dao import PersonDAO
from personen import Personen
from personen_service import PersonenService

_log = logging.getLogger(__name__)

app = FastAPI()


def get_personen_service(session: Annotated[Session, Depends(get_session)]) -> Personen:
    return PersonenService(PersonDAO(session))


PersonenDep = Annotated[Personen, Depends(get_personen_service)]


@app.post("/api/person")
def create_person(request: PersonRequest, service: PersonenDep) -> Person:
    return service.create(request.vorname, request.name)


@app.get("/api/person/{id}")
def find_by_id(id: int, service: PersonenDep) -> Person:
    person = service.find_by_id(id)
    if person is None:
        raise HTTPException(status_code=404)
    return person
