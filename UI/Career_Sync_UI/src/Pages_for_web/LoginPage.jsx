import React, { useState } from 'react'
import './css_for_web/LoginPage.css'
import { Link, useNavigate } from 'react-router-dom'
const IconMail = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
    <rect x="2" y="4" width="20" height="16" rx="2" />
    <path d="m2 7 10 6 10-6" />
  </svg>
)

const IconLock = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
    <rect x="4" y="10" width="16" height="10" rx="2" />
    <path d="M8 10V7a4 4 0 0 1 8 0v3" />
  </svg>
)

const IconEye = ({ off }) => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
    {off ? (
      <>
        <path d="M3 3l18 18" />
        <path d="M10.6 10.6a2 2 0 0 0 2.8 2.8" />
        <path d="M9.4 5.5A10.9 10.9 0 0 1 12 5c6 0 10 7 10 7a17.6 17.6 0 0 1-3.2 4" />
        <path d="M6.6 6.6C4 8.3 2 12 2 12s4 7 10 7a10 10 0 0 0 3.4-.6" />
      </>
    ) : (
      <>
        <path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7-10-7-10-7Z" />
        <circle cx="12" cy="12" r="3" />
      </>
    )}
  </svg>
)

const IconGoogle = () => (
  <svg width="18" height="18" viewBox="0 0 24 24">
    <path fill="#EA4335" d="M12 10.2v3.9h5.5c-.24 1.4-1.7 4.1-5.5 4.1-3.3 0-6-2.7-6-6.2s2.7-6.2 6-6.2c1.9 0 3.1.8 3.9 1.5l2.6-2.5C16.9 3 14.7 2 12 2 6.9 2 2.8 6.1 2.8 11.2S6.9 20.4 12 20.4c6.9 0 9.6-4.8 9.6-7.3 0-.5 0-.9-.1-1.3H12Z" />
  </svg>
)

const IconGithub = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
    <path d="M12 2a10 10 0 0 0-3.16 19.49c.5.09.68-.22.68-.48v-1.7c-2.78.6-3.37-1.34-3.37-1.34-.46-1.16-1.11-1.47-1.11-1.47-.9-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.9 1.52 2.34 1.08 2.91.83.09-.65.35-1.08.63-1.33-2.22-.25-4.56-1.11-4.56-4.95 0-1.09.39-1.98 1.03-2.68-.1-.26-.45-1.29.1-2.68 0 0 .84-.27 2.75 1.02a9.6 9.6 0 0 1 5 0c1.9-1.29 2.75-1.02 2.75-1.02.55 1.39.2 2.42.1 2.68.64.7 1.03 1.59 1.03 2.68 0 3.85-2.34 4.7-4.57 4.94.36.31.68.92.68 1.85v2.75c0 .27.18.58.69.48A10 10 0 0 0 12 2Z" />
  </svg>
)

const IconShield = () => (
  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
    <path d="M12 2 4 5v6c0 5 3.5 8.5 8 11 4.5-2.5 8-6 8-11V5l-8-3Z" />
  </svg>
)

export default function LoginPage() {
  const [showPassword, setShowPassword] = useState(false)
  const [form, setForm] = useState({ email: '', password: '' })

  const handleChange = (e) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }))
  }

const handleSubmit = async (e) => {
  e.preventDefault()

  try {
    const response = await fetch("http://localhost:8000/api/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: form.email,
        password: form.password,
      }),
    })

    const data = await response.json()

    if (!response.ok) {
      console.error("Login failed:", data)
      return
    }

    console.log("Login successful:", data)
    navigate("/dashboard", {
  state: {
    username: data.email
  }
  })
  } catch (error) {
    console.error("Cannot connect to FastAPI:", error)
  }
}

  return (
    <div className="login">
      <header className="login__nav">
        <Link to="/" className="brand">
          <span className="brand__mark" aria-hidden="true">
            <svg viewBox="0 0 24 24" width="22" height="22" fill="none">
              <path d="M12 2 L14.5 9.2 L22 12 L14.5 14.8 L12 22 L9.5 14.8 L2 12 L9.5 9.2 Z" fill="currentColor" />
            </svg>
          </span>
          <span className="brand__name">Career Sync <span className="brand__accent">AI</span></span>
        </Link>
        <Link to="/" className="link-muted">Back to home</Link>
      </header>

      <main className="login__main">
        <div className="login__intro">
          <span className="eyebrow">
            <span className="eyebrow__arrow" aria-hidden="true">&larr;</span>
            Welcome back
          </span>
          <h1 className="login__headline">
            Pick up right where
            <br />
            you <span className="login__accent">left off.</span>
          </h1>
          <p className="login__subtext">
            Your resume score, skill gaps, and personalized roadmap are exactly
            where you left them.
          </p>

          <ul className="login__points">
            <li>Track your Career Score over time</li>
            <li>Get matched to new roles as your profile grows</li>
            <li>Pick up your learning roadmap where you paused</li>
          </ul>
        </div>

        <div className="login__card">
          <h2 className="login__cardTitle">Welcome Back <span aria-hidden="true">👋</span></h2>
          <p className="login__cardSub">Login to continue your journey</p>

          <form onSubmit={handleSubmit} noValidate>
            <label className="login__label" htmlFor="email">Email Address</label>
            <div className="login__inputWrap">
              <span className="login__inputIcon"><IconMail /></span>
              <input
                id="email"
                name="email"
                type="email"
                placeholder="Enter your email"
                value={form.email}
                onChange={handleChange}
                autoComplete="email"
              />
            </div>

            <label className="login__label" htmlFor="password">Password</label>
            <div className="login__inputWrap">
              <span className="login__inputIcon"><IconLock /></span>
              <input
                id="password"
                name="password"
                type={showPassword ? 'text' : 'password'}
                placeholder="Enter your password"
                value={form.password}
                onChange={handleChange}
                autoComplete="current-password"
              />
              <button
                type="button"
                className="login__eyeBtn"
                onClick={() => setShowPassword((s) => !s)}
                aria-label={showPassword ? 'Hide password' : 'Show password'}
              >
                <IconEye off={showPassword} />
              </button>
            </div>

            <div className="login__forgotRow">
              <a href="#forgot" className="login__link">Forgot Password?</a>
            </div>

            <button type="submit" className="btn btn--primary login__submit">
              Login
              <span className="btn__arrow" aria-hidden="true">&rarr;</span>
            </button>
          </form>

          <div className="login__divider"><span>or continue with</span></div>

          <div className="login__oauthRow">
            <button type="button" className="login__oauthBtn">
              <IconGoogle />
              Google
            </button>
            <button type="button" className="login__oauthBtn">
              <IconGithub />
              GitHub
            </button>
          </div>

          <p className="login__register">
            Don't have an account? <Link to="/register">Register</Link>
          </p>
        </div>
      </main>

      <footer className="login__footer">
        <span className="login__footerIcon"><IconShield /></span>
        <div>
          <p>Your data is secure with us.</p>
          <p className="login__footerSub">We use industry-standard encryption to protect your information.</p>
        </div>
      </footer>
    </div>
  )
}