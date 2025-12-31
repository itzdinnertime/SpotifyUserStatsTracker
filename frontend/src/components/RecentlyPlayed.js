import { useState, useEffect } from 'react';

function RecentlyPlayed({ snapshotId, timezone = 'UTC' }) {
  const [tracks, setTracks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let url = `http://localhost:8000/api/stats/recently-played?timezone=${timezone}`;
    if (snapshotId) url += `&snapshot_id=${snapshotId}`;
    fetch(url)
      .then(res => res.json())
      .then(data => {
        setTracks(data);
        setLoading(false);
      })
      .catch(err => {
        setLoading(false);
      });
  }, [timezone, snapshotId]);

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
      <div className="time-range-buttons" style={{ visibility: 'hidden', marginBottom: '1rem' }}>
        {/* Placeholder for alignment */}
        <button>Last 4 Weeks</button>
        <button>Last 6 Months</button>
        <button>All Time</button>
      </div>
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