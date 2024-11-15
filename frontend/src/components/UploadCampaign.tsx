// UploadCampaign.tsx
import React, { useState } from "react";

const UploadCampaign: React.FC = () => {
  const [campaignFile, setCampaignFile] = useState<File | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setCampaignFile(e.target.files[0]);
    }
  };

  const handleUpload = () => {
    if (campaignFile) {
      // Simulate uploading campaign file
      console.log("Uploading campaign file: ", campaignFile.name);
      // Here you can call the API or handle the file upload logic
    } else {
      alert("Please select a file to upload.");
    }
  };

  return (
    <div className="upload-campaign-container">
      <h2>Upload Campaign</h2>
      <input
        type="file"
        onChange={handleFileChange}
        accept=".csv,.xls,.xlsx"
      />
      <button onClick={handleUpload}>Upload Campaign</button>
      {campaignFile && <p>Selected file: {campaignFile.name}</p>}
    </div>
  );
};

export default UploadCampaign;
