from fastapi import APIRouter
from ..models import Session, User

router = APIRouter()

@router.get("/profile")
def get_profile():
    session = Session()
    user = session.query(User).first()
    profile_image_url = None
    if hasattr(user, "profile_image_url"):
        profile_image_url = user.profile_image_url
    return {
        "spotify_id": user.spotify_id,
        "display_name": user.display_name,
        "profile_image_url": profile_image_url
    }