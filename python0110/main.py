import logging

import uvicorn

from database import engine
from orm_models import Base

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s - %(message)s",
)

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    uvicorn.run("app:app", host="0.0.0.0", port=8080)
