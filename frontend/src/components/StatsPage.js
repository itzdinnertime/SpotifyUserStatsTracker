import React, { useState, useEffect } from 'react';
import TopTracks from './TopTracks';
import TopArtists from './TopArtists';
import RecentlyPlayed from './RecentlyPlayed';
import SnapshotSelector from './SnapshotSelector';
import { Link } from 'react-router-dom';
import '../App.css';

function StatsPage() {
  const [snapshotId, setSnapshotId] = useState(null);

  // Fetch snapshots and set the latest as default
  useEffect(() => {
    fetch('http://localhost:8000/api/stats/snapshots')
      .then(res => res.json())
      .then(data => {
        if (data && data.length > 0) {
          setSnapshotId(data[0].id);
        }
      });
  }, []);

  return (
    <div className="App">
      <Link to="/" style={{ color: '#1db954', textDecoration: 'underline', marginBottom: '1rem', display: 'inline-block' }}>
        ← Back to Home
      </Link>
      <SnapshotSelector snapshotId={snapshotId} setSnapshotId={setSnapshotId} />
      <div className="stats-container">
        <TopTracks snapshotId={snapshotId} />
        <TopArtists snapshotId={snapshotId} />
        <RecentlyPlayed snapshotId={snapshotId} />
      </div>
    </div>
  );
}

export default StatsPage;