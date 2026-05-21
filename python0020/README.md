# Python Starter

## Step 20

Projektverwaltung mit **uv** und **pyproject.toml**

### Was ist neu?

In Step 10 haben wir `venv` direkt genutzt und Pakete mit `pip` installiert.
Ab Step 20 verwenden wir **uv** — ein modernes Tool, das `venv`, `pip` und mehr in einem Befehl vereint.

| Step 10 (klassisch)          | Step 20 (uv)              |
|------------------------------|---------------------------|
| `python3 -m venv .venv`      | `uv sync`                 |
| `source .venv/bin/activate`  | entfällt                  |
| `pip install <paket>`        | `uv add <paket>`          |
| `python hello_world.py`      | `uv run python hello_world.py` |

Für Java-Entwickler: `pyproject.toml` ist Pythons Entsprechung zur `pom.xml`.

### Voraussetzungen

- Python 3.12+
- uv installiert

#### uv installieren (einmalig)

```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Installationscheck:

```shell
uv --version
```

### Projekt einrichten

Beim ersten Auschecken des Projekts einmalig ausführen:

```shell
uv sync
```

`uv sync` liest `pyproject.toml`, erstellt automatisch eine `.venv` und installiert alle Abhängigkeiten.
Das Ergebnis wird in `uv.lock` festgehalten (analog zu `pom.xml` mit fixen Versionen).

### Ausführen

```shell
uv run python hello_world.py
```

`uv run` aktiviert die virtuelle Umgebung automatisch — kein `source .venv/bin/activate` nötig.

### Abhängigkeit hinzufügen

```shell
uv add requests
```

Dieser Befehl:
1. Trägt `requests` in `pyproject.toml` ein
2. Installiert das Paket in `.venv`
3. Aktualisiert `uv.lock`

### Starten in PyCharm

1. Projekt öffnen: **File → Open** → Verzeichnis `python0020` auswählen
2. Interpreter konfigurieren: **File → Settings → Project → Python Interpreter → Add Interpreter → Add Local Interpreter**
   - **Existing** auswählen, Pfad: `.venv/bin/python`
3. `hello_world.py` im Editor öffnen
4. Rechtsklick im Editor → **Run 'hello_world'**

PyCharm erkennt `pyproject.toml` automatisch und schlägt die `.venv` als Interpreter vor.

### Was gehört ins Git?

| Datei / Verzeichnis | Einchecken? | Warum |
|---------------------|-------------|-------|
| `pyproject.toml`    | Ja          | Projektdefinition |
| `uv.lock`           | Ja          | Reproduzierbare Builds (analog zu `pom.xml` mit fixen Versionen) |
| `.python-version`   | Ja          | Legt die Python-Version fest |
| `.venv/`            | Nein        | Wird von `uv sync` generiert |

### Was passiert hier?

- `pyproject.toml` beschreibt das Projekt: Name, Version, Python-Mindestversion und Abhängigkeiten
- `.python-version` teilt uv mit, welche Python-Version genutzt werden soll
- `uv.lock` pinnt alle Paketversionen exakt fest — damit laufen Builds überall identisch
