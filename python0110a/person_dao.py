from sqlalchemy import text
from sqlalchemy.orm import Session

from models import Person


class PersonDAO:
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, vorname: str, name: str) -> Person:
        result = self._session.execute(
            text("INSERT INTO persons (vorname, name) VALUES (:vorname, :name) RETURNING id"),
            {"vorname": vorname, "name": name},
        )
        row = result.mappings().fetchone()
        assert row is not None
        self._session.commit()
        return Person(id=row["id"], vorname=vorname, name=name)

    def find_by_id(self, id: int) -> Person | None:
        result = self._session.execute(
            text("SELECT id, vorname, name FROM persons WHERE id = :id"),
            {"id": id},
        )
        row = result.mappings().fetchone()
        if row is None:
            return None
        return Person(id=row["id"], vorname=row["vorname"], name=row["name"])
