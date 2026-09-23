from fastapi import FastAPI
from .database import Base, engine
from .routers.movies import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Movie Service")
app.include_router(router)

@app.get("/")
def root():
    return {"service": "Movie Service", "status": "running"}
