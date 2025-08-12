import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import RedditLogo from './reddit-logo-23F13F6A6A-seeklogo.com.png';

function EditPost() {
    const { postId } = useParams();
    const navigate = useNavigate();
    const [postData, setPostData] = useState({
        title: '',
        body: '',
        subreddit: '',
        timestamp: ''
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    useEffect(() => {
        setLoading(true);
        axios.get(`/api/posts/${postId}`)
            .then(response => {
                setPostData(response.data);
                setLoading(false);
            })
            .catch(error => {
                setError('Failed to fetch post data.');
                setLoading(false);
            });
    }, [postId]);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setPostData(prev => ({ ...prev, [name]: value }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        axios.put(`/api/posts/${postId}`, postData)
            .then(response => {
                alert('Post updated successfully');
                navigate('/');
            })
            .catch(error => {
                setError('Failed to update the post.');
            });
    };

    if (loading) return <p>Loading...</p>;
    if (error) return <p>{error}</p>;

    return (
        <div style={{ padding: '20px', backgroundColor: '#FF4500', minHeight: '100vh', fontFamily: 'Quicksand, sans-serif' }}>
            <img src={RedditLogo} alt="Reddit Logo" width="100" height="100" />
            <h1 style={{ fontSize: '32px', color: 'white', marginBottom: '30px' }}>Edit Post</h1>
            <form onSubmit={handleSubmit} style={{ backgroundColor: 'white', padding: '20px', borderRadius: '10px', boxShadow: '0px 0px 10px 0px rgba(0,0,0,0.2)' }}>
                <div style={{ marginBottom: '20px' }}>
                    <label htmlFor="title" style={{ fontSize: '18px', color: '#333' }}>Title:</label><br />
                    <input type="text" id="title" name="title" value={postData.title} onChange={handleInputChange} style={{ width: '100%', padding: '10px', borderRadius: '5px', border: '1px solid #8c8c8c' }} />
                </div>
                <div style={{ marginBottom: '20px' }}>
                    <label htmlFor="body" style={{ fontSize: '18px', color: '#333' }}>Body:</label><br />
                    <textarea id="body" name="body" value={postData.body} onChange={handleInputChange} style={{ width: '100%', padding: '10px', borderRadius: '5px', border: '1px solid #8c8c8c', minHeight: '200px' }} />
                </div>
                <div style={{ marginBottom: '20px' }}>
                    <label htmlFor="subreddit" style={{ fontSize: '18px', color: '#333' }}>Subreddit Name:</label><br />
                    <input type="text" id="subreddit" name="subreddit" value={postData.subreddit} onChange={handleInputChange} style={{ width: '100%', padding: '10px', borderRadius: '5px', border: '1px solid #8c8c8c' }} />
                </div>
                <div style={{ marginBottom: '20px' }}>
                    <label htmlFor="timestamp" style={{ fontSize: '18px', color: '#333' }}>Date:</label><br />
                    <input type="date" id="timestamp" name="timestamp" value={postData.timestamp} onChange={handleInputChange} style={{ padding: '10px', borderRadius: '5px', border: '1px solid #8c8c8c' }} />
                </div>
                <button type="submit" style={{ backgroundColor: '#0079D3', color: 'white', padding: '10px 20px', borderRadius: '5px', border: 'none', cursor: 'pointer' }}>Update Post</button>
            </form>
        </div>
    );
}

export default EditPost;