import { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import './css_for_web/Onboarding.css'


import { supabase } from "../lib/supabaseClient"

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000"




const TOTAL_STEPS = 4;

const ROLE_OPTIONS = [
  "Student",
  "Software Engineer",
  "Data Analyst",
  "Product Manager",
  "Designer",
  "Other",
];

const EDUCATION_OPTIONS = [
  "High School",
  "Bachelor's Degree",
  "Master's Degree",
  "PhD",
  "Other",
];

const EXPERIENCE_OPTIONS = [
  "No experience yet",
  "0–1 years",
  "1–3 years",
  "3–5 years",
  "5+ years",
];

export default function Onboarding() {
  const navigate = useNavigate();
  const location = useLocation();

  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    currentRole: "",
    education: "",
    experience: "",
    careerGoals: "",
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

const handleNext = async (e) => {
  e.preventDefault();

  if (step < TOTAL_STEPS) {
    setStep(step + 1);
    return;
  }

  try {
    const { data: sessionData } = await supabase.auth.getSession();
    const accessToken = sessionData?.session?.access_token;

    await fetch(`${API_BASE}/api/profile`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...(accessToken ? { Authorization: `Bearer ${accessToken}` } : {}),
      },
      body: JSON.stringify({
        full_name: location.state?.email?.split("@")[0] ?? "",
        current_role: formData.currentRole,
        education: formData.education,
        experience: formData.experience,
        career_goals: formData.careerGoals,
      }),
    });
  } catch (err) {
    console.error("Onboarding save failed:", err);
  }

  navigate("/dashboard");
};

  const handleBack = () => {
    if (step > 1) setStep(step - 1);
    else navigate(-1);
  };

  const isStepValid = () => {
    if (step === 1) return formData.currentRole !== "";
    if (step === 2) return formData.education !== "";
    if (step === 3) return formData.experience !== "";
    if (step === 4) return formData.careerGoals.trim() !== "";
    return false;
  };

  return (
    <div className="onboarding-page">
      <div className="onboarding-card">
        <div className="onboarding-header">
          <button className="back-btn" onClick={handleBack} type="button">
            ← Back
          </button>

          <div className="step-progress">
            <span className="step-label">
              Step {step} of {TOTAL_STEPS}
            </span>
            <div className="step-dots">
              {Array.from({ length: TOTAL_STEPS }).map((_, i) => (
                <span
                  key={i}
                  className={`step-dot ${i < step ? "step-dot-active" : ""}`}
                />
              ))}
            </div>
          </div>

          <button className="help-btn" type="button" aria-label="Help">
            ?
          </button>
        </div>

        <h1 className="onboarding-title">Let's get to know you</h1>
        <p className="onboarding-subtitle">
          This will help us personalize your experience
        </p>

        <form onSubmit={handleNext} className="onboarding-form">
          {step === 1 && (
            <div className="form-group">
              <label className="field-label" htmlFor="currentRole">
                What is your current role?
              </label>
              <select
                id="currentRole"
                name="currentRole"
                className="field-select"
                value={formData.currentRole}
                onChange={handleChange}
              >
                <option value="">Select your current role</option>
                {ROLE_OPTIONS.map((role) => (
                  <option key={role} value={role}>
                    {role}
                  </option>
                ))}
              </select>
            </div>
          )}

          {step === 2 && (
            <div className="form-group">
              <label className="field-label" htmlFor="education">
                What is your highest education?
              </label>
              <select
                id="education"
                name="education"
                className="field-select"
                value={formData.education}
                onChange={handleChange}
              >
                <option value="">Select your education</option>
                {EDUCATION_OPTIONS.map((edu) => (
                  <option key={edu} value={edu}>
                    {edu}
                  </option>
                ))}
              </select>
            </div>
          )}

          {step === 3 && (
            <div className="form-group">
              <label className="field-label" htmlFor="experience">
                Years of experience
              </label>
              <select
                id="experience"
                name="experience"
                className="field-select"
                value={formData.experience}
                onChange={handleChange}
              >
                <option value="">Select experience</option>
                {EXPERIENCE_OPTIONS.map((exp) => (
                  <option key={exp} value={exp}>
                    {exp}
                  </option>
                ))}
              </select>
            </div>
          )}

          {step === 4 && (
            <div className="form-group">
              <label className="field-label" htmlFor="careerGoals">
                What are your primary career goals?
              </label>
              <textarea
                id="careerGoals"
                name="careerGoals"
                className="field-textarea"
                placeholder="e.g. Get a software engineering job, switch to data science..."
                rows={4}
                value={formData.careerGoals}
                onChange={handleChange}
              />
            </div>
          )}

          <button
            type="submit"
            className="btn-primary onboarding-next"
            disabled={!isStepValid()}
          >
            {step === TOTAL_STEPS ? "Finish" : "Next"} →
          </button>
        </form>
      </div>
    </div>
  );
}