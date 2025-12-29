import './App.css';
import { BrowserRouter as Router, Routes, Route, Link, useNavigate } from 'react-router-dom';
import UserProfile from './components/UserProfile';
import TopTracks from './components/TopTracks';
import TopArtists from './components/TopArtists';
import RecentlyPlayed from './components/RecentlyPlayed';

function HomePage() {
  const navigate = useNavigate();
  return (
    <div className="home-page" style={{ textAlign: 'center', marginTop: '5rem' }}>
      <h1>Welcome to Spotify Stats!</h1>
      <p>See your top tracks, artists, and more.</p>
      <button
        style={{
          marginTop: '2rem',
          padding: '1rem 2rem',
          fontSize: '1.2rem',
          borderRadius: '8px',
          background: '#1db954',
          color: '#fff',
          border: 'none',
          cursor: 'pointer'
        }}
        onClick={() => navigate('/stats')}
      >
        Go to Stats
      </button>
    </div>
  );
}

function StatsPage() {
  return (
    <div className="App">
      <UserProfile />
      <div className="stats-container">
        <TopTracks />
        <TopArtists />
        <RecentlyPlayed />
      </div>
    </div>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/stats" element={<StatsPage />} />
      </Routes>
    </Router>
  );
}

export default App;