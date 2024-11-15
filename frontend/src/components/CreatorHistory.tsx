// CreatorHistory.tsx
import React from "react";

const CreatorHistory: React.FC = () => {
  return (
    <div className="creator-history-container">
      <h2>Creator History</h2>
      <p>Here you can view the history of campaigns and interactions for each creator.</p>
      {/* You can add functionality to fetch and display creator history here */}
      <div className="history-list">
        <ul>
          <li>Creator 1 - Campaign 1</li>
          <li>Creator 2 - Campaign 2</li>
          <li>Creator 3 - Campaign 3</li>
        </ul>
      </div>
    </div>
  );
};

export default CreatorHistory;
