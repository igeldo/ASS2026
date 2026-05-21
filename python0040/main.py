import logging

from hello_world import HelloWorld

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s - %(message)s",
)

if __name__ == "__main__":
    HelloWorld("World").run()
    HelloWorld("Python").run()
