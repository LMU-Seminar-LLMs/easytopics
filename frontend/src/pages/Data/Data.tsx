import React, { useState, useEffect } from 'react';
import MainHeadline from '../../components/typography/MainHeadline';
import DefaultParagraph from '../../components/typography/DefaultParagraph';
import CsvUploadComponent from '../../components/UploadCsv';
import DataTable from '../../components/DataTable';

import {
  DataGrid,
  GridColDef,
  GridFilterModel,
  GridFilterItem,
} from '@mui/x-data-grid';

const columns: GridColDef[] = [
  {
    field: 'id',
    headerName: 'ID',
    type: 'number',
    flex: 1,
    headerAlign: 'center',
    align: 'center',
    headerClassName: '',
  },
  {
    field: 'text',
    headerName: 'Text',
    type: 'text',
    flex: 12,
    headerClassName: '',
  },
];

const Data: React.FC = () => {
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [tableData, setTableData] = useState<any[] | null>(null);

  // checks on component mount if there is data in the backend
  const fetchData = async () => {
    const dataResponse = await fetch('http://localhost:5000/documents');
    if (dataResponse.ok) {
      const data = await dataResponse.json();
      setTableData(data);
    } else {
      console.error('Error fetching the processed data.');
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  // gets called when a file is uploaded
  const handleUpload = async (file: File) => {
    setUploadedFile(file);

    const dataResponse = await fetch('http://localhost:5000/documents');
    if (dataResponse.ok) {
      const data = await dataResponse.json();
      // Set the tableData state with the received data
      setTableData(data);
    } else {
      console.error('Error fetching the processed data.');
    }
  };

  return (
    <>
      <div className='container mx-auto p-4'>
        <MainHeadline text='Data' />
        <CsvUploadComponent onUpload={handleUpload} />
        {/* Display the uploaded file name */}
        {uploadedFile && <p>Uploaded File: {uploadedFile.name}</p>}
      </div>

      <div className='container mx-auto p-4'>
        <MainHeadline text='Preview' />
        {tableData && tableData.length > 0 ? (
          <>
            <div className='italic text-gray-500 pb-2'>
              <DefaultParagraph text='Hover over column names for sort and filter options.' />
            </div>
            <DataTable data={tableData} columns={columns} />
          </>
        ) : (
          <div className='italic text-gray-500 font-light p-2'>
            -- You first need to upload a file. --
          </div>
        )}
      </div>
    </>
  );
};

export default Data;
