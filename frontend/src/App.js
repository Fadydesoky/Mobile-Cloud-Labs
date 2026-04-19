import { useState } from "react";
import axios from "axios";

const API = "http://localhost:5000";

function App() {
  const [homeData, setHomeData] = useState(null);
  const [data, setData] = useState(null);
  const [health, setHealth] = useState(null);
  const [size, setSize] = useState(100);

  const fetchHome = async () => {
    const res = await axios.get(`${API}/`);
    setHomeData(res.data);
  };

  const fetchData = async () => {
    const res = await axios.get(`${API}/data?size=${size}`);
    setData(res.data);
  };

  const checkHealth = async () => {
    const res = await axios.get(`${API}/health`);
    setHealth(res.data);
  };

  return (
    <div className="container">
      <h1>Mobile Cloud Dashboard</h1>

      <div className="card">
        <h2>Response Time</h2>
        <button onClick={fetchHome}>Fetch</button>
        {homeData && (
          <p>Delay: {homeData.delay}s</p>
        )}
      </div>

      <div className="card">
        <h2>Data Endpoint</h2>
        <input
          type="number"
          value={size}
          onChange={(e) => setSize(e.target.value)}
        />
        <button onClick={fetchData}>Get Data</button>
        {data && (
          <p>Count: {data.count}</p>
        )}
      </div>

      <div className="card">
        <h2>Health Check</h2>
        <button onClick={checkHealth}>Check</button>
        {health && <p>Status: {health}</p>}
      </div>
    </div>
  );
}

export default App;
