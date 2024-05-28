from fastapi import FastAPI
from api.routes import search_router
import uvicorn

def init_app():
    app = FastAPI()
    app.include_router(search_router)
    return app


app = init_app()


@app.get("/")
def read_root():
    return {
        "message": "Make a post request to /ask to ask a question about Meditations by Marcus Aurelius"
    }


if __name__ == "__main__":
    uvicorn.run(app)
