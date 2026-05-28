import logging

import uvicorn
from sqlalchemy import text

from database import engine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s - %(message)s",
)

if __name__ == "__main__":
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS persons (
                id SERIAL PRIMARY KEY,
                vorname VARCHAR(100) NOT NULL,
                name VARCHAR(100) NOT NULL
            )
        """))
        conn.commit()
    uvicorn.run("app:app", host="0.0.0.0", port=8080)
