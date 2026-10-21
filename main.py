from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from backend.database import db
from backend.routes import products, chatbot

app = FastAPI()
app.include_router(products.router)
app.include_router(chatbot.router)
app.mount("/images", StaticFiles(directory="static/images"), name="images")


@app.get("/health")
def health_check():
    db.command("ping")
    return {"status": "connected to MongoDB"}


app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")