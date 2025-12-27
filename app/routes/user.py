from fastapi import APIRouter
from ..models import Session, User

router = APIRouter()

@router.get("/profile")
def get_profile():
    session = Session()
    user = session.query(User).first()
    return {"spotify_id": user.spotify_id, "display_name": user.display_name}