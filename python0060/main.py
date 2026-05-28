import logging

from greeter_service import GreeterService
from hello_world_application import HelloWorldApplication

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s - %(message)s",
)

if __name__ == "__main__":
    greeter = GreeterService()
    application = HelloWorldApplication(greeter)
    application.run()
