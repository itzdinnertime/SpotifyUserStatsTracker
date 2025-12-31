import { useState, useEffect } from 'react';
import './UserProfile.css';

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

  if (loading) return null;
  if (!user) return null;

  return (
    <div className="user-greeting">
      {user.profile_image_url && (
        <img
          src={user.profile_image_url}
          alt={user.display_name}
          className="user-greeting-img"
        />
      )}
      <span className="user-greeting-text">
        👋 Hello, <strong>{user.display_name}</strong>
      </span>
    </div>
  );
}

export default UserProfile;