// import React, { useState, useEffect } from 'react';
// import axios from 'axios';

// const CommunityPage = () => {
//   const [caption, setCaption] = useState('');
//   const [posts, setPosts] = useState([]);

//   useEffect(() => {
//     const fetchPosts = async () => {
//       const response = await axios.get('http://127.0.0.1:4444/community-posts');
//       setPosts(response.data);
//     };
//     fetchPosts();
//   }, []);

//   const handlePost = async () => {
//     if (caption.trim()) {
//       const response = await axios.post('http://127.0.0.1:4444/community-post', 
//         { caption }
//       );
//       setPosts([response.data, ...posts]);
//       setCaption('');
//     }
//   };

//   return (
//     <div className="community-page">
//       <div className="post-form">
//         <textarea
//           value={caption}
//           onChange={(e) => setCaption(e.target.value)}
//           placeholder="What's on your mind?"
//         />
//         <button onClick={handlePost}>Post</button>
//       </div>

//       <div className="posts-list">
//         {posts.map(post => (
//           <div key={post.id} className="post-card">
//             <p className="post-caption">{post.caption}</p>
//           </div>
//         ))}
//       </div>
//     </div>
//   );
// };

// export default CommunityPage;
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const CommunityPage = () => {
  const [caption, setCaption] = useState('');
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    const fetchPosts = async () => {
      const response = await axios.get('http://127.0.0.1:4444/community-posts');
      setPosts(response.data);
    };
    fetchPosts();
  }, []);

  const handlePost = async () => {
    if (caption.trim()) {
      const response = await axios.post('http://127.0.0.1:4444/community-post', 
        { caption }
      );
      setPosts([response.data, ...posts]);
      setCaption('');
    }
  };

  return (
    <div className="community-page">
      <div className="post-form">
        <textarea
          value={caption}
          onChange={(e) => setCaption(e.target.value)}
          placeholder="What's on your mind?"
        />
        <button onClick={handlePost}>Post</button>
      </div>

      <div className="posts-list">
        {posts.map(post => (
          <div key={post.id} className="post-card">
            <p className="post-caption">{post.caption}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default CommunityPage;
