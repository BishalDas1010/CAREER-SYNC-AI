import { useState, useRef, useEffect } from "react";
import { useNavigate, useLocation, Link } from "react-router-dom";
import './css_for_web/VerifyOtp.css'

import { supabase, verifyOtp, resendOtp } from "../lib/supabaseClient";

const CODE_LENGTH = 6;
const RESEND_COOLDOWN = 30; // seconds

export default function VerifyOtp() {
  const navigate = useNavigate();
  const location = useLocation();
  const email = location.state?.email || "";
  const fullName = location.state?.fullName || "";

  const [digits, setDigits] = useState(Array(CODE_LENGTH).fill(""));
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [resending, setResending] = useState(false);
  const [cooldown, setCooldown] = useState(RESEND_COOLDOWN);
  const inputRefs = useRef([]);

  useEffect(() => {
    inputRefs.current[0]?.focus();
  }, []);

  useEffect(() => {
    if (cooldown <= 0) return;
    const t = setTimeout(() => setCooldown((c) => c - 1), 1000);
    return () => clearTimeout(t);
  }, [cooldown]);

  const submitCode = async (code) => {
    setError("");
    setLoading(true);
    try {
      const data = await verifyOtp(email, code);
      if (supabase && data.access_token && data.refresh_token) {
        await supabase.auth.setSession({
          access_token: data.access_token,
          refresh_token: data.refresh_token,
        });
      }
      navigate("/onboarding", { state: { email, fullName } });
    } catch (err) {
      setError(err.message || "That code didn't work. Check it and try again.");
      setDigits(Array(CODE_LENGTH).fill(""));
      inputRefs.current[0]?.focus();
    } finally {
      setLoading(false);
    }
  };

  const handleDigitChange = (index, value) => {
    const clean = value.replace(/\D/g, "");
    if (!clean) {
      const next = [...digits];
      next[index] = "";
      setDigits(next);
      return;
    }

    // handles paste of the full code into one box
    if (clean.length > 1) {
      const chars = clean.slice(0, CODE_LENGTH).split("");
      const next = Array(CODE_LENGTH).fill("");
      chars.forEach((c, i) => (next[i] = c));
      setDigits(next);
      const lastFilled = Math.min(chars.length, CODE_LENGTH) - 1;
      inputRefs.current[lastFilled]?.focus();
      if (chars.length === CODE_LENGTH) submitCode(chars.join(""));
      return;
    }

    const next = [...digits];
    next[index] = clean;
    setDigits(next);

    if (index < CODE_LENGTH - 1) {
      inputRefs.current[index + 1]?.focus();
    } else if (next.every((d) => d !== "")) {
      submitCode(next.join(""));
    }
  };

  const handleKeyDown = (index, e) => {
    if (e.key === "Backspace" && !digits[index] && index > 0) {
      inputRefs.current[index - 1]?.focus();
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const code = digits.join("");
    if (code.length === CODE_LENGTH) submitCode(code);
  };

  const handleResend = async () => {
    setError("");
    setResending(true);
    try {
      await resendOtp(email);
      setCooldown(RESEND_COOLDOWN);
      setDigits(Array(CODE_LENGTH).fill(""));
      inputRefs.current[0]?.focus();
    } catch (err) {
      setError(err.message || "Could not resend the code.");
    } finally {
      setResending(false);
    }
  };

  if (!email) {
    return (
      <div className="verify-page">
        <div className="verify-card">
          <h1 className="card-title">We lost track of that email</h1>
          <p className="card-subtitle">
            Head back and register again so we know where to send your code.
          </p>
          <Link to="/register" className="btn-primary verify-back-link">
            Back to Register →
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="verify-page">
      <header className="verify-nav">
        <div className="nav-logo">
          <span className="nav-logo-mark">✦</span>
          <span className="nav-logo-text">
            Career Sync <span className="accent">AI</span>
          </span>
        </div>
        <Link to="/" className="back-home-link">
          Back to home
        </Link>
      </header>

      <main className="verify-main">
        <div className="verify-card">
          <span className="verify-icon" aria-hidden="true">✉️</span>
          <h1 className="card-title">Check your email</h1>
          <p className="card-subtitle">
            Enter the 6-digit code we sent to <strong>{email}</strong>
          </p>

          <form onSubmit={handleSubmit} className="otp-form">
            <div className="otp-boxes" role="group" aria-label="6-digit verification code">
              {digits.map((digit, i) => (
                <input
                  key={i}
                  ref={(el) => (inputRefs.current[i] = el)}
                  type="text"
                  inputMode="numeric"
                  autoComplete={i === 0 ? "one-time-code" : "off"}
                  maxLength={CODE_LENGTH}
                  className={`otp-box ${error ? "otp-box-error" : ""}`}
                  value={digit}
                  onChange={(e) => handleDigitChange(i, e.target.value)}
                  onKeyDown={(e) => handleKeyDown(i, e)}
                  disabled={loading}
                />
              ))}
            </div>

            {error && (
              <p className="inline-error" role="alert">{error}</p>
            )}

            <button
              type="submit"
              className="btn-primary verify-submit"
              disabled={loading || digits.some((d) => !d)}
            >
              {loading ? "Verifying…" : "Verify email →"}
            </button>
          </form>

          <p className="verify-resend">
            Didn't get it?{" "}
            <button
              type="button"
              className="resend-link"
              onClick={handleResend}
              disabled={resending || cooldown > 0}
            >
              {resending
                ? "Sending…"
                : cooldown > 0
                ? `Resend in ${cooldown}s`
                : "Resend code"}
            </button>
          </p>
        </div>
      </main>

      <footer className="verify-footer">
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