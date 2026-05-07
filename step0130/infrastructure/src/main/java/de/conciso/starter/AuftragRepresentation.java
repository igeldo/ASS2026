package de.conciso.starter;

import lombok.Builder;
import lombok.Value;
import lombok.extern.jackson.Jacksonized;

@Jacksonized
@Value
@Builder
public class AuftragRepresentation {
  int id;
  String bestellNummer;

  public Auftrag toAuftrag() {
    return Auftrag.builder()
            .id(id)
            .bestellNummer(bestellNummer)
            .build();
  }
}
