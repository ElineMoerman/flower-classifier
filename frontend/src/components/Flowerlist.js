import React, { useEffect, useState } from 'react';
import { fetchFlowers } from '../api';
import { Link, useLocation } from 'react-router-dom';
import { FaPencilAlt } from 'react-icons/fa';
import '../App.css';

function FlowerList() {
  const [flowers, setFlowers] = useState([]);
  const location = useLocation();

  const loadFlowers = async () => {
    try {
      const data = await fetchFlowers();
      setFlowers(data);
    } catch (err) {
      console.error('Error loading flowers:', err);
    }
  };

  useEffect(() => {
    loadFlowers();
  }, [location.state]);

  return (
    <div className="container mt-5">
      <div className="d-flex justify-content-between mb-3">
        <h2>List of current flowers</h2>
        <Link to="/create" className="btn btn-pink">
          + Add New Flower
        </Link>
      </div>
      <table className="table table-bordered table-striped table-hover">
        <thead className="table-dark">
          <tr>
            <th>Name</th>
            <th>Species</th>
            <th>Color</th>
            <th>Description</th>
            <th>Edit</th>
          </tr>
        </thead>
        <tbody>
          {flowers.map((flower) => (
            <tr key={flower.id}>
              <td>{flower.name}</td>
              <td>{flower.species}</td>
              <td>{flower.color}</td>
              <td>{flower.description}</td>
              <td>
                <Link to={`/edit/${flower.id}`} aria-label={`Edit ${flower.name}`}>
                  <FaPencilAlt style={{ cursor: 'pointer', color: '#FFB6C1' }} />
                </Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default FlowerList;
