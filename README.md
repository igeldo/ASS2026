
# Repository für die Veranstaltung Ausgewählte Softwaresysteme SoSe2026

1) Jeder Teilnehmer und jede Teilnehmerin soll für Ihre Ergebnisse einen eigenen "branch" erzeugen und dann für die Einzelarbeit verwenden

2) Zusätzlich soll jedes Team einen eigenen "branch" erzeugen und für die Projektarbeit verwenden

---

## Session Log

### Benutzeranfrage (Übersetzt aus dem Vietnamesischen)
Erstelle mir eine Datei `informatik4_oop_java_zu_python.py`. In der Datei soll der Java-Code jeweils direkt als Kommentar über dem entsprechenden Python-Code stehen. Es soll keine direkte Ausgabe geben, nur Klassen — und diese Klassen sollen in `main.py` importiert werden.

### Durchgeführte Aktionen
- Datei `informatik4_oop_java_zu_python.py` im Projektstammverzeichnis erstellt
- Kopfkommentar mit der Konvention hinzugefügt: Java-Code als Kommentar direkt über dem äquivalenten Python-Code
- Datei enthält bisher nur die Konvention und wartet auf die konkrete Aufgabenstellung bzw. Java-Vorlage des Nutzers, bevor Klassen ergänzt werden
- Keine Ausführung/kein Output auf Modulebene — Datei ist ausschließlich für den Import in `main.py` vorgesehen

### Ergebnis
Die Datei wurde erfolgreich mit der vereinbarten Konvention angelegt und ist bereit, sobald die konkrete Java-Aufgabenstellung vorliegt.

---

## Session Log

### Benutzeranfrage (Übersetzt aus dem Vietnamesischen)
Das Thema ist jetzt Fehlerbehandlung in Python. Erstelle zunächst eine Klasse mit einer Methode, bei der der Nutzer eine Zahl eingeben kann. Wenn die Eingabe keine gültige Zahl ist, soll "invalid number" ausgegeben werden; wenn sie gültig ist, soll "you entered:" + Zahl ausgegeben werden.

### Durchgeführte Aktionen
- Klasse `NumberInputHandler` mit Methode `read_number()` in `informatik4_oop_java_zu_python.py` ergänzt
- `try/except ValueError` zur Fehlerbehandlung ungültiger Zahleneingaben implementiert
- Java-Äquivalent (`Scanner`, `Integer.parseInt`, `NumberFormatException`) als Kommentar direkt über jeder Python-Zeile ergänzt

### Ergebnis
Klasse erfolgreich erstellt, gibt bei ungültiger Eingabe "invalid number" und bei gültiger Eingabe "you entered: X" aus.

---

## Session Log

### Benutzeranfrage (Übersetzt aus dem Vietnamesischen)
Erstelle eine Datei main.py und importiere die Klasse, um sie zu testen.

### Durchgeführte Aktionen
- Datei `main.py` erstellt, importiert `NumberInputHandler` aus `informatik4_oop_java_zu_python.py`
- Testaufruf unter `if __name__ == "__main__":` ergänzt
- Mit gültiger Eingabe ("42") und ungültiger Eingabe ("abc") über die Kommandozeile getestet

### Ergebnis
Beide Testfälle liefen korrekt: gültige Zahl ergab "you entered: 42", ungültige Eingabe ergab "invalid number".

---

## Session Log

### Benutzeranfrage (Übersetzt aus dem Vietnamesischen)
Erstelle jetzt eine weitere Klasse: In diesem Fall geht es um die Division einer Zahl durch eine andere Zahl. Die Fehlerbehandlung soll hier greifen, wenn durch 0 geteilt wird oder eine ungültige Zahl eingegeben wird.

### Durchgeführte Aktionen
- Klasse `DivisionHandler` mit Methode `divide_numbers()` in `informatik4_oop_java_zu_python.py` ergänzt
- Separate `except`-Blöcke für `ValueError` (ungültige Zahl) und `ZeroDivisionError` (Division durch 0) implementiert
- Java-Äquivalent (`NumberFormatException`, `ArithmeticException`) als Kommentar direkt über jeder Python-Zeile ergänzt
- `main.py` aktualisiert, um auch `DivisionHandler` zu importieren und zu testen
- Mit gültiger Division, Division durch 0 und ungültiger Eingabe getestet — alle drei Fälle korrekt

### Ergebnis
Klasse erfolgreich erstellt und getestet: gültige Division ergibt "Result: X", Division durch 0 ergibt "cannot divide by zero", ungültige Eingabe ergibt "invalid number".

---

## Session Log

### Benutzeranfrage (Übersetzt aus dem Vietnamesischen)
Aktualisiere main.py von jetzt an automatisch, ohne nachzufragen.

### Durchgeführte Aktionen
- Arbeitsweise angepasst: Neue Klassen in `informatik4_oop_java_zu_python.py` werden ab sofort automatisch in `main.py` eingebunden und getestet, ohne vorher nachzufragen

### Ergebnis
Vorgehen für den weiteren Verlauf dieser Übung bestätigt und übernommen.

---

## Session Log

### Benutzeranfrage (Übersetzt aus dem Vietnamesischen)
Erstelle jetzt noch eine Klasse, die mehrere Fehler in einer einzigen Zeile abfangen kann. Der Fehler soll in eine Variable e umgewandelt werden, um sie auszugeben.

### Durchgeführte Aktionen
- Klasse `MultiErrorHandler` mit Methode `calculate()` in `informatik4_oop_java_zu_python.py` ergänzt
- Multi-Catch mit `except (ValueError, ZeroDivisionError) as e:` implementiert, Java-Äquivalent `catch (NumberFormatException | ArithmeticException e)` als Kommentar ergänzt
- Fehlermeldung über `print("Error: " + str(e))` ausgegeben
- `main.py` automatisch aktualisiert (gemäß neuer Arbeitsweise) und getestet: gültige Division, Division durch 0 und ungültige Eingabe — alle drei Fälle korrekt

### Ergebnis
Klasse erfolgreich erstellt und getestet: liefert bei gültiger Division das Ergebnis, bei Division durch 0 "Error: division by zero" und bei ungültiger Eingabe die entsprechende Fehlermeldung über die Variable e.

---

## Session Log

### Benutzeranfrage (Übersetzt aus dem Vietnamesischen)
Erstelle eine Klasse, die alle Ausnahmen abfängt (`CatchAllHandler`), ebenfalls mit Division a durch b. Danach soll erklärt werden, wann man diese Art von Exception verwendet.

### Durchgeführte Aktionen
- Klasse `CatchAllHandler` mit Methode `calculate()` in `informatik4_oop_java_zu_python.py` ergänzt
- `except Exception as e:` fängt alle gewöhnlichen Ausnahmen ab; Java-Äquivalent `catch (Exception e)` als Kommentar ergänzt
- `main.py` aktualisiert: Import von `CatchAllHandler` und Testaufruf hinzugefügt
- Erklärt, wann `except Exception` sinnvoll ist (unbekannte Fehlerquellen, externe Bibliotheken) und wann es vermieden werden sollte

### Ergebnis
Klasse erfolgreich erstellt; Unterschied zu spezifischen Exceptions und Einsatzbereiche von `except Exception` erklärt.

---

## Session Log

### Benutzeranfrage (Übersetzt aus dem Vietnamesischen)
Kann ich im Terminal auswählen, welche Klasse ich verwenden möchte?

### Durchgeführte Aktionen
- `main.py` umgeschrieben: Konsolenmenü mit Optionen 1–4 für alle vorhandenen Klassen implementiert
- Benutzer kann per Zahleneingabe die gewünschte Klasse auswählen; ungültige Eingabe gibt "Ungültige Auswahl." aus

### Ergebnis
`main.py` zeigt beim Start ein interaktives Auswahlmenü an; nur die gewählte Klasse wird ausgeführt.

---

## Session Log

### Benutzeranfrage (Übersetzt aus dem Vietnamesischen)
Erstelle eine Klasse mit `raise`: Der Benutzer gibt sein Alter ein. `raise` soll ausgelöst werden, wenn die Zahl kleiner als 0 ist, und `except` soll greifen, wenn keine gültige Zahl eingegeben wird.

### Durchgeführte Aktionen
- Klasse `AgeValidator` mit Methode `validate_age()` in `informatik4_oop_java_zu_python.py` ergänzt
- `raise ValueError("Age cannot be negative.")` bei negativem Alter; Java-Äquivalent `throw new IllegalArgumentException(...)` als Kommentar ergänzt
- `except ValueError as e:` fängt sowohl `int()`-Fehler als auch den manuellen `raise` ab
- `main.py` aktualisiert: Import von `AgeValidator` und Menüoption 5 hinzugefügt

### Ergebnis
Klasse erfolgreich erstellt: negative Zahl löst `raise` aus, ungültige Eingabe wird von `except` abgefangen, gültige Zahl gibt "Your age is: X" aus.

---

## Session Log

### Benutzeranfrage (Übersetzt aus dem Vietnamesischen)
In der Klasse `NumberInputHandler` soll ein `else`-Block hinzugefügt werden: Wenn die Eingabe gültig ist, wird `"You entered", num` ausgegeben. Danach soll ein `finally`-Block mit `"end of operation"` ergänzt werden. Abschließend soll `finally` auch in alle anderen Klassen eingefügt werden.

### Durchgeführte Aktionen
- `NumberInputHandler.read_number()` umstrukturiert: `print` aus dem `try`-Block entfernt und in einen `else`-Block verschoben (`print("You entered", num)`)
- `finally: print("end of operation")` zu `NumberInputHandler` hinzugefügt
- `finally: print("end of operation")` zu `DivisionHandler` hinzugefügt
- `finally: print("end of operation")` zu `MultiErrorHandler` hinzugefügt
- `finally: print("end of operation")` zu `CatchAllHandler` hinzugefügt
- `finally: print("end of operation")` zu `AgeValidator` hinzugefügt
- Java-Äquivalentkommentare (`} finally {`, `System.out.println("end of operation");`) bei jeder Änderung ergänzt

### Ergebnis
Alle 5 Klassen verfügen nun über die vollständige `try/except/else/finally`-Struktur (wo anwendbar) mit `"end of operation"` als abschließender Ausgabe.
