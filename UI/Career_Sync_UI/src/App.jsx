
import React from 'react'
import './index.css'
import { BrowserRouter, Routes, Route } from 'react-router-dom'

import HomePage from './Pages_for_web/firstPage'
import LoginPage from './Pages_for_web/LoginPage'
import Register from './Pages_for_web/Register'
import Onboarding from './Pages_for_web/Onboarding'

import Dashboard from './Pages_for_web/Dashboard'
import ResumeAnalysis from './Pages_for_web/ResumeAnalysis'
import Sidebar from './Pages_for_web/Sidebar'

import DashboardLayout from './Pages_for_web/DashboardLayout'
import ChatAssistant from './Pages_for_web/Chat'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>

        {/* Public routes — no sidebar */}
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<Register />} />
        <Route path="/onboarding" element={<Onboarding />} />

        {/* App routes — wrapped in layout with sidebar */}
        <Route element={<DashboardLayout />}>
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/resume-analysis" element={<ResumeAnalysis />} />
      <Route path ="/chat-assistant" element = {<ChatAssistant />}/>
    </Route>

      </Routes>
    </BrowserRouter>
  )
}
