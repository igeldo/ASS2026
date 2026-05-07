# Python Starter

## Step 10

Unser erstes Python-Programm

### Voraussetzungen

- Python 3.12+ (Installationscheck: `python3 --version`)

### Einmalig: Virtuelle Umgebung anlegen

```shell
python3 -m venv .venv
```

### Virtuelle Umgebung aktivieren

```shell
source .venv/bin/activate
```

Nach der Aktivierung zeigt das Terminal `(.venv)` als Präfix.

### Ausführen

```shell
python hello_world.py
```

### Starten in PyCharm

1. Projekt öffnen: **File → Open** → Verzeichnis `python0010` auswählen
2. Interpreter konfigurieren: **File → Settings → Project → Python Interpreter → Add Interpreter → Add Local Interpreter**
   - **Existing** auswählen, Pfad: `.venv/bin/python`
3. `hello_world.py` im Editor öffnen
4. Rechtsklick im Editor → **Run 'hello_world'**

Beim ersten Öffnen erkennt PyCharm das `.venv` oft automatisch und schlägt es als Interpreter vor.

### Deaktivieren der virtuellen Umgebung

```shell
deactivate
```

### Was passiert hier?

- `def main()` definiert die Einstiegsfunktion
- `if __name__ == "__main__"` ist Pythons Konvention, um Code nur bei direktem Aufruf auszuführen (nicht beim Importieren)
- Die virtuelle Umgebung (`.venv`) isoliert Python-Installationen projektweise — analog zu einem eigenen Classpath in Java
