import React, { useState, useRef, useEffect } from "react";
import { MessageCircle, Search, Trash2, Plus } from "lucide-react";
import './css_for_web/chat_history.css'

const initialSessions = [
  {
    id: 1,
    title: "Resume feedback for data analyst role",
    preview: "You asked for tips to tighten your experience bullets...",
    date: "Today, 9:02 AM",
  },
  {
    id: 2,
    title: "Skill roadmap discussion",
    preview: "We mapped out SQL, Python, and dashboarding as next steps...",
    date: "Yesterday, 4:41 PM",
  },
  {
    id: 3,
    title: "Mock interview — behavioral round",
    preview: "Practiced answers using the STAR method for teamwork...",
    date: "Sep 1, 11:15 AM",
  },
  {
    id: 4,
    title: "Job search strategy for remote roles",
    preview: "Discussed where to focus applications this month...",
    date: "Aug 28, 2:30 PM",
  },
];

export default function ChatHistory() {
  const [sessions, setSessions] = useState(initialSessions);
  const [query, setQuery] = useState("");

  const filtered = sessions.filter((s) =>
    s.title.toLowerCase().includes(query.toLowerCase())
  );

  function handleDelete(id, e) {
    e.stopPropagation();
    setSessions((prev) => prev.filter((s) => s.id !== id));
  }

  return (
    <div className="history-page">
      <div className="page-header">
        <div>
          <h1>Chat History</h1>
          <p>Revisit and continue past conversations</p>
        </div>
        <button className="btn-primary">
          <Plus size={16} /> New Chat
        </button>
      </div>

      <div className="history-search">
        <Search size={16} />
        <input
          type="text"
          placeholder="Search conversations..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
      </div>

      {filtered.length === 0 ? (
        <div className="history-empty">
          <MessageCircle size={22} />
          <p>No conversations found.</p>
        </div>
      ) : (
        <div className="history-list">
          {filtered.map((session) => (
            <div className="history-row" key={session.id} role="button" tabIndex={0}>
              <div className="history-icon">
                <MessageCircle size={16} />
              </div>
              <div className="history-text">
                <div className="history-title">{session.title}</div>
                <div className="history-preview">{session.preview}</div>
              </div>
              <div className="history-date">{session.date}</div>
              <button
                className="history-delete-btn"
                aria-label="Delete conversation"
                onClick={(e) => handleDelete(session.id, e)}
              >
                <Trash2 size={15} />
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}