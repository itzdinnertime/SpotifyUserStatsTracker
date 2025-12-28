import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_url = os.getenv("SPOTIFY_REDIRECT_URL")

Scopes = [
    "user-top-read",
    "user-read-recently-played",
    "user-read-private"
]

def get_spotify_client():
    
    auth_manager = SpotifyOAuth(
        client_id = client_id,
        client_secret = client_secret,
        redirect_uri = redirect_url,
        scope = " ".join(Scopes),
        cache_path = ".cache"
    )
    
    return spotipy.Spotify(auth_manager = auth_manager)


