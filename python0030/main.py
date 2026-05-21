import logging

from hello_world import HelloWorld

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)-8s %(name)s - %(message)s",
)

if __name__ == "__main__":
    HelloWorld().run()
