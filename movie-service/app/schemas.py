from pydantic import BaseModel

class MovieCreate(BaseModel):
    title: str
    show_time: str
    total_seats: int = 50

class MovieResponse(BaseModel):
    id: int
    title: str
    show_time: str
    total_seats: int
    available_seats: int

    class Config:
        from_attributes = True
