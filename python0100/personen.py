from abc import ABC, abstractmethod

from models import Person


class Personen(ABC):
    @abstractmethod
    def create(self, vorname: str, name: str) -> Person: ...

    @abstractmethod
    def find_by_id(self, id: int) -> Person | None: ...
