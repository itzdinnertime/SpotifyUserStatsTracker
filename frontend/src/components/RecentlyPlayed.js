import { useState, useEffect } from 'react';

function RecentlyPlayed() {
  const [tracks, setTracks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:8000/api/stats/recently-played')
      .then(res => res.json())
      .then(data => {
        setTracks(data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error fetching recently played:', err);
        setLoading(false);
      });
  }, []);

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="stats-section">
      <h2>🕐 Recently Played</h2>

      {loading ? (
        <p>Loading...</p>
      ) : (
        <ul className="recent-list">
          {tracks.map((track, index) => (
            <li key={index}>
              <div className="track-info">
                <span className="track-name">{track.track_name}</span>
                <span className="artist-name">{track.artist_name}</span>
              </div>
              <span className="played-at">{formatDate(track.played_at)}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default RecentlyPlayed;
