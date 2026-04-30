# Hello World REST Service

Ein einfacher REST-Service auf Basis von Spring Boot.

## Anforderungen

- `GET /api/hello` antwortet mit `Hello World!`
- `GET /api/hello?name={name}` antwortet mit `Hello {name}!`

## Voraussetzungen

- Java 25
- Maven

## Starten

```bash
mvn spring-boot:run
```

Der Service startet auf Port `8080`.

## Endpoints

| Methode | URL                          | Antwort          |
|---------|------------------------------|------------------|
| GET     | `/api/hello`                 | `Hello World!`   |
| GET     | `/api/hello?name={name}`     | `Hello {name}!`  |

## Beispiele

```bash
curl http://localhost:8080/api/hello
# Hello World!

curl "http://localhost:8080/api/hello?name=Georg"
# Hello Georg!
```

## Request-Logging

Der eingebettete Tomcat-Server gibt alle eingehenden Requests auf der Konsole aus:

```
127.0.0.1 - "GET /api/hello HTTP/1.1" 200
127.0.0.1 - "GET /api/hello?name=Georg HTTP/1.1" 200
```

Das Logging ist in `src/main/resources/application.properties` konfiguriert. Es funktioniert auf macOS und Linux, aber nicht unter Windows.

## Build

Ausführbare JAR-Datei erzeugen:

```bash
mvn package
```
