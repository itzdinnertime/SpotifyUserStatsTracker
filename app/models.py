"""
Data models for Spotify stats.
Provides clean data structures for tracks, artists, and stats.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Track:
    """Represents a Spotify track."""
    id: str
    name: str
    artists: list[str]
    album: str
    duration_ms: int
    popularity: int
    preview_url: str | None = None

    @classmethod
    def from_spotify_data(cls, data: dict) -> "Track":
        """Create Track from Spotify API response."""
        return cls(
            id=data["id"],
            name=data["name"],
            artists=[artist["name"] for artist in data["artists"]],
            album=data["album"]["name"],
            duration_ms=data["duration_ms"],
            popularity=data.get("popularity", 0),
            preview_url=data.get("preview_url"),
        )

    @property
    def duration_str(self) -> str:
        """Return duration as mm:ss string."""
        minutes = self.duration_ms // 60000
        seconds = (self.duration_ms % 60000) // 1000
        return f"{minutes}:{seconds:02d}"

    @property
    def artists_str(self) -> str:
        """Return artists as comma-separated string."""
        return ", ".join(self.artists)


@dataclass
class Artist:
    """Represents a Spotify artist."""
    id: str
    name: str
    genres: list[str]
    popularity: int
    followers: int
    image_url: str | None = None

    @classmethod
    def from_spotify_data(cls, data: dict) -> "Artist":
        """Create Artist from Spotify API response."""
        images = data.get("images", [])
        return cls(
            id=data["id"],
            name=data["name"],
            genres=data.get("genres", []),
            popularity=data.get("popularity", 0),
            followers=data.get("followers", {}).get("total", 0),
            image_url=images[0]["url"] if images else None,
        )

    @property
    def genres_str(self) -> str:
        """Return genres as comma-separated string."""
        return ", ".join(self.genres) if self.genres else "N/A"


@dataclass
class PlayHistory:
    """Represents a recently played track entry."""
    track: Track
    played_at: datetime

    @classmethod
    def from_spotify_data(cls, data: dict) -> "PlayHistory":
        """Create PlayHistory from Spotify API response."""
        return cls(
            track=Track.from_spotify_data(data["track"]),
            played_at=datetime.fromisoformat(data["played_at"].replace("Z", "+00:00")),
        )


@dataclass
class AudioFeatures:
    """Audio features for a track (tempo, energy, etc.)."""
    track_id: str
    danceability: float  # 0.0 to 1.0
    energy: float        # 0.0 to 1.0
    tempo: float         # BPM
    valence: float       # 0.0 (sad) to 1.0 (happy)
    acousticness: float  # 0.0 to 1.0
    instrumentalness: float  # 0.0 to 1.0

    @classmethod
    def from_spotify_data(cls, data: dict) -> "AudioFeatures":
        """Create AudioFeatures from Spotify API response."""
        return cls(
            track_id=data["id"],
            danceability=data["danceability"],
            energy=data["energy"],
            tempo=data["tempo"],
            valence=data["valence"],
            acousticness=data["acousticness"],
            instrumentalness=data["instrumentalness"],
        )
