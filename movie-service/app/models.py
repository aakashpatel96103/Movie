from sqlalchemy import Column, Integer, String
from .database import Base

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    show_time = Column(String, nullable=False)
    total_seats = Column(Integer, default=50)
    available_seats = Column(Integer, default=50)
