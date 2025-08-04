import React, { useEffect, useState } from 'react';
import { fetchFlowers, detectFlower } from '../api';
import { Link, useLocation } from 'react-router-dom';
import { FaPencilAlt } from 'react-icons/fa';
import '../App.css';

function FlowerList() {
  const [flowers, setFlowers] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [prediction, setPrediction] = useState(null);

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

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

const handleUpload = async () => {
  if (!selectedFile) {
    alert("Please select an image first");
    return;
  }
  try {
    const result = await detectFlower(selectedFile);
    setPrediction(result);
    console.log("Prediction:", result);
  } catch (error) {
    console.error("Upload failed:", error);
    setPrediction("Failed to get prediction. Please try again.");
  }
};

  return (
    <div className="container mt-5">
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h2>List of current flowers</h2>
        <div className="d-flex gap-2">
          {/* Upload form */}
          <div className="input-group">
            <input
              type="file"
              className="form-control"
              id="fileInput"
              style={{ display: 'none' }}
              onChange={handleFileChange}
            />
            <button
              className="btn btn-outline-secondary"
              onClick={() => document.getElementById('fileInput').click()}
            >
              Choose Image
            </button>
            <button className="btn btn-pink" onClick={handleUpload}>
              Upload & Detect
            </button>
          </div>

          {/* Add new flower */}
          <Link to="/create" className="btn btn-pink">
            + Add New Flower
          </Link>
        </div>
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

      {prediction && (
        <div
          style={{
            marginTop: "1rem",
            padding: "10px",
            backgroundColor: "#ffb6c1",
            borderRadius: "5px",
            color: "#5a1a1a",
            fontWeight: "bold",
          }}
          role="alert"
        >
          {prediction}
        </div>
      )}
      
    </div>
  );
}

export default FlowerList;
