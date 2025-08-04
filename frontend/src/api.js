import axios from 'axios';

const BASE_URL = 'http://localhost:8060';

export const fetchFlowers = async () => {
  const response = await axios.get(`${BASE_URL}/flowers/`);
  return response.data;
};

export const getFlowerById = async (id) => {
  const response = await axios.get(`${BASE_URL}/flowers/${id}`);
  return response.data;
};

export const updateFlower = async (id, flowerData) => {
  const response = await axios.put(`${BASE_URL}/flowers/${id}`, flowerData);
  return response.data;
};

export const createFlower = async (flowerData) => {
  const response = await axios.post(`${BASE_URL}/flowers/`, flowerData);
  return response.data;
};

export const deleteFlower = async (id) => {
  const response = await axios.delete(`${BASE_URL}/flowers/${id}`);
  return response.data;
};

export const detectFlower = async (imageFile) => {
  const formData = new FormData();
  formData.append('img', imageFile);

  const response = await axios.post(`${BASE_URL}/flowers/upload/image`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};