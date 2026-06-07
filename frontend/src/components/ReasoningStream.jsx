import React from 'react';
 
function ReasoningStream({ analysis }) {
  if (!analysis) return null;
 
  return (
    <div style={styles.container}>
      <div style={styles.label}>SENTINEL Analysis</div>
      
      {analysis.thinking && (
        <div style={styles.thinkingBlock}>
          <div style={styles.blockLabel}>Thinking:</div>
          <pre style={styles.thinkingText}>{analysis.thinking}</pre>
        </div>
      )}
 
      {analysis.analysis && (
        <div style={styles.analysisBlock}>
          <div style={styles.blockLabel}>Analysis:</div>
          <pre style={styles.analysisText}>
            {JSON.stringify(analysis.analysis, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}
 
const styles = {
  container: {
    background: '#0d1425',
    border: '1px solid #1e3a5f',
    borderRadius: '8px',
    padding: '1.5rem',
    fontFamily: '"JetBrains Mono", monospace',
  },
  label: {
    fontSize: '14px',
    fontWeight: '500',
    marginBottom: '1rem',
    color: '#00d4b4',
  },
  thinkingBlock: {
    background: '#111c2e',
    padding: '1rem',
    borderRadius: '6px',
    marginBottom: '1rem',
  },
  blockLabel: {
    color: '#00d4b4',
    marginBottom: '0.5rem',
    fontWeight: 'bold',
  },
  thinkingText: {
    color: '#a0aec0',
    fontSize: '12px',
    lineHeight: '1.6',
    whiteSpace: 'pre-wrap',
    margin: 0,
  },
  analysisBlock: {
    background: '#111c2e',
    padding: '1rem',
    borderRadius: '6px',
  },
  analysisText: {
    color: '#00d9b8',
    fontSize: '11px',
    lineHeight: '1.5',
    margin: 0,
    overflow: 'auto',
    maxHeight: '400px',
  },
};
 
export default ReasoningStream;
