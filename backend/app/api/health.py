from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.models.user import User


router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("/database")
def database_health(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT 1"))
    
    return {
        "status": "healthy",
        "database": result.scalar(),
    }

@router.get("/users")
def users_health(db: Session = Depends(get_db)):
    count = db.query(User).count()

    return {
        "status": "healthy",
        "users_count": count,
    }