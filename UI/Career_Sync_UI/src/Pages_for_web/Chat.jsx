import React, { useState, useRef, useEffect } from "react";
import {
  Sparkles,
  Plus,
  Paperclip,
  Globe,
  Send,
  ThumbsUp,
  ThumbsDown,
  Copy,
  Check,
  FileText,
  Map,
  User,
  Briefcase,
} from "lucide-react";
import './css_for_web/Chat.css'

const initialMessages = [
  {
    id: 1,
    role: "assistant",
    text: (
      <>
        <p>Hi Vishal! 👋</p>
        <p>I'm your Career Sync AI assistant. I can help you with:</p>
        <ul>
          <li>Career guidance and roadmaps</li>
          <li>Resume improvement tips</li>
          <li>Skill recommendations</li>
          <li>Interview preparation</li>
          <li>Job search strategies</li>
        </ul>
        <p>What would you like to know?</p>
      </>
    ),
  },
];

const suggestions = [
  { icon: FileText, iconBg: "#eeecfd", iconColor: "#5b4df0", title: "Improve my resume", subtitle: "Get tips to improve your resume" },
  { icon: Map, iconBg: "#eeecfd", iconColor: "#5b4df0", title: "Skill roadmap", subtitle: "Find a roadmap for data analyst" },
  { icon: User, iconBg: "#eeecfd", iconColor: "#5b4df0", title: "Mock interview", subtitle: "Prepare for your next interview" },
  { icon: Briefcase, iconBg: "#eeecfd", iconColor: "#5b4df0", title: "Job search tips", subtitle: "Get job search strategies" },
];

function formatTime(date) {
  return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

function ChatBubbleAssistant({ message }) {
  return (
    <div className="msg-row msg-row-assistant">
      <div className="msg-avatar">
        <Sparkles size={16} />
      </div>
      <div className="msg-bubble msg-bubble-assistant">
        {message.text}
        <div className="msg-meta">
          <span className="msg-time">{message.time}</span>
          <button className="msg-icon-btn"><Copy size={13} /></button>
          <button className="msg-icon-btn"><ThumbsUp size={13} /></button>
          <button className="msg-icon-btn"><ThumbsDown size={13} /></button>
        </div>
      </div>
    </div>
  );
}

function ChatBubbleUser({ message }) {
  return (
    <div className="msg-row msg-row-user">
      <div className="msg-bubble msg-bubble-user">
        {message.text}
        <div className="msg-meta msg-meta-user">
          <span className="msg-time">{message.time}</span>
          <Check size={13} />
        </div>
      </div>
    </div>
  );
}

export default function ChatAssistant() {
  const [messages, setMessages] = useState(initialMessages);
  const [input, setInput] = useState("");
  const scrollRef = useRef(null);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  function sendMessage(text) {
    const trimmed = text.trim();
    if (!trimmed) return;

    const userMsg = {
      id: Date.now(),
      role: "user",
      text: trimmed,
      time: formatTime(new Date()),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput("");

    // Placeholder assistant reply — swap this for your real API call
    setTimeout(() => {
      const reply = {
        id: Date.now() + 1,
        role: "assistant",
        text: "Got it — let me look into that for you.",
        time: formatTime(new Date()),
      };
      setMessages((prev) => [...prev, reply]);
    }, 600);
  }

  function handleSubmit(e) {
    e.preventDefault();
    sendMessage(input);
  }

  function handleNewChat() {
    setMessages(initialMessages);
    setInput("");
  }

  const showSuggestions = messages.length === initialMessages.length;

  return (
    <main className="chat-page">
      <div className="chat-header">
        <div className="chat-header-left">
          <div className="chat-header-icon">
            <Sparkles size={18} />
          </div>
          <div>
            <h1 className="chat-title">Chat Assistant</h1>
            <p className="chat-subtitle">Your AI career guide</p>
          </div>
        </div>
        <button className="new-chat-btn" onClick={handleNewChat}>
          <Plus size={15} /> New Chat
        </button>
      </div>

      <div className="chat-thread">
        {messages.map((m) =>
          m.role === "assistant" ? (
            <ChatBubbleAssistant key={m.id} message={m} />
          ) : (
            <ChatBubbleUser key={m.id} message={m} />
          )
        )}
        <div ref={scrollRef} />
      </div>

      {showSuggestions && (
        <div className="suggestion-grid">
          {suggestions.map(({ icon: Icon, iconBg, iconColor, title, subtitle }) => (
            <button
              key={title}
              className="suggestion-card"
              onClick={() => sendMessage(title)}
            >
              <div className="suggestion-icon" style={{ background: iconBg, color: iconColor }}>
                <Icon size={16} />
              </div>
              <div>
                <div className="suggestion-title">{title}</div>
                <div className="suggestion-subtitle">{subtitle}</div>
              </div>
            </button>
          ))}
        </div>
      )}

      <form className="chat-input-bar" onSubmit={handleSubmit}>
        <input
          type="text"
          className="chat-input"
          placeholder="Message Career Sync AI..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <div className="chat-input-actions">
          <button type="button" className="chat-icon-btn"><Paperclip size={17} /></button>
          <button type="button" className="chat-icon-btn"><Globe size={17} /></button>
          <button type="submit" className="chat-send-btn" disabled={!input.trim()}>
            <Send size={16} />
          </button>
        </div>
      </form>

      <p className="chat-disclaimer">
        Career Sync AI can make mistakes. Please verify important information.
      </p>
    </main>
  );
}