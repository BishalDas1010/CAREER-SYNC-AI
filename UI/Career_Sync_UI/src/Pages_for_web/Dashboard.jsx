import React from "react";
import {
  Bell,
  Upload,
  TrendingUp,
  Target,
  Puzzle,
  ChevronRight,
  ArrowUp,
  ArrowRight,
  Briefcase,
} from "lucide-react";
import {
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  Radar,
  ResponsiveContainer,
} from "recharts";
import './css_for_web/CareerSyncDashboard.css'

const radarData = [
  { subject: "Python", you: 82, industry: 95 },
  { subject: "Machine Learning", you: 70, industry: 90 },
  { subject: "SQL", you: 65, industry: 80 },
  { subject: "Communication", you: 55, industry: 85 },
  { subject: "DSA", you: 45, industry: 88 },
  { subject: "Data Science", you: 75, industry: 92 },
];

function StatCard({ label, value, total, iconBg, iconColor, icon: Icon, footer, footerColor, barColor, barPct }) {
  return (
    <div className="stat-card">
      <div className="stat-card-top">
        <span className="stat-label">{label}</span>
        <div className="stat-icon" style={{ background: iconBg, color: iconColor }}>
          <Icon size={18} strokeWidth={2.2} />
        </div>
      </div>
      <div className="stat-value">
        {value}
        {total && <span className="stat-total">/{total}</span>}
      </div>
      <div className="stat-footer" style={{ color: footerColor }}>
        {footer}
      </div>
      <div className="stat-bar-track">
        <div className="stat-bar-fill" style={{ width: `${barPct}%`, background: barColor }} />
      </div>
    </div>
  );
}

function StepItem({ number, badgeColor, title, subtitle }) {
  return (
    <div className="step-item">
      <div className="step-badge" style={{ background: badgeColor }}>
        {number}
      </div>
      <div>
        <div className="step-title">{title}</div>
        <div className="step-subtitle">{subtitle}</div>
      </div>
    </div>
  );
}

function JobRow({ logoBg, logo, title, company, match }) {
  return (
    <div className="job-row">
      <div className="job-logo" style={{ background: logoBg }}>
        {logo}
      </div>
      <div className="job-info">
        <div className="job-title">{title}</div>
        <div className="job-company">{company}</div>
      </div>
      <div className="job-right">
        <span className="job-match">{match} Match</span>
        <ChevronRight size={16} color="#9ca3af" />
      </div>
    </div>
  );
}

export default function Dashboard() {
  return (
    <main className="main">
      <div className="main-header">
        <div>
          <h1 className="welcome-title">Welcome back, Vishal 👋</h1>
          <p className="welcome-sub">Here's what's happening with your career journey</p>
        </div>
        <div className="header-actions">
          <button className="upload-btn">
            <Upload size={16} /> Upload New Resume
          </button>
          <div className="bell-wrap">
            <Bell size={18} />
            <div className="bell-dot" />
          </div>
        </div>
      </div>

      {/* STAT CARDS */}
      <div className="stat-grid">
        <StatCard
          label="Career Score"
          value="78"
          total="100"
          icon={TrendingUp}
          iconBg="#eeecfd"
          iconColor="#5b4df0"
          footer="↑ Good"
          footerColor="#16a34a"
          barColor="#5b4df0"
          barPct={78}
        />
        <StatCard
          label="Skills Matched"
          value="24"
          total="35"
          icon={Target}
          iconBg="#e5f2ff"
          iconColor="#2f7fe0"
          footer="68%"
          footerColor="#2f7fe0"
          barColor="#2f7fe0"
          barPct={68}
        />
        <StatCard
          label="Skill Gaps"
          value="11"
          icon={Puzzle}
          iconBg="#feead9"
          iconColor="#f0873c"
          footer="● Improve"
          footerColor="#f0873c"
          barColor="#f0873c"
          barPct={45}
        />
        <StatCard
          label="Job Matches"
          value="32"
          icon={Briefcase}
          iconBg="#e2f7e6"
          iconColor="#16a34a"
          footer="● New"
          footerColor="#16a34a"
          barColor="#16a34a"
          barPct={80}
        />
      </div>

      {/* CONTENT GRID */}
      <div className="content-grid">
        <div className="panel">
          <div className="panel-header">
            <span className="panel-title">Skill Gap Overview</span>
          </div>
          <ResponsiveContainer width="100%" height={260}>
            <RadarChart data={radarData} outerRadius="75%">
              <PolarGrid stroke="#e5e7eb" />
              <PolarAngleAxis dataKey="subject" tick={{ fill: "#6b7280", fontSize: 11.5 }} />
              <Radar dataKey="industry" stroke="#c9c2f7" strokeDasharray="4 3" fill="transparent" strokeWidth={1.5} />
              <Radar dataKey="you" stroke="#5b4df0" fill="#5b4df0" fillOpacity={0.35} strokeWidth={2} />
            </RadarChart>
          </ResponsiveContainer>
          <div className="radar-legend">
            <div className="legend-item">
              <span className="legend-swatch" style={{ background: "#5b4df0" }} />
              Your Level
            </div>
            <div className="legend-item">
              <span className="legend-swatch" style={{ background: "#c9c2f7", borderTop: "2px dashed #c9c2f7" }} />
              Industry Demand
            </div>
          </div>
        </div>

        <div className="panel">
          <div className="panel-header">
            <span className="panel-title">Recommended Next Step</span>
          </div>
          <StepItem number={1} badgeColor="#5b4df0" title="Improve Python" subtitle="Strengthen core concepts" />
          <StepItem number={2} badgeColor="#2f7fe0" title="Strengthen ML Basics" subtitle="Focus on algorithms & models" />
          <StepItem number={3} badgeColor="#16a34a" title="Build Projects" subtitle="Apply skills with real projects" />
          <button className="roadmap-btn">
            View Full Roadmap <ArrowRight size={16} />
          </button>
        </div>

        <div className="panel">
          <div className="panel-header">
            <span className="panel-title">Top Job Matches</span>
            <span className="view-all-link">View all</span>
          </div>
          <JobRow logoBg="#fce8e6" logo="G" title="Machine Learning Engineer" company="Google" match="92%" />
          <JobRow logoBg="#eaf3ff" logo="⊞" title="Data Scientist" company="Microsoft" match="90%" />
          <JobRow logoBg="#fdf1dd" logo="a" title="AI Engineer" company="Amazon" match="90%" />
          <button className="view-jobs-btn">
            View All Jobs <ArrowRight size={16} />
          </button>
        </div>
      </div>

      {/* BOTTOM BANNER */}
      <div className="banner">
        <div className="banner-icon">
          <Target size={26} />
        </div>
        <div>
          <p className="banner-title">Keep going, Vishal 🚀</p>
          <p className="banner-sub">
            You're doing great! Focus on improving your skills and building projects to boost your career score.
          </p>
        </div>
        <div className="banner-stats">
          <span className="banner-points">+12</span>
          <span className="banner-points-label">Points this week</span>
          <span className="banner-badge">
            <ArrowUp size={12} /> 8% from last week
          </span>
        </div>
      </div>
    </main>
  );
}