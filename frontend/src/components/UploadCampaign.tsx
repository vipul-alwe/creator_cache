import React, { useState } from "react";
import axios from "axios";
import "../styles/UploadCampaign.css"

const UploadCampaign: React.FC = () => {
  const [campaignName, setCampaignName] = useState<string>("");
  const [file, setFile] = useState<File | null>(null);
  const [csvData, setCsvData] = useState<any[]>([]);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setFile(file);
    }
  };

  const handleCampaignNameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setCampaignName(e.target.value);
  };

  const handleDownloadTemplate = () => {
    const template = [
      "creator_name,ucid,gender,language,genre,ig_handle,pct_13_17,yt_genz_13_24,rpr,contacts,contact_number,email_id,median_views,campaign_name,date,brand_name,trend_type,current_cost,current_deliverables"
    ];
    const blob = new Blob([template.join("\n")], { type: "text/csv" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "campaign_template.csv";
    link.click();
  };

  const handleUpload = async () => {
    if (!campaignName || !file) {
      setErrorMessage("Please provide both campaign name and CSV file.");
      return;
    }

    const formData = new FormData();
    formData.append("campaign_name", campaignName);
    formData.append("csv", file);

    try {
      const response = await axios.post("/your-api-endpoint-to-upload-csv", formData);
      const { data } = response;

      // Process CSV data if needed, or show a success message
      setCsvData(data.csvData);
      setErrorMessage(null);
    } catch (error) {
      setErrorMessage("Failed to upload CSV data. Please try again.");
    }
  };

  const handleSubmit = async () => {
    // Send the data to the backend for further processing
    try {
      const response = await axios.post("/your-api-endpoint-to-submit-csv", {
        data: csvData,
      });
      // Handle the response
      console.log(response.data);
    } catch (error) {
      setErrorMessage("Failed to submit the data. Please try again.");
    }
  };

  const validateCsvColumns = (data: any[]) => {
    const requiredColumns = [
      "creator_name",
      "ucid",
      "contacts",
      "contact_number",
      "campaign_name",
      "date",
      "current_cost",
      "current_deliverables",
    ];
    const columns = Object.keys(data[0]);
    const missingColumns = requiredColumns.filter((column) => !columns.includes(column));

    if (missingColumns.length > 0) {
      setErrorMessage(`Missing required columns: ${missingColumns.join(", ")}`);
      return false;
    }

    return true;
  };

  return (
    <div className="upload-campaign">
      <div className="form-container">
        <h2>Upload Campaign</h2>
        <div className="form-group">
          <label htmlFor="campaign-name">Campaign Name</label>
          <input
            type="text"
            id="campaign-name"
            value={campaignName}
            onChange={handleCampaignNameChange}
            placeholder="Enter Campaign Name"
          />
        </div>

        <div className="form-group">
          <label htmlFor="csv-upload">Upload CSV</label>
          <input
            type="file"
            id="csv-upload"
            accept=".csv"
            onChange={handleFileChange}
          />
        </div>

        <button onClick={handleUpload}>Upload CSV</button>

        {errorMessage && <div className="error-message">{errorMessage}</div>}

        <button onClick={handleDownloadTemplate}>Download CSV Template</button>
      </div>

      {/* Display Uploaded CSV Data */}
      {csvData.length > 0 && (
        <div className="csv-preview">
          <h3>CSV Data Preview</h3>
          <table>
            <thead>
              <tr>
                {Object.keys(csvData[0]).map((key) => (
                  <th key={key}>{key}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {csvData.map((row, index) => (
                <tr key={index}>
                  {Object.values(row).map((value, i) => (
                    <td key={i}>{value}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
          <button onClick={handleSubmit}>Submit CSV</button>
        </div>
      )}
    </div>
  );
};

export default UploadCampaign;
