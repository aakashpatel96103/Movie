from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Movie
from ..schemas import MovieCreate, MovieResponse

router = APIRouter(prefix="/movies", tags=["Movies"])

@router.post("/", response_model=MovieResponse)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    item = Movie(
        title=movie.title,
        show_time=movie.show_time,
        total_seats=movie.total_seats,
        available_seats=movie.total_seats
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.get("/", response_model=list[MovieResponse])
def get_movies(db: Session = Depends(get_db)):
    return db.query(Movie).all()

@router.get("/{movie_id}", response_model=MovieResponse)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    item = db.query(Movie).filter(Movie.id == movie_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Movie not found")
    return item

@router.put("/{movie_id}", response_model=MovieResponse)
def update_movie(movie_id: int, data: MovieCreate, db: Session = Depends(get_db)):
    item = db.query(Movie).filter(Movie.id == movie_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Movie not found")
    item.title = data.title
    item.show_time = data.show_time
    item.total_seats = data.total_seats
    item.available_seats = min(item.available_seats, data.total_seats)
    db.commit()
    db.refresh(item)
    return item

@router.delete("/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    item = db.query(Movie).filter(Movie.id == movie_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Movie not found")
    db.delete(item)
    db.commit()
    return {"message": "Movie deleted successfully"}

@router.post("/{movie_id}/reserve")
def reserve_seat(movie_id: int, db: Session = Depends(get_db)):
    item = db.query(Movie).filter(Movie.id == movie_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Movie not found")
    if item.available_seats <= 0:
        raise HTTPException(status_code=400, detail="No seats available")
    item.available_seats -= 1
    db.commit()
    return {"message": "Seat reserved successfully", "movie_id": movie_id,
            "available_seats": item.available_seats}

@router.post("/{movie_id}/release")
def release_seat(movie_id: int, db: Session = Depends(get_db)):
    item = db.query(Movie).filter(Movie.id == movie_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Movie not found")
    if item.available_seats < item.total_seats:
        item.available_seats += 1
        db.commit()
    return {"message": "Seat released successfully", "movie_id": movie_id,
            "available_seats": item.available_seats}
