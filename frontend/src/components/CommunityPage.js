// CommunityPage.js: Page where user can post, edit, and delete as well as view other users posts

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const CommunityPage = () => {
      // Log the authentication token for debugging purposes
  console.log('Auth Token:', localStorage.getItem('authToken'));
// State management hooks
  // caption: for creating new posts
  // posts: stores the list of community posts
  // editingPost: tracks which post is currently being edited
  // editCaption: stores the edited post text
  // error: manages error messages
  // loading: controls UI state during async operations
  const [caption, setCaption] = useState('');
  const [posts, setPosts] = useState([]);
  const [editingPost, setEditingPost] = useState(null);
  const [editCaption, setEditCaption] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  // Navigation hook for programmatic routing
  const navigate = useNavigate();
 // Utility function to extract user ID from JWT token
  // Decodes the token and returns the user's ID
  const getCurrentUserId = () => {
    const token = localStorage.getItem('authToken');
    if (token) {
    // Decode the JWT token's payload
      const payload = JSON.parse(atob(token.split('.')[1]));
      console.log('Decoded Token Payload:', payload);
      return parseInt(payload.sub, 10);
    }
    return null;
  };
// Fetch posts when component mounts
  useEffect(() => {
    fetchPosts();
  }, []);
// Async function to fetch community posts from the backend
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

  // Handle creating a new post
  const handlePost = async () => {
    try {
        
      const token = localStorage.getItem('authToken');
      console.log('Token before request:', token);
// Send post request with authorization token
      const response = await axios.post(
        'http://127.0.0.1:4444/community-post',
        { caption },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
    // Update posts list and clear caption input
      setPosts([response.data, ...posts]);
      setCaption('');
    } catch (error) {
      console.error('Error creating post:', error.response?.data || error.message);
     
      // Handle unauthorized/expired token
      if (error.response && error.response.status === 401) {
        alert('Session expired. Please log in again.');
        localStorage.removeItem('authToken');
        navigate('/login');
      }
    }
  };
  // Handle editing an existing post
  const handleEdit = async (postId) => {
    // Validate edit input
    if (!editCaption.trim()) {
      setError('Please enter some text for your post.');
      return;
    }
  
    setLoading(true);
    try {
      const token = localStorage.getItem('authToken');
      console.log('Token before edit request:', token);  // Debugging statement
        // Send PUT request to update post
      const response = await axios.put(
        `http://127.0.0.1:4444/community-post/${postId}`,
        { caption: editCaption },
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );
    
    // Update posts list with edited post
      setPosts(posts.map(post => (post.id === postId ? response.data : post)));
    // Reset editing state
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
  
// Handle deleting a post
  const handleDelete = async (postId) => {
    const token = localStorage.getItem('authToken');
     // Confirm deletion with user
    console.log('Attempting to delete post with ID:', postId); // Debugging
    console.log('Token used for deletion:', token); // Debugging
  
    if (!window.confirm('Are you sure you want to delete this post?')) {
      return;
    }
  // Send DELETE request to remove post
    setLoading(true);
    try {
      await axios.delete(
        `http://127.0.0.1:4444/community-post/${postId}`,
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );

    // Remove post from local state
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

  // Render the community page UI
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