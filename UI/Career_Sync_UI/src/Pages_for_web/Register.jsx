import { useState, useEffect } from "react";
import { useNavigate, useLocation, Link } from "react-router-dom";
import "./css_for_web/Register.css";

export default function Register() {
  const navigate = useNavigate();
  const location = useLocation();

  const [formData, setFormData] = useState({
    fullName: "",
    email: location.state?.prefillEmail || "",
    password: "",
    confirmPassword: "",
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [agreedToTerms, setAgreedToTerms] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const [theme, setTheme] = useState(() => {
    if (typeof window === "undefined") return "light";
    const saved = localStorage.getItem("theme");
    if (saved) return saved;
    return window.matchMedia("(prefers-color-scheme: dark)").matches
      ? "dark"
      : "light";
  });

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);
  }, [theme]);

  const toggleTheme = () => setTheme((t) => (t === "light" ? "dark" : "light"));

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    if (error) setError(null);
  };

  const validate = () => {
    if (!formData.fullName.trim()) return "Please enter your full name.";
    if (!formData.email.trim()) return "Please enter your email.";
    if (formData.password.length < 8)
      return "Password must be at least 8 characters.";
    if (formData.password !== formData.confirmPassword)
      return "Passwords do not match.";
    if (!agreedToTerms) return "Please agree to the Terms & Conditions.";
    return null;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const validationError = validate();
    if (validationError) {
      setError({ type: "generic", message: validationError });
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const res = await fetch("/api/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          fullName: formData.fullName,
          email: formData.email,
          password: formData.password,
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        if (res.status === 409 || data.code === "EMAIL_EXISTS") {
          setError({
            type: "exists",
            message: "An account with this email already exists.",
          });
        } else {
          setError({
            type: "generic",
            message: data.message || "Something went wrong. Please try again.",
          });
        }
        setLoading(false);
        return;
      }

      if (data.token) localStorage.setItem("token", data.token);
      navigate("/onboarding", { state: { email: formData.email } });
    } catch (err) {
      setError({
        type: "generic",
        message: "Network error. Please check your connection and try again.",
      });
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      {/* Top nav */}
      <header className="login-nav">
        <div className="nav-logo">
          <span className="nav-logo-mark">✦</span>
          <span className="nav-logo-text">
            Career Sync <span className="accent">AI</span>
          </span>
        </div>
        <div className="nav-right">
          <button
            className="theme-toggle"
            onClick={toggleTheme}
            aria-label="Toggle dark mode"
            type="button"
          >
            {theme === "light" ? "🌙" : "☀️"}
          </button>
          <Link to="/" className="back-home-link">
            Back to home
          </Link>
        </div>
      </header>

      {/* Main split layout */}
      <main className="login-main">
        <section className="login-copy">
          <span className="welcome-pill">✦ Start your journey</span>
          <h1 className="copy-heading">
            Your career glow-up <span className="accent">starts here.</span>
          </h1>
          <p className="copy-subtext">
            Upload your resume, uncover skill gaps, and get a personalized
            roadmap built around where you want to go.
          </p>
          <ul className="copy-checklist">
            <li>
              <span className="check-icon">✓</span>
              Get your Career Score in under a minute
            </li>
            <li>
              <span className="check-icon">✓</span>
              See exactly which skills to close the gap on
            </li>
            <li>
              <span className="check-icon">✓</span>
              Unlock job matches tailored to your profile
            </li>
          </ul>
        </section>

        <section className="login-card-wrapper">
          <div className="login-card">
            <h2 className="card-title">Create Your Account ✨</h2>
            <p className="card-subtitle">Start your career transformation today</p>

            <form onSubmit={handleSubmit} className="login-form" noValidate>
              <label className="field-label" htmlFor="fullName">
                Full Name
              </label>
              <div className="input-with-icon">
                <span className="input-icon">👤</span>
                <input
                  id="fullName"
                  name="fullName"
                  type="text"
                  placeholder="John Doe"
                  className="field-input"
                  value={formData.fullName}
                  onChange={handleChange}
                  required
                />
              </div>

              <label className="field-label" htmlFor="email">
                Email Address
              </label>
              <div className="input-with-icon">
                <span className="input-icon">✉️</span>
                <input
                  id="email"
                  name="email"
                  type="email"
                  placeholder="you@example.com"
                  className={`field-input ${
                    error?.type === "exists" ? "field-error" : ""
                  }`}
                  value={formData.email}
                  onChange={handleChange}
                  required
                />
              </div>

              {error?.type === "exists" && (
                <div className="caution-banner" role="alert">
                  <span className="caution-icon">⚠️</span>
                  <div className="caution-text">
                    <span>{error.message}</span>
                    <Link to="/login" className="caution-link">
                      Log in instead →
                    </Link>
                  </div>
                </div>
              )}

              <label className="field-label" htmlFor="password">
                Password
              </label>
              <div className="input-with-icon">
                <span className="input-icon">🔒</span>
                <input
                  id="password"
                  name="password"
                  type={showPassword ? "text" : "password"}
                  placeholder="Create a password"
                  className="field-input"
                  value={formData.password}
                  onChange={handleChange}
                  required
                />
                <button
                  type="button"
                  className="password-toggle"
                  onClick={() => setShowPassword((s) => !s)}
                  aria-label={showPassword ? "Hide password" : "Show password"}
                >
                  {showPassword ? "🙈" : "👁️"}
                </button>
              </div>

              <label className="field-label" htmlFor="confirmPassword">
                Confirm Password
              </label>
              <div className="input-with-icon">
                <span className="input-icon">🔒</span>
                <input
                  id="confirmPassword"
                  name="confirmPassword"
                  type={showConfirmPassword ? "text" : "password"}
                  placeholder="Confirm your password"
                  className="field-input"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  required
                />
                <button
                  type="button"
                  className="password-toggle"
                  onClick={() => setShowConfirmPassword((s) => !s)}
                  aria-label={
                    showConfirmPassword ? "Hide password" : "Show password"
                  }
                >
                  {showConfirmPassword ? "🙈" : "👁️"}
                </button>
              </div>

              {error?.type === "generic" && (
                <p className="inline-error">{error.message}</p>
              )}

              <label className="checkbox-label terms-row">
                <input
                  type="checkbox"
                  checked={agreedToTerms}
                  onChange={(e) => setAgreedToTerms(e.target.checked)}
                />
                <span>
                  I agree to the <Link to="/terms">Terms &amp; Conditions</Link>
                </span>
              </label>

              <button type="submit" className="btn-primary" disabled={loading}>
                {loading ? "Creating account..." : "Create Account →"}
              </button>

              <div className="divider">
                <span>or continue with</span>
              </div>

              <div className="oauth-row">
                <button type="button" className="btn-oauth">
                  <span className="oauth-icon">G</span> Google
                </button>
                <button type="button" className="btn-oauth">
                  <span className="oauth-icon">⌥</span> GitHub
                </button>
              </div>

              <p className="card-footer">
                Already have an account?{" "}
                <Link to="/login" className="accent-link">
                  Login
                </Link>
              </p>
            </form>
          </div>
        </section>
      </main>

      {/* Trust footer */}
      <footer className="login-footer">
        <span className="footer-icon">🛡️</span>
        <div>
          <p className="footer-title">Your data is secure with us.</p>
          <p className="footer-subtext">
            We use industry-standard encryption to protect your information.
          </p>
        </div>
      </footer>
    </div>
  );
}