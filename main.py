from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from backend.database import db
from backend.routes import products

app = FastAPI()
app.include_router(products.router)
app.mount("/images", StaticFiles(directory="static/images"), name="images")
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")


@app.get("/")
def read_root():
    return {"message": "Hello from LUXE backend"}


@app.get("/health")
def health_check():
    db.command("ping")
    return {"status": "connected to MongoDB"}