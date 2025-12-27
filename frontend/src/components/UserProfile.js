import { useState, useEffect } from 'react';

function UserProfile() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:8000/api/user/profile')
      .then(res => res.json())
      .then(data => {
        setUser(data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error fetching user:', err);
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Loading profile...</p>;
  if (!user) return <p>No user found</p>;

  return (
    <div className="user-profile">
      <h1>👋 Welcome, {user.display_name}!</h1>
      <p className="spotify-id">Spotify ID: {user.spotify_id}</p>
    </div>
  );
}

export default UserProfile;
