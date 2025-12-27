"""
Spotify API client wrapper using Spotipy.
Handles authentication and provides methods to fetch user data.
"""

import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Load environment variables from .env file
load_dotenv()


class SpotifyClient:
    """Wrapper for Spotipy to fetch user listening stats."""

    # Scopes needed to read user's listening history and library
    SCOPES = [
        "user-top-read",           # Top artists and tracks
        "user-read-recently-played",  # Recently played tracks
        "user-library-read",       # Saved tracks/albums
        "playlist-read-private",   # Private playlists
        "user-read-private",       # Account details
    ]

    def __init__(self):
        """Initialize Spotify client with OAuth authentication."""
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=os.getenv("SPOTIPY_CLIENT_ID"),
                client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
                redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI", "http://127.0.0.1:8888/callback"),
                scope=" ".join(self.SCOPES),
            )
        )

    def get_current_user(self) -> dict:
        """Get the current user's profile."""
        return self.sp.current_user()

    def get_top_tracks(self, time_range: str = "medium_term", limit: int = 20) -> list[dict]:
        """
        Get user's top tracks.
        
        Args:
            time_range: 'short_term' (~4 weeks), 'medium_term' (~6 months), 'long_term' (years)
            limit: Number of tracks to return (max 50)
        
        Returns:
            List of track dictionaries
        """
        results = self.sp.current_user_top_tracks(time_range=time_range, limit=limit)
        return results.get("items", [])

    def get_top_artists(self, time_range: str = "medium_term", limit: int = 20) -> list[dict]:
        """
        Get user's top artists.
        
        Args:
            time_range: 'short_term' (~4 weeks), 'medium_term' (~6 months), 'long_term' (years)
            limit: Number of artists to return (max 50)
        
        Returns:
            List of artist dictionaries
        """
        results = self.sp.current_user_top_artists(time_range=time_range, limit=limit)
        return results.get("items", [])

    def get_recently_played(self, limit: int = 50) -> list[dict]:
        """
        Get user's recently played tracks.
        
        Args:
            limit: Number of tracks to return (max 50)
        
        Returns:
            List of play history items (each contains 'track' and 'played_at')
        """
        results = self.sp.current_user_recently_played(limit=limit)
        return results.get("items", [])

    def get_saved_tracks(self, limit: int = 50) -> list[dict]:
        """
        Get user's saved/liked tracks.
        
        Args:
            limit: Number of tracks to return (max 50)
        
        Returns:
            List of saved track items
        """
        results = self.sp.current_user_saved_tracks(limit=limit)
        return results.get("items", [])

    def get_playlists(self, limit: int = 50) -> list[dict]:
        """
        Get user's playlists.
        
        Args:
            limit: Number of playlists to return (max 50)
        
        Returns:
            List of playlist dictionaries
        """
        results = self.sp.current_user_playlists(limit=limit)
        return results.get("items", [])

    def get_audio_features(self, track_ids: list[str]) -> list[dict]:
        """
        Get audio features (tempo, energy, danceability, etc.) for tracks.
        
        Args:
            track_ids: List of Spotify track IDs
        
        Returns:
            List of audio feature dictionaries
        """
        # Spotify API allows max 100 tracks per request
        features = []
        for i in range(0, len(track_ids), 100):
            batch = track_ids[i:i + 100]
            batch_features = self.sp.audio_features(batch)
            features.extend([f for f in batch_features if f])  # Filter None values
        return features
