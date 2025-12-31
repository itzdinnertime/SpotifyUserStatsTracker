import { useState, useEffect } from 'react';

function TopTracks({ snapshotId }) {
  const [tracks, setTracks] = useState([]);
  const [timeRange, setTimeRange] = useState('short_term');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    let url = `http://localhost:8000/api/stats/top-tracks?time_range=${timeRange}`;
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
  }, [timeRange, snapshotId]);

  const timeRangeLabels = {
    short_term: 'Last 4 Weeks',
    medium_term: 'Last 6 Months',
    long_term: 'All Time'
  };

  return (
    <div className="stats-section">
      <h2>🎵 Top Tracks</h2>
      <div className="time-range-buttons">
        {Object.entries(timeRangeLabels).map(([key, label]) => (
          <button
            key={key}
            className={timeRange === key ? 'active' : ''}
            onClick={() => setTimeRange(key)}
          >
            {label}
          </button>
        ))}
      </div>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <ol className="tracks-list">
          {tracks.map((track, index) => (
            <li key={index}>
              <span className="rank">#{track.rank}</span>
              <div className="track-info">
                <span className="track-name">{track.track_name}</span>
                <span className="artist-name">{track.artist_name}</span>
              </div>
              <img className="album-art" src={track.image_url} alt={track.track_name} />
            </li>
          ))}
        </ol>
      )}
    </div>
  );
}

export default TopTracks;