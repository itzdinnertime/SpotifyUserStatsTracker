import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../App.css';

function HomePage() {
  const navigate = useNavigate();
  return (
    <div className="home-page">
      <h1>Welcome to Spotify Stats!</h1>
      <p>See your top tracks, artists, and more.</p>
      <button
        className="go-to-stats-btn"
        onClick={() => navigate('/stats')}
      >
        Go to Stats
      </button>
    </div>
  );
}

export default HomePage;
