from sqlalchemy.orm import Session

from ..models import User
from .base import BaseRepo

class UserRepository(BaseRepo[User]):
    
    def __init__(self, session: Session):
        super().__init__(session, User)
    
    def get_by_spotify_id(self, spotify_id: str) -> User | None:
        return self.session.query(User).filter(User.spotify_id == spotify_id).first()
        
    def get_or_create(self, spotify_id: str, display_name: str = None) -> User:
        user = self.get_by_spotify_id(spotify_id)
        
        if not user:
            user = self.add(User(spotify_id=spotify_id, display_name=display_name))
        
        return user
