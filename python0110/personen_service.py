import logging

from models import Person
from person_dao import PersonDAO
from personen import Personen


class PersonenService(Personen):
    _log = logging.getLogger(__qualname__)

    def __init__(self, dao: PersonDAO) -> None:
        self._dao = dao

    def create(self, vorname: str, name: str) -> Person:
        self._log.info("create person: %s %s", vorname, name)
        return self._dao.save(vorname, name)

    def find_by_id(self, id: int) -> Person | None:
        self._log.info("looking for person with id: %d", id)
        found = self._dao.find_by_id(id)
        if found is None:
            self._log.warning("no person found with id: %d", id)
        return found
