import React from 'react';

function PredictionBar({ percentage }) {
  const blueStyle = {
    width: `${percentage}%`,
    backgroundColor: 'blue',
    height: '50px',
    display: 'flex',
    justifyContent: 'flex-start', // Aligns text to the start of the blue bar
    alignItems: 'center',
    color: 'white',
    fontWeight: 'bold',
    fontSize: '20px',
    paddingLeft: percentage > 10 ? '10px' : '0', // Adds padding if the bar is wide enough
    position: 'relative'
  };

  const redStyle = {
    width: `${100 - percentage}%`,
    backgroundColor: 'red',
    height: '50px',
    display: 'flex',
    justifyContent: 'flex-end', // Aligns text to the end of the red bar
    alignItems: 'center',
    color: 'white',
    fontWeight: 'bold',
    fontSize: '20px',
    paddingRight: (100 - percentage) > 10 ? '10px' : '0', // Adds padding if the bar is wide enough
    position: 'relative'
  };

  return (
    <div style={{ width: '100%' }}>
      <h2 style={{ textAlign: 'center', marginBottom: '10px', color: 'white' }}>Current Sentiment Analysis Prediction</h2>
      <div style={{ display: 'flex' }}>
        <div style={blueStyle}>
          {percentage > 5 ? `Biden ${percentage}%` : ''}
        </div>
        <div style={redStyle}>
          {100 - percentage > 5 ? `Trump ${100 - percentage}%` : ''}
        </div>
      </div>
    </div>
  );
}

export default PredictionBar;