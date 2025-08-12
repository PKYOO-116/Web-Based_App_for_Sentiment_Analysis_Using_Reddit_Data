import React from 'react';
import { useNavigate } from 'react-router-dom';
import RedditPosts from './RedditPosts';
import RedditLogo from './reddit-logo-23F13F6A6A-seeklogo.com.png';

function AdminPage() {
    const navigate = useNavigate();

    const handleBackToHome = () => {
        navigate('/');
    };

    const handleInsert = () => {
        navigate('/insert'); // Navigate to the insert page when the button is clicked
    };

    const handleDeletePost = (id) => {
        fetch(`/api/posts/${id}`, { method: 'DELETE' })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to delete the post.');
                }
                // Refresh posts or filter locally
                window.location.reload(false); // Or better yet, refetch the posts or adjust the local state
            })
            .catch(error => alert(error.message));
    };

    const adminColumns = [
        {
            Header: 'Delete',
            id: 'delete',
            accessor: (str) => 'delete',
            Cell: (tableProps) => (
                <button onClick={() => handleDeletePost(tableProps.row.original.id)} style={{ backgroundColor: 'red', color: 'white' }}>Delete</button>
            )
        },
        {
            Header: 'Action',
            accessor: 'action',
            Cell: () => (
                <>
                    <button onClick={() => navigate('/edit')} style={{ marginRight: '10px' }}>Edit</button>
                    <button onClick={handleInsert}>Insert</button>
                </>
            ),
            disableFilters: true
        }
    ];

    return (
        <div style={{ padding: '20px', backgroundColor: '#FF4500', minHeight: '100vh', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', fontFamily: 'Quicksand, sans-serif' }}>
          <img src={RedditLogo} alt="Reddit Logo" width="50" height="50" />
          <h1 style={{ fontSize: '32px', color: 'white', marginBottom: '30px' }}>Admin View</h1>
          <div style={{ display: 'flex', gap: '10px', marginBottom: '30px' }}>
            <button onClick={handleBackToHome} style={{ backgroundColor: '#0079D3', color: 'white', padding: '10px', borderRadius: '5px', border: 'none', cursor: 'pointer' }}>Home Page</button>
            <button onClick={handleInsert} style={{ backgroundColor: '#0079D3', color: 'white', padding: '10px', borderRadius: '5px', border: 'none', cursor: 'pointer' }}>Insert Post</button>
          </div>
          <div style={{ backgroundColor: 'white', padding: '20px', borderRadius: '10px', boxShadow: '0px 0px 10px 0px rgba(0,0,0,0.2)' }}>
            <RedditPosts showActions={true} />
          </div>
        </div>
      );
}

export default AdminPage;