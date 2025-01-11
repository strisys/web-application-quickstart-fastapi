import axios from 'axios';
import { getApiPath } from './util';

const getMessage = async () => {
  try {
    const endpoint = `${getApiPath('hello')}`;
    const response = await axios.get(endpoint);
    return JSON.stringify(response.data);
  } catch (error) {
    console.error('Error fetching message:', error);
    return 'Error loading message';
  }
};

const setMessage = (message) => {
  document.getElementById('message').innerHTML = message;
};

const message = (await getMessage());

if (message) {
  setMessage(message);
}