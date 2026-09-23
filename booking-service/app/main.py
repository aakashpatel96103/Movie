from fastapi import FastAPI
from .database import Base, engine
from .routers.bookings import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Booking Service")
app.include_router(router)

@app.get("/")
def root():
    return {"service": "Booking Service", "status": "running"}
