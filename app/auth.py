import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Load variables from .env file
load_dotenv()

# Access environment variables
CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI", "http://localhost:8000/callback")

# Define scopes (permissions) your app needs
SCOPES = [
    "user-read-private",
    "user-read-email",
    "user-top-read",
    "user-read-recently-played",
    "playlist-read-private",
    "playlist-read-collaborative",
    "user-library-read",
    "user-read-playback-state"
]


# Convert scopes list to space-separated string (required by Spotipy)
SCOPE_STRING = " ".join(SCOPES)

def create_spotify_oauth(cache_path: str = ".cache") -> SpotifyOAuth:
    """
    Create and return a SpotifyOAuth object.
    
    Args:
        cache_path: Path to cache file for storing tokens (default: ".cache")
    
    Returns:
        SpotifyOAuth object configured with your credentials
    """
    return SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE_STRING,
        cache_path=cache_path,
        show_dialog=True  # Set to False after testing to skip re-auth prompt
    )


def get_auth_url(cache_path: str = ".cache") -> str:
    """
    Get the Spotify authorization URL for user login.
    
    Redirect users to this URL to authorize your app.
    
    Returns:
        Authorization URL string
    """
    sp_oauth = create_spotify_oauth(cache_path)
    auth_url = sp_oauth.get_authorize_url()
    return auth_url


def get_access_token(code: str, cache_path: str = ".cache") -> dict:
    """
    Exchange the authorization code for an access token.
    
    Called after user is redirected back from Spotify with a 'code' parameter.
    
    Args:
        code: The authorization code from Spotify callback
        cache_path: Path to cache file for storing tokens
    
    Returns:
        Token info dictionary containing access_token, refresh_token, expires_at, etc.
    """
    sp_oauth = create_spotify_oauth(cache_path)
    token_info = sp_oauth.get_access_token(code, as_dict=True)
    return token_info


def create_spotify_client(token_info: dict = None, cache_path: str = ".cache") -> spotipy.Spotify:
    """
    Create an authenticated Spotipy client.
    
    Args:
        token_info: Optional token info dict. If None, uses cached token.
        cache_path: Path to cache file for tokens
    
    Returns:
        Authenticated Spotipy client ready to make API calls
    """
    sp_oauth = create_spotify_oauth(cache_path)
    
    if token_info is None:
        # Try to get cached token
        token_info = sp_oauth.get_cached_token()
    
    if token_info is None:
        raise Exception("No token available. User must authenticate first.")
    
    # Check if token needs refresh
    if sp_oauth.is_token_expired(token_info):
        token_info = sp_oauth.refresh_access_token(token_info["refresh_token"])
    
    # Create and return the Spotify client
    return spotipy.Spotify(auth=token_info["access_token"])


def refresh_token(token_info: dict, cache_path: str = ".cache") -> dict:
    """
    Refresh an expired access token.
    
    Args:
        token_info: Current token info dict containing refresh_token
        cache_path: Path to cache file
    
    Returns:
        New token info dictionary with fresh access_token
    """
    sp_oauth = create_spotify_oauth(cache_path)
    
    if "refresh_token" not in token_info:
        raise Exception("No refresh token available. User must re-authenticate.")
    
    new_token_info = sp_oauth.refresh_access_token(token_info["refresh_token"])
    return new_token_info


def is_token_expired(token_info: dict) -> bool:
    """
    Check if the access token is expired.
    
    Args:
        token_info: Token info dictionary
    
    Returns:
        True if expired, False otherwise
    """
    sp_oauth = create_spotify_oauth()
    return sp_oauth.is_token_expired(token_info)


def get_valid_client(token_info: dict = None, cache_path: str = ".cache") -> tuple[spotipy.Spotify, dict]:
    """
    Get a Spotify client with a valid (refreshed if needed) token.
    
    Convenience function that handles token refresh automatically.
    
    Args:
        token_info: Current token info (optional, uses cache if None)
        cache_path: Path to cache file
    
    Returns:
        Tuple of (Spotify client, updated token_info)
    """
    sp_oauth = create_spotify_oauth(cache_path)
    
    if token_info is None:
        token_info = sp_oauth.get_cached_token()
    
    if token_info is None:
        raise Exception("No token available. User must authenticate first.")
    
    # Refresh if expired
    if sp_oauth.is_token_expired(token_info):
        token_info = sp_oauth.refresh_access_token(token_info["refresh_token"])
    
    client = spotipy.Spotify(auth=token_info["access_token"])
    return client, token_info
    
