from fastapi import APIRouter
from ..models import Session, TopTrack, TopArtist, RecentlyPlayed

router = APIRouter()


@router.get("/top-tracks")
def get_top_tracks(time_range: str = "short_term"):
    session = Session()
    tracks = session.query(TopTrack).filter_by(time_range=time_range).order_by(TopTrack.rank).all()
    session.close()
    return [{"rank": t.rank, "track_name": t.track_name, "artist_name": t.artist_name} for t in tracks]


@router.get("/top-artists")
def get_top_artists(time_range: str = "short_term"):
    session = Session()
    artists = session.query(TopArtist).filter_by(time_range=time_range).order_by(TopArtist.rank).all()
    session.close()
    return [{"rank": a.rank, "artist_name": a.artist_name, "genres": a.genres} for a in artists]


@router.get("/recently-played")
def get_recently_played():
    session = Session()
    tracks = session.query(RecentlyPlayed).order_by(RecentlyPlayed.played_at.desc()).limit(50).all()
    session.close()
    return [
        {
            "track_name": t.track_name,
            "artist_name": t.artist_name,
            "played_at": t.played_at.isoformat() if t.played_at else None
        }
        for t in tracks
    ]