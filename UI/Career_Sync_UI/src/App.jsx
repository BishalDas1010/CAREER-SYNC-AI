import React from 'react'
import './index.css'

const avatars = [
  'https://i.pravatar.cc/64?img=32',
  'https://i.pravatar.cc/64?img=47',
  'https://i.pravatar.cc/64?img=12',
]

const logos = ['Google', 'Microsoft', 'amazon', 'TATA', 'Infosys', 'Deloitte']

function NavBar() {
  return (
    <header className="navbar">
      <div className="navbar__inner">
        
        <div className="brand">
          <span className="brand__mark" aria-hidden="true">
            <svg viewBox="0 0 24 24" width="22" height="22" fill="none">
             <path d="M12 2 L14.5 9.2 L22 12 L14.5 14.8 L12 22 L9.5 14.8 L2 12 L9.5 9.2 Z" fill="currentColor" />

            </svg>
          </span>
          <span className="brand__name">Career Sync <span className="brand__accent">AI</span></span>
        </div>

        <nav className="navlinks" aria-label="Primary">
          <a href="#features">Features</a>
          <a href="#how-it-works">How it Works</a>
          <a href="#pricing">Pricing</a>
          <a href="#about">About</a>
        </nav>

        <div className="navactions">
          <a href="#login" className="link-muted">Login</a>
          <a href="#get-started" className="btn btn--primary btn--sm">Get Started Free</a>
        </div>
      </div>
    </header>
  )
}

function ScoreCard() {
  return (
    <div className="float-card float-card--score" role="img" aria-label="Resume score card showing 78 out of 100, Good">
      <div className="score-card__label">Your Career Score</div>
      <div className="score-card__value">
        <span className="score-card__num">78</span>
        <span className="score-card__max">/100</span>
      </div>
      <div className="score-card__pill">
        <span className="score-card__dot" />
        Good
      </div>
      <svg className="score-card__chart" viewBox="0 0 140 46" fill="none">
        <polyline
          points="0,36 15,30 30,34 45,18 60,24 75,10 90,16 105,6 120,12 140,2"
          fill="none"
          stroke="var(--accent-500)"
          strokeWidth="2.5"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    </div>
  )
}

function SkillBarsCard() {
  const bars = [40, 65, 30, 80, 55, 70, 45]
  return (
    <div className="float-card float-card--bars" aria-hidden="true">
      <div className="bars-card__row">
        {bars.map((h, i) => (
          <span key={i} className="bars-card__bar" style={{ height: `${h}%` }} />
        ))}
      </div>
      <div className="bars-card__lines">
        <span />
        <span />
        <span />
      </div>
    </div>
  )
}

function BadgeCards() {
  return (
    <>
      <div className="float-card float-card--badge float-card--badge-top" aria-hidden="true">
        <svg viewBox="0 0 24 24" width="18" height="18" fill="none">
          <path d="M12 2l2.6 6.6L22 9.3l-5 4.9 1.2 7-6.2-3.6L5.8 21.2 7 14.2 2 9.3l7.4-.7L12 2z" fill="var(--accent-500)" />
        </svg>
      </div>
      <div className="float-card float-card--badge float-card--badge-bottom" aria-hidden="true">
        <svg viewBox="0 0 24 24" width="18" height="18" fill="none">
          <circle cx="12" cy="12" r="9" stroke="var(--accent-500)" strokeWidth="2" />
          <path d="M8 12.5l2.5 2.5L16 9.5" stroke="var(--accent-500)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      </div>
    </>
  )
}

function HeroVisual() {
  return (
    <div className="hero-visual" aria-hidden="true">
      <div className="hero-visual__glow" />
      <div className="hero-visual__panel">
        <div className="hero-visual__panel-row">
          <span className="hero-visual__chip" />
          <span className="hero-visual__chip hero-visual__chip--wide" />
        </div>
        <div className="hero-visual__panel-block" />
        <div className="hero-visual__panel-row hero-visual__panel-row--tight">
          <span className="hero-visual__chip hero-visual__chip--sm" />
          <span className="hero-visual__chip hero-visual__chip--sm" />
          <span className="hero-visual__chip hero-visual__chip--sm" />
        </div>
      </div>
      <ScoreCard />
      <SkillBarsCard />
      <BadgeCards />
    </div>
  )
}

function Hero() {
  return (
    <section className="hero">
      <div className="hero__inner">
        <div className="hero__content">
          <a href="#product" className="eyebrow">
            <span className="eyebrow__arrow" aria-hidden="true">&larr;</span>
            AI-Powered Career Assistant
          </a>

          <h1 className="headline">
            Sync Your Skills.
            <br />
            Accelerate Your <span className="headline__accent">Career.</span>
          </h1>

          <p className="subtext">
            Upload your resume, analyze skill gaps, and get a personalized roadmap to discover the right job opportunities for you.
          </p>

          <div className="hero__actions">
            <a href="#get-started" className="btn btn--primary">
              Get Started Free
              <span className="btn__arrow" aria-hidden="true">&rarr;</span>
            </a>
            <a href="#demo" className="btn btn--ghost">
              <span className="btn__play" aria-hidden="true">
                <svg viewBox="0 0 24 24" width="12" height="12" fill="currentColor">
                  <path d="M6 4l14 8-14 8V4z" />
                </svg>
              </span>
              See How It Works
            </a>
          </div>

          <div className="social-proof">
            <div className="avatar-stack" aria-hidden="true">
              {avatars.map((src, i) => (
                <img key={i} src={src} alt="" className="avatar-stack__img" />
              ))}
            </div>
            <div className="social-proof__text">
              <div className="social-proof__users">Trusted by 2,000+ users</div>
              <div className="social-proof__rating">
                <span className="stars" aria-hidden="true">★★★★★</span>
                4.8/5 average rating
              </div>
            </div>
          </div>
        </div>

        <HeroVisual />
      </div>

      <div className="logo-strip">
        {logos.map((logo) => (
          <span key={logo} className="logo-strip__item">{logo}</span>
        ))}
      </div>
    </section>
  )
}

const problems = [
  {
    title: 'Resumes vanish into ATS filters',
    body: 'Most applications never reach a human. Formatting and keyword mismatches get you auto-rejected before anyone reads a word.',
  },
  {
    title: "You can't see your own gaps",
    body: "It's hard to know which skills are actually missing for the role you want, so you keep applying blind and hoping.",
  },
  {
    title: 'No clear next step',
    body: 'Generic advice like "learn more skills" isn\'t a plan. Without a sequence to follow, progress stalls.',
  },
]

function ProblemSection() {
  return (
    <section className="section section--tint" id="problem">
      <div className="section__inner">
        <div className="section__head">
          <span className="eyebrow eyebrow--static">The Problem</span>
          <h2 className="section__title">Job hunting shouldn't feel like guesswork</h2>
          <p className="section__subtext">
            Talented candidates get filtered out for reasons that have nothing to do with their ability. We built Career Sync AI to fix that.
          </p>
        </div>

        <div className="problem-grid">
          {problems.map((p) => (
            <div className="problem-card" key={p.title}>
              <span className="problem-card__mark" aria-hidden="true" />
              <h3 className="problem-card__title">{p.title}</h3>
              <p className="problem-card__body">{p.body}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

const steps = [
  {
    n: '01',
    title: 'Upload your resume',
    body: 'Drop in your resume and the target role. Our AI reads both in seconds, no formatting required.',
  },
  {
    n: '02',
    title: 'We analyze the gap',
    body: 'A retrieval-based engine compares your resume against real job requirements and scores where you stand.',
  },
  {
    n: '03',
    title: 'Get a personalized roadmap',
    body: 'See exactly which skills to build next, in what order, with resources matched to your current level.',
  },
  {
    n: '04',
    title: 'Discover matching roles',
    body: 'As your profile strengthens, we surface roles you\'re genuinely qualified for, not just keyword matches.',
  },
]

function HowItWorksSection() {
  return (
    <section className="section" id="how-it-works">
      <div className="section__inner">
        <div className="section__head">
          <span className="eyebrow eyebrow--static">How It Works</span>
          <h2 className="section__title">From resume to roadmap in four steps</h2>
          <p className="section__subtext">
            Each step feeds the next, so you always know what to do and why it matters.
          </p>
        </div>

        <div className="steps">
          {steps.map((s, i) => (
            <div className="step" key={s.n}>
              <div className="step__marker">
                <span className="step__num">{s.n}</span>
                {i < steps.length - 1 && <span className="step__line" aria-hidden="true" />}
              </div>
              <div className="step__content">
                <h3 className="step__title">{s.title}</h3>
                <p className="step__body">{s.body}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

function MissionSection() {
  return (
    <section className="section section--dark" id="about">
      <div className="section__inner mission">
        <span className="eyebrow eyebrow--onDark">Our Mission</span>
        <p className="mission__statement">
          We believe your next job should depend on <span className="mission__accent">what you can do</span>,
          not on whether a keyword scanner happened to like your resume.
        </p>
        <p className="mission__body">
          Career Sync AI exists to close the gap between where you are and where the market needs you to be, with
          honest scoring, a concrete plan, and no guesswork in between.
        </p>

        <div className="mission__stats">
          <div className="mission__stat">
            <span className="mission__stat-num">2,000+</span>
            <span className="mission__stat-label">Resumes analyzed</span>
          </div>
          <div className="mission__stat">
            <span className="mission__stat-num">4.8/5</span>
            <span className="mission__stat-label">Average rating</span>
          </div>
          <div className="mission__stat">
            <span className="mission__stat-num">78%</span>
            <span className="mission__stat-label">Avg. score improvement</span>
          </div>
        </div>
      </div>
    </section>
  )
}

export default function App() {
  return (
    <div className="page">
      <NavBar />
      <Hero />
      <ProblemSection />
      <HowItWorksSection />
      <MissionSection />
    </div>
  )
}