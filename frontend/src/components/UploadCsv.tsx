import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';

interface CsvUploadProps {
  onUpload: (file: File) => void;
}

const CsvUploadComponent: React.FC<CsvUploadProps> = ({ onUpload }) => {
  const [uploading, setUploading] = useState(false);

  const onDrop = useCallback(
    async (acceptedFiles: File[]) => {
      if (acceptedFiles.length === 1) {
        const file = acceptedFiles[0];

        try {
          setUploading(true);

          // Create a FormData object to send the file to the backend
          const formData = new FormData();
          formData.append('file', file);

          // Make the API call to backend
          const response = await fetch('http://localhost:5000/documents', {
            method: 'POST',
            body: formData,
          });

          if (response.ok) {
            onUpload(file);
          } else {
            // Handle any API errors here
            // 'response.statusText' will contain the error message
            alert('Error uploading CSV file: ' + response.statusText);
          }
        } catch (error) {
          console.error('An error occurred:', error);
          alert('An error occurred while uploading the file.');
        } finally {
          setUploading(false);
        }
      } else {
        alert('Please upload only one CSV file.');
      }
    },
    [onUpload]
  );

  const { getRootProps, getInputProps } = useDropzone({
    accept: {
      'text/csv': ['.csv'],
    },
    onDrop,
  });

  return (
    <div
      {...getRootProps()}
      className='border border-dashed border-indigo-900 p-4'
    >
      <input {...getInputProps()} />
      {uploading ? (
        <p className='text-center'>Uploading...</p>
      ) : (
        <p className='text-center'>
          Drag & drop a CSV file with a "text" column here, or click to select
          one.
        </p>
      )}
    </div>
  );
};

export default CsvUploadComponent;
