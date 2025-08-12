import React from 'react';
import { useNavigate } from 'react-router-dom';
import RedditLogo from './reddit-logo-23F13F6A6A-seeklogo.com.png';
import PredictionBar from './PredictionBar';

function HomePage() {
    const navigate = useNavigate();

    const handleUserClick = () => {
        navigate('/user');
    };

    const handleAdminClick = () => {
        navigate('/admin');
    };

    const demoPredictionPercentage = 49.62; // 49.62% for Democrats

    return (
        <>
            <div>
                <link rel="preconnect" href="https://fonts.googleapis.com" />
                <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
                <link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@300..700&display=swap" rel="stylesheet" />
            </div>
            <div style={{ position: 'absolute', top: '10px', left: '10px', zIndex: '1' }}>
                <img src={RedditLogo} alt="Reddit Logo" width="100" height="100" />
            </div>
            <div style={{ position: 'absolute', top: '10px', right: '10px', zIndex: '1' }}>
                <img src={RedditLogo} alt="Reddit Logo" width="100" height="100" />
            </div>
            <div style={{ position: 'absolute', bottom: '10px', left: '10px', zIndex: '1' }}>
                <img src={RedditLogo} alt="Reddit Logo" width="100" height="100" />
            </div>
            <div style={{ position: 'absolute', bottom: '10px', right: '10px', zIndex: '1' }}>
                <img src={RedditLogo} alt="Reddit Logo" width="100" height="100" />
            </div>
            <div style={{ backgroundColor: '#FF4500', minHeight: '100vh', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', fontFamily: 'Quicksand, sans-serif', padding: '20px', border: '2px solid #8c8c8c', borderRadius: '10px', boxShadow: '0px 0px 10px 0px rgba(0,0,0,0.2)' }}>
                <div style={{ backgroundColor: '#292929', padding: '20px', borderRadius: '10px', marginBottom: '30px', textAlign: 'center' }}>
                    <h1 style={{ fontSize: '32px', color: 'white', marginBottom: '10px' }}>Welcome to Our Reddit Firebase/Database!</h1>
                    <PredictionBar percentage={demoPredictionPercentage} />
                </div>
                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                    <h2 style={{ fontSize: '24px', color: 'white', marginBottom: '20px' }}>Are you a user or an admin?</h2>
                    <div style={{ display: 'flex', justifyContent: 'center' }}>
                        <button onClick={handleUserClick} style={{ margin: '0 10px', padding: '10px 20px', fontSize: '18px', backgroundColor: '#0079D3', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' }}>User</button>
                        <button onClick={handleAdminClick} style={{ margin: '0 10px', padding: '10px 20px', fontSize: '18px', backgroundColor: '#0079D3', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' }}>Admin</button>
                    </div>
                </div>
                <div style={{ marginTop: '50px', padding: '20px', backgroundColor: 'white', borderRadius: '10px', boxShadow: '0px 0px 10px 0px rgba(0,0,0,0.2)' }}>
                    <p style={{ fontSize: '16px', color: '#333', textAlign: 'center', marginBottom: '10px' }}>Please use the above buttons to enter and interact with our real-time database of Reddit posts!</p>
                    <p style={{ fontSize: '16px', color: '#333', textAlign: 'center', marginBottom: '10px' }}>Happy Redditing</p>
                </div>
            </div>
        </>
    );
}

export default HomePage;
