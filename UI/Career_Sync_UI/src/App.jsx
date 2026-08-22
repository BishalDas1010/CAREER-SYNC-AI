import React from 'react'
import './index.css'
import { BrowserRouter, Routes, Route } from 'react-router-dom'


import HomePage from './Pages_for_web/firstPage'
import LoginPage from './Pages_for_web/LoginPage'
import Register from './Pages_for_web/Register'
import ResumeAnalysis from './Pages_for_web/ResumeAnalysis'
import VerifyOtp from './Pages_for_web/VerifyOtp'


export default function App() {
  return (
    <BrowserRouter>
      <Routes>

        <Route path="/" element={<HomePage />} />

        <Route path="/login" element={<LoginPage />} />

        <Route path="/register" element={<Register />} />

        <Route path="/resume-analysis" element={<ResumeAnalysis />} />

      <Route path="/verify-otp" element={<VerifyOtp />} />
      </Routes>
    </BrowserRouter>
  )
}