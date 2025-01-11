
const apiServerPort = '8080';

const getLocation = () => {
  const isDeployedFromApiServer = (window.location.port === apiServerPort);
  return ((isDeployedFromApiServer) ? '' : `http://localhost:${apiServerPort}`);
}

export const getApiPath = (endpoint) => {
  return (getLocation() ? `${getLocation()}/api/${endpoint}` : `api/${endpoint}`);
};