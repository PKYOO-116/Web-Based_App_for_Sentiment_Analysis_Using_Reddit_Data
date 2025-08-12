import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import RedditLogo from './reddit-logo-23F13F6A6A-seeklogo.com.png';

function InsertPage() {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        title: '',
        timestamp: '',  // Changed from date
        subreddit: '',
        body: ''  // Changed from content
    });

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData({
            ...formData,
            [name]: value
        });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        // Make an API call to send formData to the server
        axios.post('/api/posts', formData)  // Use formData directly as it's now correctly named
        .then(response => {
            console.log('Success:', response.data);
            navigate('/admin'); // Navigate after successful submission
        })
        .catch(error => {
            console.error('Error posting data:', error);
        });
    };

    return (
        <div style={{ padding: '20px', backgroundColor: '#FF4500', minHeight: '100vh', fontFamily: 'Quicksand, sans-serif' }}>
            <img src={RedditLogo} alt="Reddit Logo" width="100" height="100" />
            <h1 style={{ fontSize: '32px', color: 'white', marginBottom: '30px' }}>Insert New Post</h1>
            <form onSubmit={handleSubmit} style={{ backgroundColor: 'white', padding: '20px', borderRadius: '10px', boxShadow: '0px 0px 10px 0px rgba(0,0,0,0.2)' }}>
                <div style={{ marginBottom: '20px' }}>
                    <label htmlFor="title" style={{ fontSize: '18px', color: '#333' }}>Title:</label><br />
                    <input type="text" id="title" name="title" value={formData.title} onChange={handleInputChange} style={{ width: '100%', padding: '10px', borderRadius: '5px', border: '1px solid #8c8c8c' }} />
                </div>
                <div style={{ marginBottom: '20px' }}>
                    <label htmlFor="timestamp" style={{ fontSize: '18px', color: '#333' }}>Date:</label><br />
                    <input type="date" id="timestamp" name="timestamp" value={formData.timestamp} onChange={handleInputChange} style={{ padding: '10px', borderRadius: '5px', border: '1px solid #8c8c8c' }} />
                </div>
                <div style={{ marginBottom: '20px' }}>
                    <label htmlFor="subreddit" style={{ fontSize: '18px', color: '#333' }}>Subreddit Name:</label><br />
                    <input type="text" id="subreddit" name="subreddit" value={formData.subreddit} onChange={handleInputChange} style={{ width: '100%', padding: '10px', borderRadius: '5px', border: '1px solid #8c8c8c' }} />
                </div>
                <div style={{ marginBottom: '20px' }}>
                    <label htmlFor="body" style={{ fontSize: '18px', color: '#333' }}>Body:</label><br />
                    <textarea id="body" name="body" value={formData.body} onChange={handleInputChange} style={{ width: '100%', padding: '10px', borderRadius: '5px', border: '1px solid #8c8c8c', minHeight: '200px' }} />
                </div>
                <button type="submit" style={{ backgroundColor: '#0079D3', color: 'white', padding: '10px 20px', borderRadius: '5px', border: 'none', cursor: 'pointer' }}>Submit</button>
            </form>
        </div>
    );
}

export default InsertPage;

