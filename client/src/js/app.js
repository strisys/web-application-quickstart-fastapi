import axios from 'axios';

const getMessage = async () => {
  try {
    const response = await axios.get('/api/hello');
    setMessage(JSON.stringify(response.data));
  } catch (error) {
    console.error('Error fetching message:', error);
    setMessage('Error loading message');
  }
};

const setMessage = (message) => {
  document.getElementById('message').innerHTML = message;
};

// Call getMessage when the page loads
getMessage();