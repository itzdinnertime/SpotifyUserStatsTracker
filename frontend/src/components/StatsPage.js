import React from 'react';
import UserProfile from './UserProfile';
import TopTracks from './TopTracks';
import TopArtists from './TopArtists';
import RecentlyPlayed from './RecentlyPlayed';
import { Link } from 'react-router-dom';
import '../App.css';

function StatsPage() {
  return (
    <div className="App">
      <Link to="/" style={{ color: '#1db954', textDecoration: 'underline', marginBottom: '1rem', display: 'inline-block' }}>
        ← Back to Home
      </Link>
      <UserProfile />
      <div className="stats-container">
        <TopTracks />
        <TopArtists />
        <RecentlyPlayed />
      </div>
    </div>
  );
}

export default StatsPage;
