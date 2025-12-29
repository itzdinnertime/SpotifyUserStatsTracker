from .spotify_client import SpotifyClient
from ..repositories import UserRepository, TrackRepository, ArtistRepository, RecentlyPlayedRepository

class SyncService:

    def __init__(self, spotify_client, user_repo, track_repo, artist_repo, recent_repo):       
        self.spotify_client = spotify_client
        self.user_repo = user_repo
        self.track_repo = track_repo
        self.artist_repo = artist_repo
        self.recent_repo = recent_repo
        
    def sync_all(self):
        
        # Get current user from Spotify
        spotify_user = self.spotify_client.get_current_user()
        
        # Get or create user in database
        user = self.user_repo.get_or_create(
            spotify_id=spotify_user['id'],
            display_name=spotify_user['display_name']
        )
        
        # Clear old data for this user
        self.track_repo.delete_by_user_id(user.id)
        self.artist_repo.delete_by_user_id(user.id)
        self.recent_repo.delete_by_user_id(user.id)
        
        # Define the limit
        limit  = 50
        
        # Fetch and save top tracks for each time range
        for time_range in ['short_term', 'medium_term', 'long_term']:
            tracks_data = self.spotify_client.get_top_tracks(time_range, limit)
            self.track_repo.save_top_tracks(user.id, tracks_data, time_range)
        
        # Fetch and save top artists for each time range
        for time_range in ['short_term', 'medium_term', 'long_term']:
            artists_data = self.spotify_client.get_top_artists(time_range)
            self.artist_repo.save_top_artists(user.id, artists_data, time_range)
        
        # Fetch and save recently played songs
        recently_played_data = self.spotify_client.get_recently_played(limit)
        self.recent_repo.save_recently_played(user.id, recently_played_data)
        
        print("✓ Stats saved to database!")