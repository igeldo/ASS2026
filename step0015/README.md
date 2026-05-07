# Java Starter #

## Step 15

Build mit Maven

### Prerequisites
- Java 21 JDK
- Maven

Prüfung mit:
```shell
mvn -version
```

Erwartetes Ergebnis (Beispiel):
```shell
Maven home: /home/georg/jee/seu/maven
Java version: 21.0.6, vendor: Eclipse Adoptium, runtime: /home/georg/jee/seu/linux/jdk-21.0.6+7
Default locale: de_DE, platform encoding: UTF-8
OS name: "linux", version: "6.8.0-55-generic", arch: "amd64", family: "unix"
```

### Build and run

```shell
mvn clean package
java -classpath target/starter-1.0-SNAPSHOT.jar de.conciso.starter.HelloWorld
```
