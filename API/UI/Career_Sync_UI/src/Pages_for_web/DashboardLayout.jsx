import { Outlet } from 'react-router-dom'

import Sidebar from './Sidebar.jsx'


export default function DashboardLayout() {
  return (
    <div className="cs-app">
      <Sidebar />
      <Outlet />
    </div>
  )
}