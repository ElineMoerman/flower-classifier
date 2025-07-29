import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createFlower } from '../api';
import '../App.css';

function CreateFlower() {
  const navigate = useNavigate();
  const [flower, setFlower] = useState({
    name: '',
    species: '',
    color: '',
    description: '',
  });
  const [error, setError] = useState(null);
  const [validationError, setValidationError] = useState('');

  const handleChange = (e) => {
    setFlower({ ...flower, [e.target.name]: e.target.value });
    setValidationError('');
  };

  const handleBack = () => {
    navigate(-1); // navigates to previous page
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!flower.name || !flower.species || !flower.color || !flower.description) {
      setValidationError('All fields are required.');
      return;
    }

    try {
      await createFlower(flower);
      navigate('/', { state: { refresh: true } });
    } catch (err) {
      console.error(err);
      setError('Failed to create flower.');
    }
  };

  return (
    <div className="container mt-5">
        <div className="header-row d-flex align-items-center mb-3">
            <button className="btn btn-secondary back-button" onClick={handleBack}>
            ← Back
            </button>
            <h2 className="flex-grow-1 text-center mb-0">🌼 Create a New Flower</h2>
            <div style={{ width: '75px' }}>{/* spacer to balance button width */}</div>
        </div>
      <form onSubmit={handleSubmit} className="mt-4">
        {validationError && (
          <div className="alert alert-danger" role="alert">
            {validationError}
          </div>
        )}
        {error && (
          <div className="alert alert-danger" role="alert">
            {error}
          </div>
        )}
        <div className="mb-3">
          <label className="form-label">Name</label>
          <input
            type="text"
            name="name"
            value={flower.name}
            onChange={handleChange}
            className="form-control"
            required
          />
        </div>
        <div className="mb-3">
          <label className="form-label">Species</label>
          <input
            type="text"
            name="species"
            value={flower.species}
            onChange={handleChange}
            className="form-control"
            required
          />
        </div>
        <div className="mb-3">
          <label className="form-label">Color</label>
          <input
            type="text"
            name="color"
            value={flower.color}
            onChange={handleChange}
            className="form-control"
            required
          />
        </div>
        <div className="mb-3">
          <label className="form-label">Description</label>
          <textarea
            name="description"
            value={flower.description}
            onChange={handleChange}
            className="form-control"
            rows="3"
            required
          />
        </div>
        <button type="submit" className="btn btn-pink">Create Flower</button>
      </form>
    </div>
  );
}

export default CreateFlower;
