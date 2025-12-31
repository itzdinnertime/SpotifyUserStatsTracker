"""
CLI script to fetch Spotify data and save to database.
Run with: python -m app.fetch_data
"""

from .auth import get_spotify_client
from .models import init_db, Session, User, TopTrack, TopArtist, RecentlyPlayed, StatsSnapshot
from datetime import datetime


def main():
    init_db()
    sp = get_spotify_client()
    session = Session()
    
    # Fetch user profile from Spotify
    me = sp.current_user()

    # Check if user exist in database
    user = session.query(User).filter_by(spotify_id=me['id']).first()

    # If user doesn't exist, create one
    if not user:
        user = User(spotify_id=me['id'], display_name=me.get('display_name'))
        session.add(user)
        session.commit()
    
    # Clear old data for this user before inserting new data
    # session.query(TopTrack).filter_by(user_id=user.id).delete()
    # session.query(TopArtist).filter_by(user_id=user.id).delete()
    # session.query(RecentlyPlayed).filter_by(user_id=user.id).delete()
    # session.commit()
    
    # Insert new stats with snapshot_id every time data is fetched
    snapshot = StatsSnapshot(user_id=user.id, created_at=datetime.utcnow(), snapshot_type="auto")
    session.add(snapshot)
    session.commit()
        
    for time_range in ['short_term', 'medium_term', 'long_term']:
        results = sp.current_user_top_tracks(limit=50, time_range=time_range)
        
        for rank, item in enumerate(results['items'], 1):
            track = TopTrack(
                user_id=user.id,
                snapshot_id=snapshot.id,
                track_id=item['id'],
                track_name=item['name'],
                artist_name=item['artists'][0]['name'],
                time_range=time_range,
                rank=rank,
                fetched_at=datetime.utcnow(),
                image_url=item['album']['images'][0]['url'] if item['album']['images'] else None
            )
            session.add(track)
            
    for time_range in ['short_term', 'medium_term', 'long_term']:
        results = sp.current_user_top_artists(limit=50, time_range=time_range)
        
        for rank, item in enumerate(results['items'], 1):
            artist = TopArtist(
                user_id=user.id,
                snapshot_id=snapshot.id,
                artist_id=item['id'],
                artist_name=item['name'],
                genres=", ".join(item.get('genres', [])),
                time_range=time_range,
                rank=rank,
                fetched_at=datetime.utcnow(),
                image_url=item['images'][0]['url'] if item['images'] else None
            )
            session.add(artist)
            
    results = sp.current_user_recently_played(limit=50)

    for item in results['items']:
        recent = RecentlyPlayed(
            user_id=user.id,
            snapshot_id=snapshot.id,
            track_id=item['track']['id'],
            track_name=item['track']['name'],
            artist_name=item['track']['artists'][0]['name'],
            played_at=datetime.fromisoformat(item['played_at'].replace('Z', '+00:00')),
            fetched_at=datetime.utcnow(),
        )
        session.add(recent)
        
    session.commit()
    print("✓ Stats saved to database!")


if __name__ == "__main__":
    main()
