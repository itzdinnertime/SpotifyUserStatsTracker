from fastapi import APIRouter, Query
from ..models import Session, TopTrack, TopArtist, RecentlyPlayed, StatsSnapshot
from fastapi import BackgroundTasks
import pytz

from ..fetch_data import main as fetch_data_main

router = APIRouter()

@router.post("/refresh")
def refresh_stats(background_tasks: BackgroundTasks):
    # Run fetch_data in the background so the API returns immediately
    background_tasks.add_task(fetch_data_main)
    return {"status": "refresh started"}


@router.get("/top-tracks")
def get_top_tracks(time_range: str = "short_term", snapshot_id: int = None):
    session = Session()
    if not snapshot_id:
        latest_snapshot = session.query(StatsSnapshot).order_by(StatsSnapshot.created_at.desc()).first()
        if latest_snapshot:
            snapshot_id = latest_snapshot.id
    query = session.query(TopTrack).filter_by(time_range=time_range)
    if snapshot_id:
        query = query.filter_by(snapshot_id=snapshot_id)
    tracks = query.order_by(TopTrack.rank).all()
    session.close()
    return [
        {
            "rank": t.rank, 
            "track_name": t.track_name, 
            "artist_name": t.artist_name, 
            "image_url": t.image_url,
            "snapshot_id": t.snapshot_id
        } 
        for t in tracks
    ]


@router.get("/top-artists")
def get_top_artists(
    time_range: str = "short_term",
    snapshot_id: int = None
):
    session = Session()
    if not snapshot_id:
        latest_snapshot = session.query(StatsSnapshot).order_by(StatsSnapshot.created_at.desc()).first()
        if latest_snapshot:
            snapshot_id = latest_snapshot.id
    query = session.query(TopArtist).filter_by(time_range=time_range)
    if snapshot_id:
        query = query.filter_by(snapshot_id=snapshot_id)
    artists = query.order_by(TopArtist.rank).all()
    session.close()
    return [
        {
            "rank": a.rank,
            "artist_name": a.artist_name,
            "genres": a.genres,
            "image_url": a.image_url,
            "snapshot_id": a.snapshot_id
        }
        for a in artists
    ]

@router.get("/recently-played")
def get_recently_played(
    timezone: str = Query("UTC"),
    snapshot_id: int = None
):
    session = Session()
    query = session.query(RecentlyPlayed)
    if snapshot_id:
        query = query.filter_by(snapshot_id=snapshot_id)
    tracks = query.order_by(RecentlyPlayed.played_at.desc()).limit(50).all()
    session.close()
    tz = pytz.timezone(timezone)
    return [
        {
            "track_name": t.track_name,
            "artist_name": t.artist_name,
            "played_at": t.played_at.astimezone(tz).isoformat() if t.played_at else None,
            "snapshot_id": t.snapshot_id
        }
        for t in tracks
    ]

@router.get("/snapshots")
def get_snapshots():
    session = Session()
    snapshots = session.query(StatsSnapshot).order_by(StatsSnapshot.created_at.desc()).all()
    session.close()
    return [
        {
            "id": s.id,
            "created_at": s.created_at.isoformat() if s.created_at else None,
            "snapshot_type": s.snapshot_type
        }
        for s in snapshots
    ]