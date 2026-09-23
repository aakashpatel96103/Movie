from sqlalchemy import Column, Integer, String
from .database import Base

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, nullable=False)
    movie_id = Column(Integer, nullable=False)
    seats = Column(Integer, default=1)
    status = Column(String, default="confirmed")
