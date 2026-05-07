package de.conciso.starter;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class HelloWorldApplication {

  private static final Logger log = LoggerFactory.getLogger(HelloWorldApplication.class);

  public void run() {
    var greeter = new GreeterService();
    log.info(greeter.greet("World"));
  }
}
