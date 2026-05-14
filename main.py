from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from database import engine
from models import Base

from routers.prompts import router as prompt_router
from routers import auth

Base.metadata.create_all(bind=engine)

app = FastAPI()


app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


app.include_router(prompt_router)
app.include_router(auth.router)