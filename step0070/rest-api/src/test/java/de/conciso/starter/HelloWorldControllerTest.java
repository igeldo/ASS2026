package de.conciso.starter;

import org.junit.jupiter.api.*;

import static org.assertj.core.api.Assertions.assertThat;

@DisplayNameGeneration(DisplayNameGenerator.ReplaceUnderscores.class)
class HelloWorldControllerTest {

  private static final String NAME = "Georg";
  private static final String GREETINGS = "Hello " + NAME;

  HelloWorldController cut;

  @Nested
  class Given_the_Greeter_responds {

    @BeforeEach
    void arrange() {
      cut = new HelloWorldController(new GreeterService());
    }

    @Nested
    class When_calling_sayHello {
      String result;

      @BeforeEach
      void act() {
        result = cut.sayHello(NAME);
      }

      @Test
      void then_result_is_correct() {
        assertThat(result).isEqualTo(GREETINGS);
      }
    }
  }
}
