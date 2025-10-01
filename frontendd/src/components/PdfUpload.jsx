import React, { useState } from 'react';

const PdfUpload = () => {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');
  const [uploading, setUploading] = useState(false);

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];

    if (selectedFile && selectedFile.type === 'application/pdf') {
      setFile(selectedFile);
      setMessage('');
    } else {
      setFile(null);
      setMessage('Please select a valid PDF file.');
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage('No PDF file selected.');
      return;
    }

    const formData = new FormData();
    formData.append('pdf', file); // This key name should match what your Django backend expects

    try {
      setUploading(true);
      setMessage('');

      const response = await fetch('http://localhost:8000/api/upload/', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setMessage(`✅ Uploaded: ${data.file_path || 'Success'}`);
        setFile(null);
      } else {
        const errorData = await response.json();
        console.error("Backend error:", errorData); 
        setMessage(`❌ Error: ${errorData.error || 'Upload failed.'}`);
      }
    } catch (error) {
      console.error('Upload error:', error);
      setMessage('❌ Network or server error occurred.');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div style={styles.container}>
      <h2>Upload PDF</h2>
      <input type="file" accept="application/pdf" onChange={handleFileChange} />
      <button
        onClick={handleUpload}
        disabled={uploading || !file}
        style={styles.button}
      >
        {uploading ? 'Uploading...' : 'Upload'}
      </button>
      {message && <p style={styles.message}>{message}</p>}
    </div>
  );
};

const styles = {
  container: {
    padding: '20px',
    border: '1px solid #ccc',
    maxWidth: '400px',
    margin: '20px auto',
    borderRadius: '6px',
    textAlign: 'center',
  },
  button: {
    marginTop: '10px',
    padding: '10px 20px',
    cursor: 'pointer',
  },
  message: {
    marginTop: '15px',
    fontWeight: 'bold',
  },
};

export default PdfUpload;
