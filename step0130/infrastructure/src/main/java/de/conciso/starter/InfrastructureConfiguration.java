package de.conciso.starter;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.reactive.function.client.ClientRequest;
import org.springframework.web.reactive.function.client.ClientResponse;
import org.springframework.web.reactive.function.client.ExchangeFunction;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

@Slf4j
@Configuration
public class InfrastructureConfiguration {

  @Bean
  public WebClient auftrageWebClient(@Value("${service.auftrag.url}") String url) {
    log.info("creating WebClient for {}", url);
    return WebClient.builder()
        .baseUrl(url)
            .filter(InfrastructureConfiguration::setAuthorizationToken)
            .build();
  }

  private static Mono<ClientResponse> setAuthorizationToken(ClientRequest request, ExchangeFunction next) {
    return Mono.deferContextual(contextView -> next.exchange(contextView.getOrEmpty("authorizationToken")
            .map(String.class::cast)
            .map(token -> ClientRequest.from(request)
                    .header("Authorization", token)
                    .build()
            )
            .orElse(request)));
  }
}
