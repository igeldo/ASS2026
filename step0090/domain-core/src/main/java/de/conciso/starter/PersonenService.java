package de.conciso.starter;

import java.util.Optional;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

// todo: Test zufügen
@Service
public class PersonenService implements Personen {

  private static final Logger log = LoggerFactory.getLogger(PersonenService.class);

  private final PersonDAO personDAO;

  public PersonenService(PersonDAO personDAO) {
    this.personDAO = personDAO;
  }

  @Override
  public Person create(String vorname, String name) {
    log.info("create person: " + vorname + " " + name);
    var person = new Person(vorname, name);
    return personDAO.save(person);
  }

  @Override
  public Optional<Person> findById(int id) {
    log.info("looking for person with id: " + id);
    var found = personDAO.findById(id);
    if (found.isEmpty()) {
      log.warn("no person found with id: " + id);
    }
    return found;
  }
}
