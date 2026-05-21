# Python Starter

## Step 30

Logging mit dem Python Standard-Logging-Modul

### Was ist neu?

Python bringt ein vollständiges Logging-Framework bereits in der Standardbibliothek mit — kein externes Paket nötig.

| Java (SLF4J + Logback)                              | Python                                      |
|-----------------------------------------------------|---------------------------------------------|
| `import org.slf4j.Logger`                           | `import logging`                            |
| `LoggerFactory.getLogger(HelloWorld.class)`         | `logging.getLogger(__name__)`               |
| `log.info("Hello")`                                 | `log.info("Hello")`                         |
| `logback.xml`                                       | `logging.basicConfig(...)`                  |

### Voraussetzungen

- Python 3.12+
- uv installiert

### Einrichten und Ausführen

```shell
uv sync
uv run python hello_world.py
```

Erwartete Ausgabe:

```
2026-05-21 10:00:00,000 DEBUG    __main__ - Starte HelloWorld
2026-05-21 10:00:00,001 INFO     __main__ - Hello, World!
2026-05-21 10:00:00,001 WARNING  __main__ - Dies ist eine Warnung
2026-05-21 10:00:00,001 ERROR    __main__ - Dies ist ein Fehler
```

### Log-Level

Python kennt fünf Log-Level (von niedrig nach hoch):

| Level      | Methode            | Verwendung                        |
|------------|--------------------|-----------------------------------|
| `DEBUG`    | `log.debug(...)`   | Entwickler-Infos                  |
| `INFO`     | `log.info(...)`    | Normaler Programmablauf           |
| `WARNING`  | `log.warning(...)` | Unerwartetes, aber kein Fehler    |
| `ERROR`    | `log.error(...)`   | Fehler, Programm läuft weiter     |
| `CRITICAL` | `log.critical(...)`| Schwerwiegender Fehler            |

Mit `level=logging.DEBUG` in `basicConfig` werden alle Level ausgegeben.
Setzt man `level=logging.WARNING`, erscheinen nur `WARNING`, `ERROR` und `CRITICAL`.

### Was passiert hier?

- `logging.basicConfig(...)` konfiguriert das Logging einmalig beim Programmstart (analog zu `logback.xml`)
- `format=...` legt das Ausgabeformat fest: Zeitstempel, Level, Logger-Name, Nachricht
- `logging.getLogger(__name__)` erzeugt einen Logger, dessen Name dem Modulnamen entspricht — in `hello_world.py` ist das `__main__` bei direktem Aufruf
- Jede Klasse oder jedes Modul kann einen eigenen Logger haben, was die Ausgabe filterbar macht
