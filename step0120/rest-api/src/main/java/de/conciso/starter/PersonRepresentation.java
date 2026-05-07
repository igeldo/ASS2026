package de.conciso.starter;

import lombok.Value;

@Value
public class PersonRepresentation {

  int id;
  String vorname;
  String name;

  static PersonRepresentation from(Person person) {
    return new PersonRepresentation(person.getId(), person.getVorname(), person.getName());
  }
}
