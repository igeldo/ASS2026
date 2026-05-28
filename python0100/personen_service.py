import logging

from models import Person
from personen import Personen


class PersonenService(Personen):
    _log = logging.getLogger(__qualname__)

    def __init__(self) -> None:
        self._store: dict[int, Person] = {}
        self._next_id: int = 1

    def create(self, vorname: str, name: str) -> Person:
        self._log.info("create person: %s %s", vorname, name)
        person = Person(id=self._next_id, vorname=vorname, name=name)
        self._store[self._next_id] = person
        self._next_id += 1
        return person

    def find_by_id(self, id: int) -> Person | None:
        self._log.info("looking for person with id: %d", id)
        found = self._store.get(id)
        if found is None:
            self._log.warning("no person found with id: %d", id)
        return found
