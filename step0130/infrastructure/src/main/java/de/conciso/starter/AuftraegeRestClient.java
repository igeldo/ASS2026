package de.conciso.starter;

import org.springframework.http.MediaType;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;

@Component
public class AuftraegeRestClient implements Auftraege {

  private final WebClient webClient;

  private final AuthorizationTokenHolder tokenHolder;

  public AuftraegeRestClient(WebClient webClient, AuthorizationTokenHolder tokenHolder) {
    this.webClient = webClient;
    this.tokenHolder = tokenHolder;
  }

  @Override
  public Auftrag create(Auftrag auftrag) {
    return webClient.post()
            .uri(uriBuilder -> uriBuilder.queryParam("bestellNummer", auftrag.getBestellNummer()).build())
            .accept(MediaType.APPLICATION_JSON)
            .exchangeToMono(clientResponse -> clientResponse.bodyToMono(AuftragRepresentation.class)
                    .map(AuftragRepresentation::toAuftrag)
            )
            .contextWrite(context -> context.put("authorizationToken", tokenHolder.getToken()))
            .block();
  }
}
