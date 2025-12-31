import React, { useState } from 'react';
import TopTracks from './TopTracks';
import TopArtists from './TopArtists';
import RecentlyPlayed from './RecentlyPlayed';
import SnapshotSelector from './SnapshotSelector';
import { Link } from 'react-router-dom';
import '../App.css';

function StatsPage() {
  const [snapshotId, setSnapshotId] = useState(null);

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