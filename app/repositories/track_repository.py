from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from ..models import TopTrack
from .base import BaseRepo

class TrackRepository(BaseRepo[TopTrack]):
    
    def __init__(self, session: Session):
        super().__init__(session, TopTrack)
    
    def get_by_time_range(self, time_range: str):
        return self.session.query(TopTrack).filter(TopTrack.time_range == time_range).order_by(TopTrack.rank).all()
        
    def save_top_tracks(self, user_id: int, tracks_data: List[dict], time_range: str) -> List[TopTrack]:
        
        tracks = []
        
        for rank, track_data in enumerate(tracks_data, 1):
            track = TopTrack(
                user_id=user_id,
                track_id=track_data['id'],
                track_name=track_data['name'],
                artist_name=track_data['artist'],
                time_range=time_range,
                rank=rank,
                fetched_at=datetime.utcnow(),
                image_url=track_data.get('image_url')
            )
            tracks.append(track)
        
        self.add_all(tracks)
        return tracks
    