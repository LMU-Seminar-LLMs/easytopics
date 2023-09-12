import React from 'react';
import MainHeadline from '../../components/typography/MainHeadline';
import Scatterplot from '../../components/Scatterplot';

const Results: React.FC = () => {
  return (
    <>
      <div className='container mx-auto p-4'>
        <MainHeadline text='Results' />
        <Scatterplot />
      </div>
    </>
  );
};

export default Results;
