# =============================================================================
# Informatik 4 – Von Java zu OOP in Python
# Klassenbibliothek – Modul 1 & Ergänzung: Objektorientierung
#
# Diese Datei enthält ausschließlich Klassendefinitionen – keine Ausgaben.
# Sie wird von main.py importiert:
#   from informatik4_oop_java_zu_python import Person, Student, Kreis, Vektor, Rechteck
#
# Kommentare erklären jeweils den Vergleich zu Java.
# =============================================================================


# -----------------------------------------------------------------------------
# 1. KLASSEN UND OBJEKTE
# -----------------------------------------------------------------------------
# Java:
#   public class Person {
#       private String name;
#       private int alter;
#       public Person(String name, int alter) {
#           this.name = name;
#           this.alter = alter;
#       }
#       public void vorstellen() { ... }
#   }

class Person:
    def __init__(self, name, alter):    # __init__ = Konstruktor,  self = this
        self.name = name                # kein private/public – direkte Zuweisung
        self.alter = alter

    def vorstellen(self):               # self muss immer explizit angegeben werden
        return f"Ich bin {self.name}, {self.alter} Jahre alt."

    def __str__(self):                  # entspricht toString() in Java
        return f"Person({self.name}, {self.alter} Jahre)"

    def __repr__(self):                 # __repr__ sollte eine Darstellung liefern, mit der man das Objekt idealerweise neu erzeugen könnte: Person("Anna", 22)
        return f"Person('{self.name}', {self.alter})"


# -----------------------------------------------------------------------------
# 2. SICHTBARKEIT: KONVENTION STATT ERZWINGUNG
# -----------------------------------------------------------------------------
# Java:  private String pin;  -> vom Compiler erzwungen
# Python: Konvention statt Zwang
#   self.name      -> öffentlich          (entspricht public)
#   self._name     -> intern, Finger weg  (entspricht protected)
#   self.__name    -> name-mangled        (entspricht annähernd private)

class Konto:
    def __init__(self, inhaber, kontostand):
        self.inhaber = inhaber             # öffentlich
        self._kontonummer = "DE12345"      # intern (Konvention)
        self.__pin = "1234"                # name-mangled: _Konto__pin

    def info(self):
        return f"Konto von {self.inhaber}, Nr: {self._kontonummer}"

    def __str__(self):
        return f"Konto({self.inhaber})"


# -----------------------------------------------------------------------------
# 3. PROPERTIES: GETTER UND SETTER AUF PYTHONS ART
# -----------------------------------------------------------------------------
# Java:
#   public int getAlter() { return alter; }
#   public void setAlter(int alter) {
#       if (alter < 0) throw new IllegalArgumentException(...);
#       this.alter = alter;
#   }
#
# In Python sieht der Zugriff nach außen aus wie ein normales Attribut,
# hat aber die Kontrolle einer Methode.

class Student:
    def __init__(self, name, alter):
        self.name = name
        self._alter = alter             # _ signalisiert: bitte über Property zugreifen

    @property
    def alter(self):                    # Getter – kein get_alter() nötig
        return self._alter

    @alter.setter
    def alter(self, wert):              # Setter mit Validierung
        if wert < 0:
            raise ValueError("Alter kann nicht negativ sein!")
        if wert > 120:
            raise ValueError("Alter unrealistisch hoch!")
        self._alter = wert

    def __str__(self):                  # entspricht toString() in Java
        return f"Student({self.name}, {self.alter} Jahre)"


# -----------------------------------------------------------------------------
# 4. KLASSENMETHODEN UND STATISCHE METHODEN
# -----------------------------------------------------------------------------
# Java: public static Kreis ausRadius(double r) { ... }
#
# Python unterscheidet:
#   @classmethod   -> kennt die Klasse (cls), z. B. für alternative Konstruktoren
#   @staticmethod  -> kennt weder Klasse noch Instanz (entspricht static in Java)

class Kreis:
    pi = 3.14159                        # Klassenattribut (wie static in Java)

    def __init__(self, radius):
        self.radius = radius

    def flaeche(self):                  # normale Instanzmethode
        return Kreis.pi * self.radius ** 2

    def umfang(self):
        return 2 * Kreis.pi * self.radius

    @classmethod
    def aus_durchmesser(cls, durchmesser):   # alternativer Konstruktor
        return cls(durchmesser / 2)

    @staticmethod
    def ist_gueltig(radius):            # braucht keine Instanz/Klasse
        return radius > 0

    def __str__(self):
        return f"Kreis(r={self.radius}, A={self.flaeche():.2f})"

    def __lt__(self, other):            # ermöglicht sorted()
        return self.flaeche() < other.flaeche()

    def __eq__(self, other):
        if not isinstance(other, Kreis):
            return False
        return self.radius == other.radius


# -----------------------------------------------------------------------------
# 5. DUNDER-METHODEN: OPERATOREN ÜBERLADEN
# -----------------------------------------------------------------------------
# In Java kann man Operatoren nicht überladen.
# In Python definiert man spezielle __methoden__ dafür:
#
#   __str__    -> toString()
#   __repr__   -> technische Darstellung (für Debugging / Listen)
#   __add__    -> ermöglicht v1 + v2
#   __sub__    -> ermöglicht v1 - v2
#   __mul__    -> ermöglicht v * skalar
#   __eq__     -> ermöglicht v1 == v2
#   __len__    -> ermöglicht len(obj)

class Vektor:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Vektor({self.x}, {self.y})"

    def __repr__(self):                 # für Debugging und Listen-Ausgabe
        return f"Vektor({self.x}, {self.y})"

    def __add__(self, other):           # v1 + v2
        return Vektor(self.x + other.x, self.y + other.y)

    def __sub__(self, other):           # v1 - v2
        return Vektor(self.x - other.x, self.y - other.y)

    def __mul__(self, skalar):          # v * 3
        return Vektor(self.x * skalar, self.y * skalar)

    def __eq__(self, other):            # v1 == v2
        if not isinstance(other, Vektor):
            return False
        return self.x == other.x and self.y == other.y

    def __len__(self):                  # len(v) -> Dimension
        return 2

    def betrag(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5


# -----------------------------------------------------------------------------
# 6. VERERBUNG – ERSTER BLICK
# -----------------------------------------------------------------------------
# Java:  public class Mitarbeiter extends Person { ... }
# Python: class Mitarbeiter(Person): ...
#
# super() braucht in Python keine Argumente – häufiger Stolperstein!

class Mitarbeiter(Person):
    def __init__(self, name, alter, abteilung):
        super().__init__(name, alter)   # kein super(name, alter) wie in Java!
        self.abteilung = abteilung

    def vorstellen(self):               # Methode überschreiben (Override)
        basis = super().vorstellen()    # Elternmethode aufrufen
        return f"{basis} Ich arbeite in der Abteilung: {self.abteilung}"

    def __str__(self):
        return f"Mitarbeiter({self.name}, {self.abteilung})"


# -----------------------------------------------------------------------------
# 7. DUCK TYPING – KLASSE OHNE GEMEINSAMES INTERFACE
# -----------------------------------------------------------------------------
# Java braucht ein Interface (z. B. Shape) damit Kreis und Rechteck
# polymorph verwendet werden können.
# Python braucht das nicht – solange beide eine flaeche()-Methode haben,
# funktioniert es ("If it quacks like a duck...")

class Rechteck:
    def __init__(self, breite, hoehe):
        self._breite = breite
        self._hoehe = hoehe

    @property
    def breite(self):
        return self._breite

    @property
    def hoehe(self):
        return self._hoehe

    def flaeche(self):
        return self._breite * self._hoehe

    def umfang(self):
        return 2 * (self._breite + self._hoehe)

    def __str__(self):
        return f"Rechteck({self._breite}x{self._hoehe}, A={self.flaeche()})"

    def __lt__(self, other):            # ermöglicht sorted()
        return self.flaeche() < other.flaeche()

    def __eq__(self, other):
        if not isinstance(other, Rechteck):
            return False
        return self.flaeche() == other.flaeche()
