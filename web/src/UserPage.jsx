import React from 'react';
import RedditPosts from './RedditPosts';
import { useNavigate, Link } from 'react-router-dom';
import RedditLogo from './reddit-logo-23F13F6A6A-seeklogo.com.png';

function UserPage() {
  const navigate = useNavigate();

  const handleBackToHome = () => {
    navigate('/');
  };

  const handleInsert = () => {
    navigate('/insert');  // Navigate to insert page or handle insert action
  };

  return (
    <div style={{ padding: '20px', backgroundColor: '#FF4500', minHeight: '100vh', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', fontFamily: 'Quicksand, sans-serif' }}>
      <img src={RedditLogo} alt="Reddit Logo" width="50" height="50" />
      <h1 style={{ fontSize: '32px', color: 'white', marginBottom: '30px' }}>User View</h1>
      <div style={{ display: 'flex', gap: '10px', marginBottom: '30px' }}>
        <button onClick={handleBackToHome} style={{ backgroundColor: '#0079D3', color: 'white', padding: '10px', borderRadius: '5px', border: 'none', cursor: 'pointer' }}>Home Page</button>
        <button onClick={handleInsert} style={{ backgroundColor: '#0079D3', color: 'white', padding: '10px', borderRadius: '5px', border: 'none', cursor: 'pointer' }}>Insert Post</button>
      </div>
      <div style={{ backgroundColor: 'white', padding: '20px', borderRadius: '10px', boxShadow: '0px 0px 10px 0px rgba(0,0,0,0.2)' }}>
        <RedditPosts showActions={false} />
      </div>
    </div>
  );
}

export default UserPage;