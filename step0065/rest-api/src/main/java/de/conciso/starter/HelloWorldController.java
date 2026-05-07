package de.conciso.starter;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/hello")
public class HelloWorldController {

  private static final Logger log = LoggerFactory.getLogger(HelloWorldController.class);

  @GetMapping(produces = MediaType.TEXT_PLAIN_VALUE)
  public String sayHello(@RequestParam("name") String name) {
    var greeter = new GreeterService();
    var greetings = greeter.greet(name);
    log.info("response: " + greetings);
    return greetings;
  }

  @GetMapping(value = "/{name}", produces = MediaType.TEXT_PLAIN_VALUE)
  public String sayHelloWithPathVariable(@PathVariable("name") String name) {
    return sayHello(name);
  }
}
