package de.conciso.starter;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class HelloWorldApplication {

  private static final Logger log = LoggerFactory.getLogger(HelloWorldApplication.class);

  private final Greeter greeter;

  public HelloWorldApplication(Greeter greeter) {
    this.greeter = greeter;
  }

  public void run() {
    log.info(greeter.greet("World"));
  }
}
