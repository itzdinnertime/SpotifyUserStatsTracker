import './App.css';
import UserProfile from './components/UserProfile';
import TopTracks from './components/TopTracks';
import TopArtists from './components/TopArtists';
import RecentlyPlayed from './components/RecentlyPlayed';

function App() {
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

export default App;
