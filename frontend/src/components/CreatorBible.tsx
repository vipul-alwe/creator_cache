// CreatorBible.tsx
import React from "react";

const CreatorBible: React.FC = () => {
  return (
    <div className="creator-bible-container">
      <h2>Creator Bible</h2>
      <p>Here you can view all the creator data stored in the database.</p>
      {/* You can add functionality to fetch and display the creator data here */}
      <div className="creator-list">
        <ul>
          <li>Creator 1</li>
          <li>Creator 2</li>
          <li>Creator 3</li>
        </ul>
      </div>
    </div>
  );
};

export default CreatorBible;
