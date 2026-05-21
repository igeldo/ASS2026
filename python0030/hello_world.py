import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)-8s %(name)s - %(message)s",
)

log = logging.getLogger(__name__)


class HelloWorld:
    def run(self):
        log.debug("Starte HelloWorld")
        log.info("Hello, World!")
        log.warning("Dies ist eine Warnung")
        log.error("Dies ist ein Fehler")


if __name__ == "__main__":
    HelloWorld().run()
