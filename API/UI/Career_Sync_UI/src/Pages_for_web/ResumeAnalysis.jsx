import React, { useRef, useState } from "react";
import { Lottie } from "lottie-react";                        // FIXED: default import
import emptyAnimation from '../assets/Empty red (1).json';
import './css_for_web/ResumeAnalysis.css';

// Point this at wherever the FastAPI backend actually runs.
// Override with VITE_API_BASE_URL in your .env if it's not localhost:8000.
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

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

// ---------- Helpers ----------
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

// Turns a scoreCard's value/suffix into a 0–100 ring percentage.
function ringValue(card) {
  if (typeof card.value !== "number") return 0;
  if (card.suffix === "%") return card.value;
  if (card.suffix === "/100") return card.value;
  if (card.suffix && card.suffix.startsWith("/")) {
    const denom = parseFloat(card.suffix.slice(1)) || 100;
    return (card.value / denom) * 100;
  }
  return card.value;
}

// ---------- Empty / Upload State ----------
function EmptyResumeState({ onUploadClick, uploading, error }) {
  return (
    <div className="empty-state">
      <Lottie
        src={emptyAnimation}
        loop={true}
        autoplay={true}
        style={{ width: 150, height: 200 }}
      />
      <h2>No Resume Uploaded Yet</h2>
      <p>Upload your resume to get a detailed analysis.</p>

      {error && <p className="upload-error">{error}</p>}

      <button className="btn-primary" type="button" onClick={onUploadClick} disabled={uploading}>
        <UploadCloud size={16} />
        {uploading ? "Analyzing..." : "Upload Resume"}
      </button>
    </div>
  );
}

// ---------- Main Component ----------
export default function ResumeAnalysis() {
  const fileInputRef = useRef(null);
  const [analysis, setAnalysis] = useState(null);
  const [fileName, setFileName] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);

  const triggerFilePicker = () => {
    setError(null);
    fileInputRef.current?.click();
  };

  const handleFileSelected = async (event) => {
    const selectedFile = event.target.files?.[0];
    // Let the user re-select the same file later.
    event.target.value = "";
    if (!selectedFile) return;

    setUploading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append("file", selectedFile);

      const response = await fetch(`${API_BASE_URL}/upload`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        let detail = `Upload failed (${response.status})`;
        try {
          const errBody = await response.json();
          if (errBody?.detail) detail = errBody.detail;
        } catch {
          // response wasn't JSON, keep the generic message
        }
        throw new Error(detail);
      }

      const data = await response.json();
      setAnalysis(data.analysis);
      setFileName(data.filename);
    } catch (err) {
      setError(err.message || "Something went wrong uploading your resume.");
      setAnalysis(null);
    } finally {
      setUploading(false);
    }
  };

  const hiddenInput = (
    <input
      ref={fileInputRef}
      type="file"
      accept=".pdf,.docx,.doc,.txt,.rtf"
      onChange={handleFileSelected}
      style={{ display: "none" }}
    />
  );

  // Early return for empty / not-yet-analyzed state
  if (!analysis) {
    return (
      <div className="app-shell">
        <main className="main-content">
          <EmptyResumeState onUploadClick={triggerFilePicker} uploading={uploading} error={error} />
          {hiddenInput}
        </main>
      </div>
    );
  }

  const {
    scoreCards = [],
    sections = [],
    matchedKeywords = [],
    missingKeywords = [],
    suggestions = [],
  } = analysis;

  // Render analysis dashboard
  return (
    <div className="app-shell">
      <main className="main-content">
        <header className="page-header">
          <div>
            <h1>Resume Analysis</h1>
            <p>
              A section-by-section breakdown of {fileName ? `"${fileName}"` : "your resume"}'s strengths and gaps
            </p>
          </div>
          <button className="btn-primary" onClick={triggerFilePicker} disabled={uploading}>
            <UploadCloud size={16} />
            {uploading ? "Analyzing..." : "Upload New Resume"}
          </button>
          {hiddenInput}
        </header>

        {error && <p className="upload-error">{error}</p>}

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
              <ScoreRing value={ringValue(card)} />
            </div>
          ))}
        </section>

        <section className="content-grid">
          <div className="panel">
            <div className="panel-header">
              <h2>Section Breakdown</h2>
              <span className="panel-subtitle">{sections.length} sections analyzed</span>
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
              <span className="panel-subtitle">
                {matchedKeywords.length} of {matchedKeywords.length + missingKeywords.length} target keywords found
              </span>
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