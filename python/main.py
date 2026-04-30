from fastapi import FastAPI
from hello_controller import HelloController
import uvicorn

app = FastAPI()

hello_controller = HelloController()
app.include_router(hello_controller.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
