import { NavLink } from "react-router-dom";
import {
  Home,
  FileText,
  BarChart2,
  Map,
  Briefcase,
  MessageCircle,
  Bookmark,
  Settings,
  LogOut,
  ChevronDown,
} from "lucide-react";

import './css_for_web/sidebar.css'

function Sidebar() {
  return (
    <aside className="sidebar">

      {/* Brand */}
      <div className="brand">
        <span>◆</span>
        Career Sync <span className="brand-ai">AI</span>
      </div>

      {/* Main Navigation */}
      <div className="nav-section">

        <NavLink
        to="/dashboard"
        end
        className={({ isActive }) => `nav-item ${isActive ? "nav-item-active" : ""}`}>
        <Home size={18} />
        <span>Dashboard</span>
        </NavLink>

        <NavLink
          to="/resume-analysis"
          className={({ isActive }) => `nav-item ${isActive ? "nav-item-active" : ""}`}
        >
          <FileText size={18} />
          <span>Resume Analysis</span>
        </NavLink>


        <NavLink
          to="/chat-assistant"
          className={({ isActive }) => `nav-item ${isActive ? "nav-item-active" : ""}`}
        >
          <MessageCircle size={18} />
          <span>Chat Assistant</span>
        </NavLink>



      </div>

      <div className="nav-divider" />

      {/* Bottom Navigation */}
      <div className="nav-section">

        <NavLink
          to="/settings"
          className={({ isActive }) => `nav-item ${isActive ? "nav-item-active" : ""}`}
        >
          <Settings size={18} />
          <span>Settings</span>
        </NavLink>

        <NavLink
          to="/logout"
          className={({ isActive }) => `nav-item ${isActive ? "nav-item-active" : ""}`}
        >
          <LogOut size={18} />
          <span>Logout</span>
        </NavLink>

      </div>

      {/* Profile */}
      <div className="profile-card">

        <div className="profile-avatar">
          VD
        </div>

        <div className="profile-info">
          <div className="profile-name">
            Vishal Das
          </div>

          <div className="profile-email">
            vishal@example.com
          </div>
        </div>

        <ChevronDown size={16} />

      </div>

    </aside>
  );
}

export default Sidebar;