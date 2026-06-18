class Unternehmen:
    """Basisklasse: repräsentiert ein Unternehmen mit Name und Kalender."""

    def __init__(self, name: str):
        self.name = name
        self.kalender: list[str] = []

    def __str__(self) -> str:
        return f"Unternehmen: {self.name}"
