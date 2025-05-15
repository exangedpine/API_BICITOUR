from fastapi import FastAPI
from routes import recorrido

app = FastAPI()

app.include_router(recorrido.router)
