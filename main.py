from fastapi import FastAPI

from src import models, api
from src.database import engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(api.router)
