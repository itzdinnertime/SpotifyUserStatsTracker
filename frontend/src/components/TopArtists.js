import { useState, useEffect } from 'react';

function TopArtists() {
  const [artists, setArtists] = useState([]);
  const [timeRange, setTimeRange] = useState('short_term');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    fetch(`http://localhost:8000/api/stats/top-artists?time_range=${timeRange}`)
      .then(res => res.json())
      .then(data => {
        setArtists(data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error fetching artists:', err);
        setLoading(false);
      });
  }, [timeRange]);

  const timeRangeLabels = {
    short_term: 'Last 4 Weeks',
    medium_term: 'Last 6 Months',
    long_term: 'All Time'
  };

  return (
    <div className="stats-section">
      <h2>🎤 Top Artists</h2>
      
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
        <ol className="artists-list">
          {artists.map((artist, index) => (
            <li key={index}>
              <span className="rank">#{artist.rank}</span>
              <div className="artist-info">
                <span className="artist-name">{artist.artist_name}</span>
                <span className="genres">{artist.genres}</span>
              </div>
            </li>
          ))}
        </ol>
      )}
    </div>
  );
}

export default TopArtists;
