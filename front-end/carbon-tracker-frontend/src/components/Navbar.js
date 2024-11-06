import React from 'react';

function Navbar() {
  return (
    <div className="w-full p-4 bg-green-800 flex justify-around text-white fixed bottom-0 left-0">
      <span className="text-2xl">🏠</span>
      <span className="text-2xl">👤</span>
      <span className="text-2xl">✏️</span>
      <span className="text-2xl">⚙️</span>
    </div>
  );
}

export default Navbar;
