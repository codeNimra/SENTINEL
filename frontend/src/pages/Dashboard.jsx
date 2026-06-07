import React, { useState } from 'react';
import ReasoningStream from '../components/ReasoningStream';
 
function Dashboard() {
  const [problems, setProblems] = useState([]);
  const [selectedProblem, setSelectedProblem] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
 
  const fetchProblems = async () => {
    setLoading(true);
    try {
      const res = await fetch('http://localhost:5000/api/problems');
      const data = await res.json();
      setProblems(data.problems || []);
    } catch (err) {
      console.error('Error fetching problems:', err);
    }
    setLoading(false);
  };
 
  const analyzeProblem = async (problemId) => {
    setLoading(true);
    try {
      const res = await fetch('http://localhost:5000/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ problemId })
      });
      const data = await res.json();
      setAnalysis(data);
    } catch (err) {
      console.error('Error analyzing problem:', err);
    }
    setLoading(false);
  };
 
  const testDemo = async () => {
    setLoading(true);
    try {
      const res = await fetch('http://localhost:5000/api/demo', { method: 'POST' });
      const data = await res.json();
      setAnalysis(data);
    } catch (err) {
      console.error('Error running demo:', err);
    }
    setLoading(false);
  };
 
  return (
    <div style={styles.container}>
      <header style={styles.header}>
        <h1>SENTINEL</h1>
        <p>AI Site Reliability Engineer</p>
      </header>
 
      <div style={styles.controls}>
        <button onClick={fetchProblems} style={styles.button} disabled={loading}>
          {loading ? 'Loading...' : 'Load Dynatrace Problems'}
        </button>
        <button onClick={testDemo} style={{ ...styles.button, background: '#ff6b35' }} disabled={loading}>
          {loading ? 'Loading...' : 'Test Demo'}
        </button>
      </div>
 
      {problems.length > 0 && (
        <div style={styles.section}>
          <h2>Active Problems</h2>
          <div style={styles.problemList}>
            {problems.map(p => (
              <div
                key={p.id}
                style={styles.problemCard}
                onClick={() => analyzeProblem(p.id)}
              >
                <h3>{p.title}</h3>
                <p>Status: {p.status}</p>
              </div>
            ))}
          </div>
        </div>
      )}
 
      {analysis && (
        <div style={styles.section}>
          <h2>Analysis</h2>
          <ReasoningStream analysis={analysis} />
        </div>
      )}
    </div>
  );
}
 
const styles = {
  container: {
    background: '#05080f',
    color: '#e2e8f0',
    minHeight: '100vh',
    padding: '2rem',
  },
  header: {
    textAlign: 'center',
    marginBottom: '2rem',
  },
  controls: {
    display: 'flex',
    gap: '1rem',
    marginBottom: '2rem',
    justifyContent: 'center',
  },
  button: {
    background: '#00d4b4',
    color: '#05080f',
    border: 'none',
    padding: '10px 20px',
    borderRadius: '4px',
    cursor: 'pointer',
    fontWeight: 'bold',
  },
  section: {
    marginBottom: '2rem',
  },
  problemList: {
    display: 'grid',
    gap: '1rem',
  },
  problemCard: {
    background: '#0d1425',
    border: '1px solid #1e3a5f',
    padding: '1rem',
    borderRadius: '8px',
    cursor: 'pointer',
  },
};
 
export default Dashboard;