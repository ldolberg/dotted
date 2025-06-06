import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import PatientListPage from './pages/patients/PatientListPage';
import HomePage from './pages/HomePage';
import logo from './logo.svg';
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/patients" element={<PatientListPage />} />
        <Route path="/" element={<HomePage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
