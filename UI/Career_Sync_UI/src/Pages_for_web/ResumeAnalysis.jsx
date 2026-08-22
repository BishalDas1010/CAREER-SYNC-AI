import React from "react";

// Minimal placeholder icons to avoid pulling the `lucide-react` dependency
// in environments where React 19 causes peer dependency conflicts.
const IconPlaceholder = ({ label = "", size = 18, className = "" }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" className={className} aria-hidden>
    <rect x="2" y="2" width="20" height="20" rx="3" fill="currentColor" opacity="0.08" />
    <text x="50%" y="55%" dominantBaseline="middle" textAnchor="middle" fontSize="9" fill="currentColor">
      {label}
    </text>
  </svg>
);

const LayoutDashboard = (props) => <IconPlaceholder label="DB" {...props} />;
const FileText = (props) => <IconPlaceholder label="FT" {...props} />;
const Target = (props) => <IconPlaceholder label="T" {...props} />;
const Map = (props) => <IconPlaceholder label="M" {...props} />;
const Briefcase = (props) => <IconPlaceholder label="B" {...props} />;
const MessageSquare = (props) => <IconPlaceholder label="MS" {...props} />;
const Bookmark = (props) => <IconPlaceholder label="BK" {...props} />;
const Settings = (props) => <IconPlaceholder label="S" {...props} />;
const LogOut = (props) => <IconPlaceholder label="LO" {...props} />;
const Sparkles = (props) => <IconPlaceholder label="*" {...props} />;
const UploadCloud = (props) => <IconPlaceholder label="U" {...props} />;
const CheckCircle2 = (props) => <IconPlaceholder label="✓" {...props} />;
const AlertTriangle = (props) => <IconPlaceholder label="!" {...props} />;
const XCircle = (props) => <IconPlaceholder label="✕" {...props} />;
const ChevronRight = (props) => <IconPlaceholder label=">" {...props} />;
const Wand2 = (props) => <IconPlaceholder label="✨" {...props} />;
import './css_for_web/ResumeAnalysis.css'

const navItems = [
  { icon: LayoutDashboard, label: "Dashboard" },
  { icon: FileText, label: "Resume Analysis", active: true },
  { icon: Target, label: "Skill Gap" },
  { icon: Map, label: "Roadmap" },
  { icon: Briefcase, label: "Job Recommendations" },
  { icon: MessageSquare, label: "Chat Assistant" },
  { icon: Bookmark, label: "Bookmarks" },
];

const bottomNavItems = [
  { icon: Settings, label: "Settings" },
  { icon: LogOut, label: "Logout" },
];

const scoreCards = [
  { label: "Overall Score", value: 78, suffix: "/100", status: "Good", tone: "good" },
  { label: "ATS Compatibility", value: 92, suffix: "%", status: "Excellent", tone: "good" },
  { label: "Keywords Matched", value: 24, suffix: "/35", status: "Improve", tone: "warn" },
  { label: "Readability", value: "A-", suffix: "", status: "Strong", tone: "good" },
];

const sections = [
  { name: "Contact Information", score: 100, status: "complete" },
  { name: "Professional Summary", score: 85, status: "complete" },
  { name: "Work Experience", score: 74, status: "complete" },
  { name: "Skills", score: 60, status: "warn" },
  { name: "Education", score: 100, status: "complete" },
  { name: "Projects", score: 45, status: "missing" },
];

const matchedKeywords = ["Python", "REST APIs", "Git", "SQL", "Data Structures", "FastAPI", "Docker"];
const missingKeywords = ["Kubernetes", "LangChain", "System Design", "CI/CD", "AWS"];

const suggestions = [
  {
    priority: "High",
    title: "Add measurable impact to your project bullets",
    detail: "3 of 5 project descriptions lack quantified outcomes (e.g., \"reduced latency by 40%\").",
  },
  {
    priority: "High",
    title: "Include a dedicated Projects section",
    detail: "Recruiters for AI roles expect visible project depth above the fold.",
  },
  {
    priority: "Medium",
    title: "Add missing high-demand keywords",
    detail: "Kubernetes, LangChain and System Design appear in 68% of matched job postings.",
  },
  {
    priority: "Low",
    title: "Tighten your professional summary",
    detail: "Currently 4 lines — trim to 2–3 lines for faster recruiter scanning.",
  },
];

function ScoreRing({ value }) {
  const radius = 30;
  const circumference = 2 * Math.PI * radius;
  const progress = Math.min(Math.max(value, 0), 100) / 100;
  const offset = circumference * (1 - progress);

  return (
    <svg width="72" height="72" viewBox="0 0 72 72" className="score-ring">
      <circle cx="36" cy="36" r={radius} className="score-ring-track" strokeWidth="7" fill="none" />
      <circle
        cx="36"
        cy="36"
        r={radius}
        className="score-ring-progress"
        strokeWidth="7"
        fill="none"
        strokeDasharray={circumference}
        strokeDashoffset={offset}
        strokeLinecap="round"
      />
    </svg>
  );
}

function StatusIcon({ status }) {
  if (status === "complete") return <CheckCircle2 size={18} className="icon-good" />;
  if (status === "warn") return <AlertTriangle size={18} className="icon-warn" />;
  return <XCircle size={18} className="icon-bad" />;
}

export default function ResumeAnalysis() {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="sidebar-brand">
          <div className="brand-icon">
            <Sparkles size={18} />
          </div>
          <span>Career Sync AI</span>
        </div>

        <nav className="sidebar-nav">
          {navItems.map((item) => (
            <button key={item.label} className={`nav-item ${item.active ? "active" : ""}`}>
              <item.icon size={18} />
              <span>{item.label}</span>
            </button>
          ))}
        </nav>

        <div className="sidebar-nav sidebar-nav-bottom">
          {bottomNavItems.map((item) => (
            <button key={item.label} className="nav-item">
              <item.icon size={18} />
              <span>{item.label}</span>
            </button>
          ))}
        </div>
      </aside>

      <main className="main-content">
        <header className="page-header">
          <div>
            <h1>Resume Analysis</h1>
            <p>A section-by-section breakdown of your resume's strengths and gaps</p>
          </div>
          <button className="btn-primary">
            <UploadCloud size={16} />
            Upload New Resume
          </button>
        </header>

        <section className="score-grid">
          {scoreCards.map((card) => (
            <div className="score-card" key={card.label}>
              <div>
                <p className="score-label">{card.label}</p>
                <p className="score-value">
                  {card.value}
                  <span className="score-suffix">{card.suffix}</span>
                </p>
                <span className={`badge badge-${card.tone}`}>{card.status}</span>
              </div>
              {typeof card.value === "number" && card.suffix !== "/35" ? (
                <ScoreRing value={card.suffix === "%" ? card.value : card.value} />
              ) : (
                <ScoreRing value={(card.value / (card.suffix === "/35" ? 35 : 100)) * 100} />
              )}
            </div>
          ))}
        </section>

        <section className="content-grid">
          <div className="panel">
            <div className="panel-header">
              <h2>Section Breakdown</h2>
              <span className="panel-subtitle">6 sections analyzed</span>
            </div>
            <div className="section-list">
              {sections.map((s) => (
                <div className="section-row" key={s.name}>
                  <div className="section-row-top">
                    <div className="section-row-name">
                      <StatusIcon status={s.status} />
                      <span>{s.name}</span>
                    </div>
                    <span className="section-row-score">{s.score}%</span>
                  </div>
                  <div className="progress-track">
                    <div
                      className={`progress-fill fill-${s.status}`}
                      style={{ width: `${s.score}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="panel">
            <div className="panel-header">
              <h2>Keyword Match</h2>
              <span className="panel-subtitle">24 of 35 target keywords found</span>
            </div>

            <p className="keyword-group-label">Matched</p>
            <div className="chip-row">
              {matchedKeywords.map((kw) => (
                <span className="chip chip-good" key={kw}>
                  {kw}
                </span>
              ))}
            </div>

            <p className="keyword-group-label">Missing</p>
            <div className="chip-row">
              {missingKeywords.map((kw) => (
                <span className="chip chip-bad" key={kw}>
                  {kw}
                </span>
              ))}
            </div>
          </div>
        </section>

        <section className="panel suggestions-panel">
          <div className="panel-header">
            <h2>Improvement Suggestions</h2>
            <button className="link-btn">
              View All <ChevronRight size={14} />
            </button>
          </div>
          <div className="suggestion-list">
            {suggestions.map((sug) => (
              <div className="suggestion-row" key={sug.title}>
                <span className={`priority-tag priority-${sug.priority.toLowerCase()}`}>
                  {sug.priority}
                </span>
                <div className="suggestion-text">
                  <p className="suggestion-title">{sug.title}</p>
                  <p className="suggestion-detail">{sug.detail}</p>
                </div>
                <button className="btn-ghost">
                  <Wand2 size={14} />
                  Fix with AI
                </button>
              </div>
            ))}
          </div>
        </section>
      </main>
    </div>
  );
}