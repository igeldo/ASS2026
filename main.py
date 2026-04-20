# =============================================================================
# Informatik 4 – Von Java zu OOP in Python
# main.py – Demonstrations-Anwendung für Modul 1
#
# Dieses Skript importiert alle Klassen aus der Klassenbibliothek und führt
# die Konzepte Schritt für Schritt vor. Einfach ausführen und die Ausgabe
# mit dem Code in informatik4_oop_java_zu_python.py vergleichen.
#
# Ausführen:
#   PyCharm:  grüner Play-Button (Shift + F10)
#   Terminal: python main.py
# =============================================================================

from informatik4_oop_java_zu_python import (
    Person, Konto, Student, Kreis, Vektor, Mitarbeiter, Rechteck
)


def trennlinie(titel: str) -> None:
    """Gibt eine formatierte Überschrift für jeden Abschnitt aus."""
    print(f"\n{'=' * 60}")
    print(f"  {titel}")
    print(f"{'=' * 60}")


# -----------------------------------------------------------------------------
# 1. KLASSEN UND OBJEKTE
# -----------------------------------------------------------------------------
def demo_klassen_und_objekte() -> None:
    trennlinie("Abschnitt 1: Klassen und Objekte")

    # Java: Person p = new Person("Anna", 22);
    # Python: kein new, kein Typ vor dem Variablennamen
    anna = Person("Anna", 22)

    print(anna.vorstellen())    # Methode aufrufen
    print(anna)                 # __str__ wird von print() automatisch aufgerufen
    print(repr(anna))           # repr() gibt die Standard-Darstellung aus

    print(f"\nDirekter Attributzugriff: anna.name = '{anna.name}'")
    print(f"Direkter Attributzugriff: anna.alter = {anna.alter}")


# -----------------------------------------------------------------------------
# 2. SICHTBARKEIT: KONVENTION STATT ERZWINGUNG
# -----------------------------------------------------------------------------
def demo_sichtbarkeit() -> None:
    trennlinie("Abschnitt 2: Sichtbarkeit")

    maryam = Person("Maryam", 30)
    konto = Konto(maryam.name, 1500)

    print(konto.info())
    print(f"Kontoinhaber als Person: {maryam}")
    print(f"Öffentliches Attribut:  konto.inhaber      = '{konto.inhaber}'")
    print(f"Internes Attribut:      konto._kontonummer = '{konto._kontonummer}'")

    # Name Mangling: __pin ist von außen nicht direkt zugänglich
    # konto.__pin          -> AttributeError!
    # konto._Konto__pin    -> geht, aber bitte nicht machen
    print(f"Name-Mangling Demo:     konto._Konto__pin  = '{konto._Konto__pin}'  <- bitte nie so verwenden!")


# -----------------------------------------------------------------------------
# 3. PROPERTIES: GETTER UND SETTER AUF PYTHONS ART
# -----------------------------------------------------------------------------
def demo_properties() -> None:
    trennlinie("Abschnitt 3: Properties")

    student = Student("Alan", 21)   # siehe auch Vererbung !
    print(student)

    # Setter wird aufgerufen wie eine normale Zuweisung – kein setAlter()!
    student.alter = 22
    print(f"Nach Änderung: {student}")

    # Validierung testen
    print("\nValidierung – ungültiges Alter:")
    try:
        student.alter = -5          # löst ValueError aus
    except ValueError as e:
        print(f"  ValueError: {e}")

    try:
        student.alter = 200         # löst ValueError aus
    except ValueError as e:
        print(f"  ValueError: {e}")


# -----------------------------------------------------------------------------
# 4. KLASSENMETHODEN UND STATISCHE METHODEN
# -----------------------------------------------------------------------------
def demo_klassenmethoden() -> None:
    trennlinie("Abschnitt 4: Klassenmethoden und statische Methoden")

    # Normaler Konstruktor
    k1 = Kreis(5)
    print(f"Kreis aus Radius:      {k1}")
    print(f"  Fläche:  {k1.flaeche():.2f}")
    print(f"  Umfang:  {k1.umfang():.2f}")

    # Alternativer Konstruktor via @classmethod
    k2 = Kreis.aus_durchmesser(10)
    print(f"\nKreis aus Durchmesser: {k2}")

    # @staticmethod – braucht kein Objekt
    print(f"\nKreis.ist_gueltig(5)  = {Kreis.ist_gueltig(5)}")
    print(f"Kreis.ist_gueltig(-1) = {Kreis.ist_gueltig(-1)}")

    # Klassenattribut (entspricht static-Feld in Java)
    print(f"\nKlassenattribut Kreis.pi = {Kreis.pi}")


# -----------------------------------------------------------------------------
# 5. DUNDER-METHODEN: OPERATOREN ÜBERLADEN
# -----------------------------------------------------------------------------
def demo_dunder_methoden() -> None:
    trennlinie("Abschnitt 5: Dunder-Methoden")

    v1 = Vektor(2, 3)
    v2 = Vektor(1, -1)

    print(f"v1 = {v1}")
    print(f"v2 = {v2}")
    print(f"\nv1 + v2 = {v1 + v2}")           # __add__
    print(f"v1 - v2 = {v1 - v2}")             # __sub__
    print(f"v1 * 3  = {v1 * 3}")              # __mul__
    print(f"v1 == v2: {v1 == v2}")            # __eq__
    print(f"v1 == Vektor(2,3): {v1 == Vektor(2, 3)}")
    print(f"len(v1) = {len(v1)}")             # __len__
    print(f"|v1|    = {v1.betrag():.2f}")     # normale Methode

    # repr() vs str()
    vektoren = [Vektor(1, 0), Vektor(0, 1), Vektor(3, 4)]
    print(f"\nListe: {vektoren}")              # __repr__ wird in Listen verwendet


# -----------------------------------------------------------------------------
# 6. VERERBUNG
# -----------------------------------------------------------------------------
def demo_vererbung() -> None:
    trennlinie("Abschnitt 6: Vererbung")

    m = Mitarbeiter("Ben", 35, "Entwicklung")
    print(m)
    print(m.vorstellen())       # überschriebene Methode – ruft super() auf

    # isinstance() prüft die Vererbungshierarchie
    print(f"\nisinstance(m, Mitarbeiter): {isinstance(m, Mitarbeiter)}")
    print(f"isinstance(m, Person):      {isinstance(m, Person)}")

    # Polymorphismus: Person und Mitarbeiter in einer Liste
    personen: list[Person] = [
        Person("Cara", 28),
        Mitarbeiter("Dan", 40, "Marketing"),
        Person("Eva", 19),
        Mitarbeiter("Frank", 52, "Vertrieb"),
    ]

    print("\nAlle Personen (polymorph):")
    for p in personen:
        print(f"  {p.vorstellen()}")


# -----------------------------------------------------------------------------
# 7. DUCK TYPING
# -----------------------------------------------------------------------------
def demo_duck_typing() -> None:
    trennlinie("Abschnitt 7: Duck Typing")

    # Kreis und Rechteck haben kein gemeinsames Interface (kein implements Shape).
    # Solange beide flaeche() und umfang() haben, funktioniert der Code.
    formen = [
        Kreis(3),
        Rechteck(4, 6),
        Kreis(1),
        Rechteck(10, 2),
        Kreis(7),
    ]

    print("Alle Formen – Duck Typing in Aktion:")
    for form in formen:
        print(f"  {form}  ->  Fläche: {form.flaeche():.2f},  Umfang: {form.umfang():.2f}")

    # sorted() ist eine eingebaute Python-Methode, die eine sortierte Liste erstellt
    # sorted() funktioniert dank __lt__ auf beiden Klassen
    # Achtung: sorted() kann nur Objekte vergleichen, die denselben Typ haben
    kreise = [Kreis(3), Kreis(1), Kreis(7), Kreis(5)]
    kreise_sortiert = sorted(kreise)
    print(f"\nKreise sortiert (via __lt__): {[str(k) for k in kreise_sortiert]}")

    rechtecke = [Rechteck(4, 6), Rechteck(10, 2), Rechteck(3, 3)]
    rechtecke_sortiert = sorted(rechtecke)
    print(f"Rechtecke sortiert (via __lt__): {[str(r) for r in rechtecke_sortiert]}")


# -----------------------------------------------------------------------------
# Python-Einstiegspunkt
# -----------------------------------------------------------------------------
# Java: public static void main(String[] args) { ... }
# Python: if __name__ == "__main__": schützt Code vor ungewollter Ausführung
#         beim Import dieser Datei als Modul.
if __name__ == "__main__":
    demo_klassen_und_objekte()
    demo_sichtbarkeit()
    demo_properties()
    demo_klassenmethoden()
    demo_dunder_methoden()
    demo_vererbung()
    demo_duck_typing()

    trennlinie("Ende der Demonstration – viel Erfolg in Informatik 4!")