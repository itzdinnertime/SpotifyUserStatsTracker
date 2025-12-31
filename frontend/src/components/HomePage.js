import React, { useState, useEffect, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import '../App.css';
import { TimezoneContext } from './TimezoneContext';
import UserProfile from './UserProfile'; // <-- Add this import

const timezones = [
  'UTC',
  'America/New_York',
  'Europe/London',
  'Asia/Tokyo',
  'Australia/Sydney'
  // Add more as needed
];

function HomePage() {
  const navigate = useNavigate();
  const { timezone, setTimezone } = useContext(TimezoneContext);
  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  // Format time in selected timezone
  const getTimeString = () => {
    try {
      return currentTime.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        timeZone: timezone
      });
    } catch {
      // fallback if timezone is invalid
      return currentTime.toLocaleTimeString();
    }
  };

  const handleTimezoneChange = (e) => {
    setTimezone(e.target.value);
  };

  return (
    <div className="home-page">
      <UserProfile />
      <h1>Welcome to Spotify Stats!</h1>
      <p>See your top tracks, artists, and more.</p>
      <button
        className="go-to-stats-btn"
        onClick={() => navigate('/stats')}
      >
        Go to Stats
      </button>
      <div className="settings-widget" style={{ marginTop: '2rem' }}>
        <h3>Settings</h3>
        <label htmlFor="timezone-select">Timezone:</label>
        <select
          id="timezone-select"
          value={timezone}
          onChange={handleTimezoneChange}
        >
          {timezones.map(tz => (
            <option key={tz} value={tz}>{tz}</option>
          ))}
        </select>
        <div style={{ marginTop: '1rem', fontSize: '1.2rem' }}>
          <strong>Current Time:</strong> {getTimeString()}
        </div>
      </div>
    </div>
  );
}

export default HomePage;