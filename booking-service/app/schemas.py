from pydantic import BaseModel

class BookingCreate(BaseModel):
    customer_name: str
    movie_id: int
    seats: int = 1

class BookingResponse(BaseModel):
    id: int
    customer_name: str
    movie_id: int
    seats: int
    status: str

    class Config:
        from_attributes = True
