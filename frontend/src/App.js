// src/App.js
import React, { useEffect, useState } from 'react';
import { fetchFlowers } from './api';
import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import FlowerList from './components/Flowerlist.js';
import EditFlower from './components/EditFlower.js';
import CreateFlower from './components/CreateFlower.js';

function App() {
  const [flowers, setFlowers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchFlowers()
      .then(data => {
        setFlowers(data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Fetch error:", err);
        setError('Could not fetch flowers');
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div className="text-center mt-5">Loading...</div>;
  }

  if (error) {
    return <div className="alert alert-danger text-center mt-5">{error}</div>;
  }


  return (
    <Router>
      <div className="App">
        <div className="container mt-5">
          <h1 className="text-center mb-4">🌸 Flower List 🌸</h1>
          <div className="table-container">
            <Routes>
              <Route path="/" element={<FlowerList flowers={flowers} />} />
              <Route path="/edit/:id" element={<EditFlower flowers={flowers} />} />
              <Route path="/create" element={<CreateFlower />} />
            </Routes>
          </div>
        </div>
      </div>
    </Router>
  );
}

export default App;
