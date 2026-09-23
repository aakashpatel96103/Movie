import os
import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Booking
from ..schemas import BookingCreate, BookingResponse

router = APIRouter(prefix="/bookings", tags=["Bookings"])
MOVIE_SERVICE_URL = os.getenv("MOVIE_SERVICE_URL", "http://localhost:8001")

@router.post("/", response_model=BookingResponse)
def create_booking(data: BookingCreate, db: Session = Depends(get_db)):
    if data.seats != 1:
        raise HTTPException(
            status_code=400,
            detail="Book one seat at a time in this simple project"
        )

    try:
        response = httpx.post(
            f"{MOVIE_SERVICE_URL}/movies/{data.movie_id}/reserve",
            timeout=5
        )
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Movie Service is unavailable")

    if response.status_code != 200:
        detail = "Seat reservation failed"
        try:
            detail = response.json().get("detail", detail)
        except Exception:
            pass
        raise HTTPException(status_code=response.status_code, detail=detail)

    booking = Booking(
        customer_name=data.customer_name,
        movie_id=data.movie_id,
        seats=1,
        status="confirmed"
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking

@router.get("/", response_model=list[BookingResponse])
def get_bookings(db: Session = Depends(get_db)):
    return db.query(Booking).all()

@router.get("/{booking_id}", response_model=BookingResponse)
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    item = db.query(Booking).filter(Booking.id == booking_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Booking not found")
    return item

@router.delete("/{booking_id}")
def cancel_booking(booking_id: int, db: Session = Depends(get_db)):
    item = db.query(Booking).filter(Booking.id == booking_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Booking not found")
    if item.status == "cancelled":
        return {"message": "Booking already cancelled"}

    try:
        response = httpx.post(
            f"{MOVIE_SERVICE_URL}/movies/{item.movie_id}/release",
            timeout=5
        )
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Movie Service is unavailable")

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Could not release the seat")

    item.status = "cancelled"
    db.commit()
    return {"message": "Booking cancelled successfully", "booking_id": item.id}
