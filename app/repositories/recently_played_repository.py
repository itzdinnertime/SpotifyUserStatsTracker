from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from ..models import RecentlyPlayed
from .base import BaseRepo

class RecentlyPlayedRepository(BaseRepo[RecentlyPlayed]):
    
    def __init__(self, session: Session):
        super().__init__(session, RecentlyPlayed)

    def get_recent(self, limit: int = 50):
        return self.session.query(RecentlyPlayed)
    
    def save_recently_played(self, user_id: int, tracks_data: List[dict]) -> List[RecentlyPlayed]:
        
        tracks = []
        
        for track_data in tracks_data:
            track = RecentlyPlayed(
                user_id=user_id,
                track_id=track_data['id'],
                track_name=track_data['name'],
                artist_name=track_data['artist'],
                played_at=track_data.get('played_at'),
                fetched_at=datetime.utcnow()
            )
            tracks.append(track)
        
        self.add_all(tracks)
        return tracks
