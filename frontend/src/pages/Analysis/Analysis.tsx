import React, { useState } from 'react';
import MainHeadline from '../../components/typography/MainHeadline';
import { CircularProgress, Button } from '@mui/material';

const Analysis: React.FC = () => {
  const [isLoading, setIsLoading] = useState(false);

  const handleClick = async () => {
    setIsLoading(true);
    await new Promise((resolve) => setTimeout(resolve, 5000)); // wait 5 seconds
    setIsLoading(false);
  };

  return (
    <>
      <div className='container mx-auto p-4'>
        <MainHeadline text='Analysis' />
        <div className='flex justify-center pt-5'>
          <div className='loading-container'>
            <Button onClick={handleClick} disabled={isLoading}>
              {isLoading ? <CircularProgress /> : 'Make API Call'}
            </Button>
          </div>
        </div>
      </div>
    </>
  );
};

export default Analysis;
