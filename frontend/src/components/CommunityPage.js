// CommunityPage.js

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const CommunityPage = () => {
  console.log('Auth Token:', localStorage.getItem('authToken'));

  const [caption, setCaption] = useState('');
  const [posts, setPosts] = useState([]);
  const [editingPost, setEditingPost] = useState(null);
  const [editCaption, setEditCaption] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  const getCurrentUserId = () => {
    const token = localStorage.getItem('authToken');
    if (token) {
      const payload = JSON.parse(atob(token.split('.')[1]));
      console.log('Decoded Token Payload:', payload);
      return parseInt(payload.sub, 10);
    }
    return null;
  };

  useEffect(() => {
    fetchPosts();
  }, []);

  const fetchPosts = async () => {
    try {
      console.log('Fetching posts...');
      const response = await axios.get('http://127.0.0.1:4444/community-posts');
      console.log('Posts fetched:', response.data);
      setPosts(response.data);
    } catch (error) {
      console.error('Error fetching posts:', error);
    }
  };

  const handlePost = async () => {
    try {
      const token = localStorage.getItem('authToken');
      console.log('Token before request:', token);

      const response = await axios.post(
        'http://127.0.0.1:4444/community-post',
        { caption },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );

      setPosts([response.data, ...posts]);
      setCaption('');
    } catch (error) {
      console.error('Error creating post:', error.response?.data || error.message);

      if (error.response && error.response.status === 401) {
        alert('Session expired. Please log in again.');
        localStorage.removeItem('authToken');
        navigate('/login');
      }
    }
  };

  const handleEdit = async (postId) => {
    if (!editCaption.trim()) {
      setError('Please enter some text for your post.');
      return;
    }
  
    setLoading(true);
    try {
      const token = localStorage.getItem('authToken');
      console.log('Token before edit request:', token);  // Debugging statement
  
      const response = await axios.put(
        `http://127.0.0.1:4444/community-post/${postId}`,
        { caption: editCaption },
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );
      setPosts(posts.map(post => (post.id === postId ? response.data : post)));
      setEditingPost(null);
      setEditCaption('');
      setError('');
    } catch (error) {
      setError('Failed to update post. Please try again.');
      console.error('Error updating post:', error.response?.data || error.message);
    } finally {
      setLoading(false);
    }
  };
  

  const handleDelete = async (postId) => {
    const token = localStorage.getItem('authToken');
    console.log('Attempting to delete post with ID:', postId); // Debugging
    console.log('Token used for deletion:', token); // Debugging
  
    if (!window.confirm('Are you sure you want to delete this post?')) {
      return;
    }
  
    setLoading(true);
    try {
      await axios.delete(
        `http://127.0.0.1:4444/community-post/${postId}`,
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );
  
      setPosts(posts.filter(post => post.id !== postId));
      setError('');
      console.log('Post deleted successfully'); // Debugging
    } catch (error) {
      setError('Failed to delete post. Please try again.');
      console.error('Error deleting post:', error.response?.data || error.message);
    } finally {
      setLoading(false);
    }
  };
  
  
  

  const currentUserId = getCurrentUserId();
  console.log('Current User ID:', currentUserId);

  return (
    <div className="community-page" style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>Community Posts</h1>

      {error && <div style={{ color: 'red', marginBottom: '10px' }}>{error}</div>}

      <div className="post-form" style={{ marginBottom: '20px' }}>
        <textarea
          value={caption}
          onChange={(e) => setCaption(e.target.value)}
          placeholder="What's on your mind?"
          disabled={loading}
          style={{ width: '100%', height: '100px', padding: '10px', marginBottom: '10px' }}
        />
        <button
          onClick={handlePost}
          disabled={loading || !caption.trim()}
          style={{
            backgroundColor: '#083e13',
            color: 'white',
            padding: '10px 20px',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
          }}
        >
          {loading ? 'Posting...' : 'Post'}
        </button>
      </div>

      <div className="posts-list">
        {posts.length > 0 ? (
          posts.map((post) => (
            <div
              key={post.id}
              className="post-card"
              style={{
                border: '1px solid #ccc',
                padding: '15px',
                marginBottom: '15px',
                borderRadius: '8px',
              }}
            >
              {editingPost === post.id ? (
                <div className="edit-form">
                  <textarea
                    value={editCaption}
                    onChange={(e) => setEditCaption(e.target.value)}
                    disabled={loading}
                    style={{ width: '100%', height: '80px', marginBottom: '10px' }}
                  />
                  <div className="edit-buttons">
                    <button
                      onClick={() => handleEdit(post.id)}
                      disabled={loading || !editCaption.trim()}
                      style={{ backgroundColor: '#28a745', color: 'white', padding: '8px 12px', marginRight: '8px' }}
                    >
                      Save
                    </button>
                    <button
                      onClick={() => setEditingPost(null)}
                      disabled={loading}
                      style={{ backgroundColor: '#dc3545', color: 'white', padding: '8px 12px' }}
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              ) : (
                <div>
                  <p className="post-caption">{post.caption}</p>
                  <p className="post-author">Posted by: {post.author_email}</p>
                  {currentUserId === post.user_id && (
                    <div className="post-actions">
                      <button
                        onClick={() => {
                          setEditingPost(post.id);
                          setEditCaption(post.caption);
                        }}
                        style={{ backgroundColor: '#083e13', color: 'white', padding: '8px 12px', marginRight: '8px' }}
                      >
                        Edit
                      </button>
                      <button
                        onClick={() => handleDelete(post.id)}
                        style={{ backgroundColor: '#dc3545', color: 'white', padding: '8px 12px' }}
                      >
                        Delete
                      </button>
                    </div>
                  )}
                </div>
              )}
            </div>
          ))
        ) : (
          <p>No posts available.</p>
        )}
      </div>
    </div>
  );
};

export default CommunityPage;