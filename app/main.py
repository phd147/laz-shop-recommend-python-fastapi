from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI

from .routers import recommend

app = FastAPI()

app.include_router(recommend.router)


@app.get('/')
def read_root():
    return {"Hello": "World"}
