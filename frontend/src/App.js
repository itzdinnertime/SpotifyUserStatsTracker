import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './components/HomePage';
import StatsPage from './components/StatsPage';
import { TimezoneProvider } from './components/TimezoneContext';

function App() {
  return (
    <TimezoneProvider>
      <Router>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/stats" element={<StatsPage />} />
        </Routes>
      </Router>
    </TimezoneProvider>
  );
}

export default App;