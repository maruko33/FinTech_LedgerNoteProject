import {useEffect, useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [health, setHealth] = useState("loading...");
  useEffect(() => {
    fetch("http://localhost:8000/health")
      .then((r) => r.json())
      .then((d) => setHealth(d.status))
      .catch(() => setHealth("error"));
  }, []);
  return <div style={{ padding: 24 }}>Backend health: {health}</div>;
}
export default App;