import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getFlowerById, updateFlower } from '../api';
import '../App.css';

function EditFlower() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [flower, setFlower] = useState({
    name: '',
    species: '',
    color: '',
    description: '',
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [validationError, setValidationError] = useState('');

  useEffect(() => {
    const loadFlower = async () => {
      try {
        const data = await getFlowerById(id);
        setFlower(data);
        setLoading(false);
      } catch (err) {
        console.error(err);
        setError('Failed to fetch flower');
        setLoading(false);
      }
    };

    loadFlower();
  }, [id]);

  const handleChange = (e) => {
    setFlower({ ...flower, [e.target.name]: e.target.value });
    setValidationError('');
  };

  const handleBack = () => {
    navigate(-1); // navigates to previous page
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Manual check (in addition to required attr, for clarity)
    if (!flower.name || !flower.species || !flower.color || !flower.description) {
      setValidationError('All fields are required.');
      return;
    }

    try {
      await updateFlower(id, flower);
      navigate('/', { state: { refresh: true } });
    } catch (err) {
      console.error(err);
      setError('Failed to update flower');
    }
  };

  if (loading) return <p className="text-center mt-4">Loading...</p>;
  if (error) return <p className="text-danger text-center mt-4">{error}</p>;

  return (
    <div className="container mt-5">
        <div className="header-row d-flex align-items-center mb-3">
            <button className="btn btn-secondary back-button" onClick={handleBack}>
            ← Back
            </button>
            <h2 className="flex-grow-1 text-center mb-0">Edit flower</h2>
            <div style={{ width: '75px' }}>{/* spacer to balance button width */}</div>
        </div>
      <form onSubmit={handleSubmit} className="mt-4">
        {validationError && (
          <div className="alert alert-danger" role="alert">
            {validationError}
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
        <button type="submit" className="btn btn-pink">Update Flower</button>
      </form>
    </div>
  );
}

export default EditFlower;
