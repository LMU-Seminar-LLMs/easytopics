// Routes.tsx
import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Home from '../pages/Home';
import Data from '../pages/Data';
import Qa from '../pages/Qa';
import Analysis from '../pages/Analysis';
import Results from '../pages/Results';
import Save from '../pages/Save';

const MyRoutes = () => {
  return (
    <Routes>
      <Route path='/' element={<Home />} />
      <Route path='/data' element={<Data />} />
      <Route path='/qa' element={<Qa />} />
      <Route path='/analysis' element={<Analysis />} />
      <Route path='/results' element={<Results />} />
      <Route path='/save' element={<Save />} />
    </Routes>
  );
};

export default MyRoutes;
