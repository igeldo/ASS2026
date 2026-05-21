import logging


class HelloWorld:
    _log = logging.getLogger(__qualname__)

    def run(self):
        self._log.debug("Starte HelloWorld")
        self._log.info("Hello, World!")
        self._log.warning("Dies ist eine Warnung")
        self._log.error("Dies ist ein Fehler")
