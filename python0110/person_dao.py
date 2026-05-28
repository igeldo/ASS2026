from sqlalchemy.orm import Session

from models import Person
from orm_models import PersonModel


class PersonDAO:
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, vorname: str, name: str) -> Person:
        model = PersonModel(vorname=vorname, name=name)
        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)
        return Person(id=model.id, vorname=model.vorname, name=model.name)

    def find_by_id(self, id: int) -> Person | None:
        model = self._session.get(PersonModel, id)
        if model is None:
            return None
        return Person(id=model.id, vorname=model.vorname, name=model.name)
