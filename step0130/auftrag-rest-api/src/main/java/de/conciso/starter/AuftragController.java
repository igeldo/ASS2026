package de.conciso.starter;

import lombok.extern.slf4j.Slf4j;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@Slf4j
@RestController
@RequestMapping("/api/auftrag")
public class AuftragController {

  @PostMapping(produces = MediaType.APPLICATION_JSON_VALUE)
  public ResponseEntity<AuftragResponseRepresentation> create(
          @RequestParam("bestellNummer") String bestellNummer
  ) {
    log.info("AuftragController.create, bestellnummer: {}", bestellNummer);
    return ResponseEntity.ok(new AuftragResponseRepresentation(42, bestellNummer));
  }
}
