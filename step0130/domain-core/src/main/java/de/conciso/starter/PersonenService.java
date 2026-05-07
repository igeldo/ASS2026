package de.conciso.starter;

import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Slf4j
@Service
public class PersonenService implements Personen {

  private final PersonDAO personDAO;

  private final Auftraege auftraege;

  public PersonenService(PersonDAO personDAO, Auftraege auftraege) {
    this.personDAO = personDAO;
    this.auftraege = auftraege;
  }

  @Override
  public Person create(String vorname, String name) {
    var auftrag = auftraege.create(Auftrag.builder().bestellNummer(vorname).build());
    log.info("created auftrag: " + auftrag.getId());

    log.info("create person: {} {}", vorname, name);
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
