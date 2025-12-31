from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

Base = declarative_base()
engine = create_engine("sqlite:///spotify_stats.db")
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    spotify_id = Column(String, unique=True)
    display_name = Column(String)
    profile_image_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class TopTrack(Base):
    __tablename__ = "top_track"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    snapshot_id = Column(Integer, ForeignKey("stats_snapshot.id"))
    track_id = Column(String)
    track_name = Column(String)
    artist_name = Column(String)
    time_range = Column(String)
    rank = Column(Integer)
    fetched_at = Column(DateTime)
    image_url = Column(String)
    
class TopArtist(Base):
    __tablename__ = "top_artist"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    snapshot_id = Column(Integer, ForeignKey("stats_snapshot.id"))
    artist_id = Column(String)
    genres = Column(String)
    artist_name = Column(String)
    time_range = Column(String)
    rank = Column(Integer)
    fetched_at = Column(DateTime)
    image_url = Column(String)
    
class RecentlyPlayed(Base):
    __tablename__ = "recently_played"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    snapshot_id = Column(Integer, ForeignKey("stats_snapshot.id"))
    track_id = Column(String)
    track_name = Column(String)
    artist_name = Column(String)
    played_at = Column(DateTime)
    fetched_at = Column(DateTime)
    
class StatsSnapshot(Base):
    __tablename__ = "stats_snapshot"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime)
    snapshot_type = Column(String, default="auto")

def init_db():
    Base.metadata.create_all(engine)
    