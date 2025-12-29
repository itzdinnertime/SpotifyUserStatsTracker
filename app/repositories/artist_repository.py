from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from ..models import TopArtist
from .base import BaseRepo

class ArtistRepository(BaseRepo[TopArtist]):
    
    def __init__(self, session: Session):
        super().__init__(session, TopArtist)

    def get_by_time_range(self, time_range: str ):
        return self.session.query(TopArtist).filter(TopArtist.time_range == time_range).order_by(TopArtist.rank).all()
        
    def save_top_artists(self, user_id: str, artist_data: List[dict], time_range: str) -> List[TopArtist]:
        
        artists = []
        
        for rank, artist_data in enumerate(artist_data, 1):
            artist =  TopArtist(
                user_id=user_id,
                artist_id=artist_data['id'],
                artist_name=artist_data['name'],
                genres=artist_data.get('genres', ''),
                time_range=time_range,
                rank=rank,
                fetched_at=datetime.utcnow(),
                image_url=artist_data.get('image_url')
            )
            artists.append(artist)
        
        self.add_all(artists)
        return artists
