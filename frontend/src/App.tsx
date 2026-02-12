// src/App.tsx
import { useState } from "react";
import "./App.css";

const API_BASE_URL = "http://127.0.0.1:8000"; // backend fastapi url

type RiskLabel = "Low" | "Moderate" | "High";

interface PredictionBlock {
  risk_label: RiskLabel;
  confidence: string;
  confidence_score: number;
}

interface RiskDriversBlock {
  primary: string;
  high_domains: string[];
  moderate_domains: string[];
}

interface RiskIndicesBlock {
  posture_risk_index: number;
  visual_strain_index: number;
  cognitive_load_index: number;
  msk_risk_index: number;
  lifestyle_risk_index: number;
  overall_risk_index: number;
}

interface ModelProbabilitiesBlock {
  low: number;
  moderate: number;
  high: number;
}

interface ReportResponse {
  prediction: PredictionBlock;
  risk_drivers: RiskDriversBlock;
  risk_indices: RiskIndicesBlock;
  model_probabilities: ModelProbabilitiesBlock;
  rag_report?: string;
}

interface FormState {
  consent: string;
  age_group: string;
  department: string;
  designation: string;
  experience_years: string;
  marital_status: string;

  teaching_hours: number;
  admin_hours: number;

  weekend_work: string;
  role_overload: number;
  publish_pressure: string;

  workspace_setup: string;
  screen_position: string;
  feet_support: string;
  sitting_duration: string;
  most_discomfort_activity: string;

  sleep_hours: string;
  physical_activity: string;
  hydration: string;
  commute_time: string;

  neck_pain: number;
  lower_back_pain: number;
  wrist_pain: number;
  shoulder_pain: number;
  leg_pain: number;
  eye_strain: number;

  who5_q1: string;
  who5_q2: string;
  who5_q3: string;
  who5_q4: string;
  who5_q5: string;
}

const initialState: FormState = {
  consent: "Yes",
  age_group: "18-25",
  department: "Computer Science / AIML",
  designation: "Student",
  experience_years: "0-1",
  marital_status: "Single",

  teaching_hours: 0,
  admin_hours: 0,

  weekend_work: "Never",
  role_overload: 3,
  publish_pressure: "No",

  workspace_setup: "Basic Chair and Table",
  screen_position: "At eye level",
  feet_support: "No",
  sitting_duration: "1 - 2 hours",
  most_discomfort_activity: "Sitting",

  sleep_hours: "6 - 7 hours",
  physical_activity: "Sedentary (No Exercise)",
  hydration: "1 - 2 litres",
  commute_time: "Less than 30 mins",

  neck_pain: 0,
  lower_back_pain: 0,
  wrist_pain: 0,
  shoulder_pain: 0,
  leg_pain: 0,
  eye_strain: 0,

  who5_q1: "Some of the time",
  who5_q2: "Some of the time",
  who5_q3: "Some of the time",
  who5_q4: "Some of the time",
  who5_q5: "Some of the time",
};

export default function App() {
  const [form, setForm] = useState<FormState>(initialState);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>("");
  const [response, setResponse] = useState<ReportResponse | null>(null);

  function updateField<K extends keyof FormState>(key: K, value: FormState[K]) {
    setForm((prev) => ({ ...prev, [key]: value }));
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setResponse(null);
    setLoading(true);

    try {
      const payload = form;

      const res = await fetch(`${API_BASE_URL}/predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        const text = await res.text();
        throw new Error(`API Error ${res.status}: ${text}`);
      }

      const data: ReportResponse = await res.json();
      setResponse(data);
      
      // Scroll to results
      setTimeout(() => {
        document.getElementById('results')?.scrollIntoView({ 
          behavior: 'smooth', 
          block: 'start' 
        });
      }, 100);
    } catch (err) {
      if (err instanceof Error) setError(err.message);
      else setError("Unknown error occurred.");
    } finally {
      setLoading(false);
    }
  }

  const getRiskColor = (label: RiskLabel) => {
    switch(label) {
      case "Low": return "var(--success)";
      case "Moderate": return "var(--warning)";
      case "High": return "var(--danger)";
      default: return "var(--text-secondary)";
    }
  };

  return (
    <div className="app">
      {/* Hero Section */}
      <div className="hero">
        <div className="hero-content">
          <div className="logo-badge">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" strokeWidth="2" strokeLinejoin="round"/>
              <path d="M2 17L12 22L22 17" stroke="currentColor" strokeWidth="2" strokeLinejoin="round"/>
              <path d="M2 12L12 17L22 12" stroke="currentColor" strokeWidth="2" strokeLinejoin="round"/>
            </svg>
            <span>ErgoCare AI</span>
          </div>
          <h1 className="hero-title">
            Workplace Health
            <span className="gradient-text">Risk Assessment</span>
          </h1>
          <p className="hero-subtitle">
            Advanced ergonomic analysis powered by machine learning to predict and prevent workplace health risks
          </p>
        </div>
        <div className="hero-pattern"></div>
      </div>

      <div className="container">
        <form className="assessment-form" onSubmit={handleSubmit}>
          {/* CONSENT */}
          <section className="form-section">
            <div className="section-header">
              <div className="section-number">01</div>
              <div>
                <h2 className="section-title">Consent & Agreement</h2>
                <p className="section-description">Please confirm your consent to participate</p>
              </div>
            </div>

            <div className="form-grid-1">
              <div className="input-group">
                <label className="input-label">I consent to this assessment</label>
                <select
                  className="input-field"
                  value={form.consent}
                  onChange={(e) => updateField("consent", e.target.value)}
                >
                  <option value="Yes">Yes, I consent</option>
                  <option value="No">No</option>
                </select>
              </div>
            </div>
          </section>

          {/* PERSONAL INFO */}
          <section className="form-section">
            <div className="section-header">
              <div className="section-number">02</div>
              <div>
                <h2 className="section-title">Personal Details</h2>
                <p className="section-description">Basic demographic information</p>
              </div>
            </div>

            <div className="form-grid-2">
              <div className="input-group">
                <label className="input-label">Age Group</label>
                <select
                  className="input-field"
                  value={form.age_group}
                  onChange={(e) => updateField("age_group", e.target.value)}
                >
                  <option value="18-25">18-25</option>
                  <option value="26-30">26-30</option>
                  <option value="31-40">31-40</option>
                  <option value="41-50">41-50</option>
                  <option value="50+">50+</option>
                </select>
              </div>

              <div className="input-group">
                <label className="input-label">Department</label>
                <input
                  type="text"
                  className="input-field"
                  value={form.department}
                  onChange={(e) => updateField("department", e.target.value)}
                />
              </div>

              <div className="input-group">
                <label className="input-label">Designation</label>
                <select
                  className="input-field"
                  value={form.designation}
                  onChange={(e) => updateField("designation", e.target.value)}
                >
                  <option value="Student">Student</option>
                  <option value="Professor">Professor</option>
                  <option value="Assistant Professor">Assistant Professor</option>
                  <option value="Associate Professor">Associate Professor</option>
                  <option value="Researcher">Researcher</option>
                  <option value="Staff">Staff</option>
                </select>
              </div>

              <div className="input-group">
                <label className="input-label">Years of Experience</label>
                <select
                  className="input-field"
                  value={form.experience_years}
                  onChange={(e) => updateField("experience_years", e.target.value)}
                >
                  <option value="0-1">0-1 years</option>
                  <option value="2-5">2-5 years</option>
                  <option value="6-10">6-10 years</option>
                  <option value="11-15">11-15 years</option>
                  <option value="15+">15+ years</option>
                </select>
              </div>

              <div className="input-group">
                <label className="input-label">Marital Status</label>
                <select
                  className="input-field"
                  value={form.marital_status}
                  onChange={(e) => updateField("marital_status", e.target.value)}
                >
                  <option value="Single">Single</option>
                  <option value="Married">Married</option>
                  <option value="Other">Other</option>
                </select>
              </div>
            </div>
          </section>

          {/* WORKLOAD */}
          <section className="form-section">
            <div className="section-header">
              <div className="section-number">03</div>
              <div>
                <h2 className="section-title">Workload Assessment</h2>
                <p className="section-description">Your typical work hours and responsibilities</p>
              </div>
            </div>

            <div className="form-grid-2">
              <div className="input-group">
                <label className="input-label">Teaching Hours per Week</label>
                <input
                  type="number"
                  className="input-field"
                  min={0}
                  max={60}
                  value={form.teaching_hours}
                  onChange={(e) => updateField("teaching_hours", Number(e.target.value))}
                />
              </div>

              <div className="input-group">
                <label className="input-label">Administrative Hours per Week</label>
                <input
                  type="number"
                  className="input-field"
                  min={0}
                  max={60}
                  value={form.admin_hours}
                  onChange={(e) => updateField("admin_hours", Number(e.target.value))}
                />
              </div>

              <div className="input-group">
                <label className="input-label">Weekend Work Frequency</label>
                <select
                  className="input-field"
                  value={form.weekend_work}
                  onChange={(e) => updateField("weekend_work", e.target.value)}
                >
                  <option value="Never">Never</option>
                  <option value="Rarely">Rarely</option>
                  <option value="Sometimes">Sometimes</option>
                  <option value="Often">Often</option>
                  <option value="Always">Always</option>
                </select>
              </div>

              <div className="input-group">
                <label className="input-label">Role Overload (1-5)</label>
                <input
                  type="number"
                  className="input-field"
                  min={1}
                  max={5}
                  value={form.role_overload}
                  onChange={(e) => updateField("role_overload", Number(e.target.value))}
                />
                <span className="input-hint">1 = No overload, 5 = Severe overload</span>
              </div>

              <div className="input-group">
                <label className="input-label">Publication Pressure</label>
                <select
                  className="input-field"
                  value={form.publish_pressure}
                  onChange={(e) => updateField("publish_pressure", e.target.value)}
                >
                  <option value="No">No</option>
                  <option value="Yes">Yes</option>
                </select>
              </div>
            </div>
          </section>

          {/* WORKSPACE */}
          <section className="form-section">
            <div className="section-header">
              <div className="section-number">04</div>
              <div>
                <h2 className="section-title">Workspace Ergonomics</h2>
                <p className="section-description">Your physical work environment setup</p>
              </div>
            </div>

            <div className="form-grid-2">
              <div className="input-group">
                <label className="input-label">Workspace Setup Type</label>
                <select
                  className="input-field"
                  value={form.workspace_setup}
                  onChange={(e) => updateField("workspace_setup", e.target.value)}
                >
                  <option value="Basic Chair and Table">Basic Chair and Table</option>
                  <option value="Adjustable Chair and Setup">Adjustable Chair and Setup</option>
                  <option value="Standing Desk Setup">Standing Desk Setup</option>
                  <option value="Poor Setup">Poor Setup</option>
                </select>
              </div>

              <div className="input-group">
                <label className="input-label">Screen Position</label>
                <select
                  className="input-field"
                  value={form.screen_position}
                  onChange={(e) => updateField("screen_position", e.target.value)}
                >
                  <option value="Below eye level">Below eye level</option>
                  <option value="At eye level">At eye level</option>
                  <option value="Above eye level">Above eye level</option>
                </select>
              </div>

              <div className="input-group">
                <label className="input-label">Feet Support Available</label>
                <select
                  className="input-field"
                  value={form.feet_support}
                  onChange={(e) => updateField("feet_support", e.target.value)}
                >
                  <option value="Yes">Yes</option>
                  <option value="No">No</option>
                </select>
              </div>

              <div className="input-group">
                <label className="input-label">Continuous Sitting Duration</label>
                <select
                  className="input-field"
                  value={form.sitting_duration}
                  onChange={(e) => updateField("sitting_duration", e.target.value)}
                >
                  <option value="Less than 30 mins">Less than 30 mins</option>
                  <option value="30 mins - 1 hour">30 mins - 1 hour</option>
                  <option value="1 - 2 hours">1 - 2 hours</option>
                  <option value="More than 2 hours">More than 2 hours</option>
                </select>
              </div>

              <div className="input-group">
                <label className="input-label">Most Discomfort During</label>
                <select
                  className="input-field"
                  value={form.most_discomfort_activity}
                  onChange={(e) => updateField("most_discomfort_activity", e.target.value)}
                >
                  <option value="Sitting">Sitting</option>
                  <option value="Standing">Standing</option>
                  <option value="Walking">Walking</option>
                  <option value="Typing">Typing</option>
                </select>
              </div>
            </div>
          </section>

          {/* LIFESTYLE */}
          <section className="form-section">
            <div className="section-header">
              <div className="section-number">05</div>
              <div>
                <h2 className="section-title">Lifestyle Factors</h2>
                <p className="section-description">Daily habits and health behaviors</p>
              </div>
            </div>

            <div className="form-grid-2">
              <div className="input-group">
                <label className="input-label">Sleep Duration per Night</label>
                <select
                  className="input-field"
                  value={form.sleep_hours}
                  onChange={(e) => updateField("sleep_hours", e.target.value)}
                >
                  <option value="Less than 5 hours">Less than 5 hours</option>
                  <option value="5 - 6 hours">5 - 6 hours</option>
                  <option value="6 - 7 hours">6 - 7 hours</option>
                  <option value="7 - 8 hours">7 - 8 hours</option>
                  <option value="More than 8 hours">More than 8 hours</option>
                </select>
              </div>

              <div className="input-group">
                <label className="input-label">Physical Activity Level</label>
                <select
                  className="input-field"
                  value={form.physical_activity}
                  onChange={(e) => updateField("physical_activity", e.target.value)}
                >
                  <option value="Sedentary (No Exercise)">Sedentary (No Exercise)</option>
                  <option value="Light Activity (Walking)">Light Activity (Walking)</option>
                  <option value="Moderate Activity (Gym / Yoga)">Moderate Activity (Gym / Yoga)</option>
                  <option value="High Activity (Sports / Running)">High Activity (Sports / Running)</option>
                </select>
              </div>

              <div className="input-group">
                <label className="input-label">Daily Water Intake</label>
                <select
                  className="input-field"
                  value={form.hydration}
                  onChange={(e) => updateField("hydration", e.target.value)}
                >
                  <option value="Less than 1 litre">Less than 1 litre</option>
                  <option value="1 - 2 litres">1 - 2 litres</option>
                  <option value="More than 2 litres">More than 2 litres</option>
                </select>
              </div>

              <div className="input-group">
                <label className="input-label">Daily Commute Time</label>
                <select
                  className="input-field"
                  value={form.commute_time}
                  onChange={(e) => updateField("commute_time", e.target.value)}
                >
                  <option value="Less than 30 mins">Less than 30 mins</option>
                  <option value="30 mins - 1 hour">30 mins - 1 hour</option>
                  <option value="1 - 2 hours">1 - 2 hours</option>
                  <option value="More than 2 hours">More than 2 hours</option>
                </select>
              </div>
            </div>
          </section>

          {/* PAIN SCORES */}
          <section className="form-section">
            <div className="section-header">
              <div className="section-number">06</div>
              <div>
                <h2 className="section-title">Discomfort Assessment</h2>
                <p className="section-description">Rate your pain levels (0 = None, 5 = Severe)</p>
              </div>
            </div>

            <div className="form-grid-3">
              <div className="input-group">
                <label className="input-label">Neck Pain</label>
                <input
                  type="number"
                  className="input-field"
                  min={0}
                  max={5}
                  value={form.neck_pain}
                  onChange={(e) => updateField("neck_pain", Number(e.target.value))}
                />
              </div>

              <div className="input-group">
                <label className="input-label">Lower Back Pain</label>
                <input
                  type="number"
                  className="input-field"
                  min={0}
                  max={5}
                  value={form.lower_back_pain}
                  onChange={(e) => updateField("lower_back_pain", Number(e.target.value))}
                />
              </div>

              <div className="input-group">
                <label className="input-label">Wrist Pain</label>
                <input
                  type="number"
                  className="input-field"
                  min={0}
                  max={5}
                  value={form.wrist_pain}
                  onChange={(e) => updateField("wrist_pain", Number(e.target.value))}
                />
              </div>

              <div className="input-group">
                <label className="input-label">Shoulder Pain</label>
                <input
                  type="number"
                  className="input-field"
                  min={0}
                  max={5}
                  value={form.shoulder_pain}
                  onChange={(e) => updateField("shoulder_pain", Number(e.target.value))}
                />
              </div>

              <div className="input-group">
                <label className="input-label">Leg Pain</label>
                <input
                  type="number"
                  className="input-field"
                  min={0}
                  max={5}
                  value={form.leg_pain}
                  onChange={(e) => updateField("leg_pain", Number(e.target.value))}
                />
              </div>

              <div className="input-group">
                <label className="input-label">Eye Strain</label>
                <input
                  type="number"
                  className="input-field"
                  min={0}
                  max={5}
                  value={form.eye_strain}
                  onChange={(e) => updateField("eye_strain", Number(e.target.value))}
                />
              </div>
            </div>
          </section>

          {/* WHO-5 */}
          <section className="form-section">
            <div className="section-header">
              <div className="section-number">07</div>
              <div>
                <h2 className="section-title">Wellbeing Index (WHO-5)</h2>
                <p className="section-description">How have you been feeling over the past 2 weeks?</p>
              </div>
            </div>

            <div className="form-grid-1">
              <div className="input-group">
                <label className="input-label">I have felt cheerful and in good spirits</label>
                <select
                  className="input-field"
                  value={form.who5_q1}
                  onChange={(e) => updateField("who5_q1", e.target.value)}
                >
                  <option value="At no time">At no time</option>
                  <option value="Some of the time">Some of the time</option>
                  <option value="Less than half of the time">Less than half of the time</option>
                  <option value="More than half of the time">More than half of the time</option>
                  <option value="Most of the time">Most of the time</option>
                  <option value="All of the time">All of the time</option>
                </select>
              </div>

              <div className="input-group">
                <label className="input-label">I have felt calm and relaxed</label>
                <select
                  className="input-field"
                  value={form.who5_q2}
                  onChange={(e) => updateField("who5_q2", e.target.value)}
                >
                  <option value="At no time">At no time</option>
                  <option value="Some of the time">Some of the time</option>
                  <option value="Less than half of the time">Less than half of the time</option>
                  <option value="More than half of the time">More than half of the time</option>
                  <option value="Most of the time">Most of the time</option>
                  <option value="All of the time">All of the time</option>
                </select>
              </div>

              <div className="input-group">
                <label className="input-label">I have felt active and vigorous</label>
                <select
                  className="input-field"
                  value={form.who5_q3}
                  onChange={(e) => updateField("who5_q3", e.target.value)}
                >
                  <option value="At no time">At no time</option>
                  <option value="Some of the time">Some of the time</option>
                  <option value="Less than half of the time">Less than half of the time</option>
                  <option value="More than half of the time">More than half of the time</option>
                  <option value="Most of the time">Most of the time</option>
                  <option value="All of the time">All of the time</option>
                </select>
              </div>

              <div className="input-group">
                <label className="input-label">I woke up feeling fresh and rested</label>
                <select
                  className="input-field"
                  value={form.who5_q4}
                  onChange={(e) => updateField("who5_q4", e.target.value)}
                >
                  <option value="At no time">At no time</option>
                  <option value="Some of the time">Some of the time</option>
                  <option value="Less than half of the time">Less than half of the time</option>
                  <option value="More than half of the time">More than half of the time</option>
                  <option value="Most of the time">Most of the time</option>
                  <option value="All of the time">All of the time</option>
                </select>
              </div>

              <div className="input-group">
                <label className="input-label">My daily life has been filled with things that interest me</label>
                <select
                  className="input-field"
                  value={form.who5_q5}
                  onChange={(e) => updateField("who5_q5", e.target.value)}
                >
                  <option value="At no time">At no time</option>
                  <option value="Some of the time">Some of the time</option>
                  <option value="Less than half of the time">Less than half of the time</option>
                  <option value="More than half of the time">More than half of the time</option>
                  <option value="Most of the time">Most of the time</option>
                  <option value="All of the time">All of the time</option>
                </select>
              </div>
            </div>
          </section>

          <div className="form-actions">
            <button className="submit-btn" type="submit" disabled={loading}>
              {loading ? (
                <>
                  <span className="spinner"></span>
                  Analyzing Your Data...
                </>
              ) : (
                <>
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                    <path d="M9 11L12 14L22 4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    <path d="M21 12V19C21 20.1046 20.1046 21 19 21H5C3.89543 21 3 20.1046 3 19V5C3 3.89543 3.89543 3 5 3H16" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                  Generate Risk Assessment
                </>
              )}
            </button>
          </div>
        </form>

        {/* ERRORS */}
        {error && (
          <div className="alert alert-error">
            <div className="alert-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2"/>
                <path d="M12 8V12" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                <circle cx="12" cy="16" r="1" fill="currentColor"/>
              </svg>
            </div>
            <div>
              <h3 className="alert-title">Error Occurred</h3>
              <p className="alert-message">{error}</p>
            </div>
          </div>
        )}

        {/* RESPONSE */}
        {response && (
          <div className="results" id="results">
            <div className="results-header">
              <h2 className="results-title">Your Health Risk Assessment</h2>
              <p className="results-subtitle">Based on your responses, here's a comprehensive analysis of your workplace health risks</p>
            </div>

            {/* Main Prediction Card */}
            <div className="prediction-card" style={{ borderColor: getRiskColor(response.prediction.risk_label) }}>
              <div className="prediction-content">
                <div className="prediction-label-group">
                  <span className="prediction-label-text">Overall Risk Level</span>
                  <h3 
                    className="prediction-label-value" 
                    style={{ color: getRiskColor(response.prediction.risk_label) }}
                  >
                    {response.prediction.risk_label}
                  </h3>
                </div>
                <div className="prediction-confidence">
                  <div className="confidence-label">Confidence Score</div>
                  <div className="confidence-value">
                    {(response.prediction.confidence_score * 100).toFixed(1)}%
                  </div>
                  <div className="confidence-bar">
                    <div 
                      className="confidence-fill" 
                      style={{ 
                        width: `${response.prediction.confidence_score * 100}%`,
                        backgroundColor: getRiskColor(response.prediction.risk_label)
                      }}
                    ></div>
                  </div>
                </div>
              </div>
            </div>

            {/* Risk Indices Grid */}
            <div className="metrics-section">
              <h3 className="metrics-title">Risk Indices Breakdown</h3>
              <div className="metrics-grid">
                <div className="metric-card">
                  <div className="metric-icon" style={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}>
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                      <path d="M12 2C10.3431 2 9 3.34315 9 5C9 6.65685 10.3431 8 12 8C13.6569 8 15 6.65685 15 5C15 3.34315 13.6569 2 12 2Z" fill="white"/>
                      <path d="M7 22V14C7 12.8954 7.89543 12 9 12H15C16.1046 12 17 12.8954 17 14V22" stroke="white" strokeWidth="2" strokeLinecap="round"/>
                    </svg>
                  </div>
                  <div className="metric-label">Posture Risk</div>
                  <div className="metric-value">{response.risk_indices.posture_risk_index.toFixed(2)}</div>
                </div>

                <div className="metric-card">
                  <div className="metric-icon" style={{ background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)' }}>
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                      <circle cx="12" cy="12" r="3" stroke="white" strokeWidth="2"/>
                      <path d="M12 5V2M12 22V19M19 12H22M2 12H5" stroke="white" strokeWidth="2" strokeLinecap="round"/>
                      <path d="M17 7L19 5M5 19L7 17M17 17L19 19M5 5L7 7" stroke="white" strokeWidth="2" strokeLinecap="round"/>
                    </svg>
                  </div>
                  <div className="metric-label">Visual Strain</div>
                  <div className="metric-value">{response.risk_indices.visual_strain_index.toFixed(2)}</div>
                </div>

                <div className="metric-card">
                  <div className="metric-icon" style={{ background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)' }}>
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                      <path d="M9.5 2C13.0899 2 16 4.91015 16 8.5C16 10.3736 15.1721 12.0569 13.8527 13.1918L20.5104 19.8494C20.8931 20.2321 20.8931 20.8474 20.5104 21.2301C20.1277 21.6128 19.5123 21.6128 19.1296 21.2301L12.4719 14.5725C11.3371 15.892 9.65381 16.7198 7.78027 16.7198C4.19037 16.7198 1.28027 13.8097 1.28027 10.2198C1.28027 6.62988 4.19037 3.71973 7.78027 3.71973" stroke="white" strokeWidth="2" strokeLinecap="round"/>
                    </svg>
                  </div>
                  <div className="metric-label">Cognitive Load</div>
                  <div className="metric-value">{response.risk_indices.cognitive_load_index.toFixed(2)}</div>
                </div>

                <div className="metric-card">
                  <div className="metric-icon" style={{ background: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)' }}>
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                      <path d="M20 14C20 18.4183 16.4183 22 12 22C7.58172 22 4 18.4183 4 14" stroke="white" strokeWidth="2" strokeLinecap="round"/>
                      <path d="M12 2V6M8 4L12 6L16 4" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                  </div>
                  <div className="metric-label">Musculoskeletal</div>
                  <div className="metric-value">{response.risk_indices.msk_risk_index.toFixed(2)}</div>
                </div>

                <div className="metric-card">
                  <div className="metric-icon" style={{ background: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)' }}>
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                      <path d="M12 21C16.9706 21 21 16.9706 21 12C21 7.02944 16.9706 3 12 3C7.02944 3 3 7.02944 3 12C3 16.9706 7.02944 21 12 21Z" stroke="white" strokeWidth="2"/>
                      <path d="M9 12H15M12 9V15" stroke="white" strokeWidth="2" strokeLinecap="round"/>
                    </svg>
                  </div>
                  <div className="metric-label">Lifestyle</div>
                  <div className="metric-value">{response.risk_indices.lifestyle_risk_index.toFixed(2)}</div>
                </div>

                <div className="metric-card metric-card-highlight">
                  <div className="metric-icon" style={{ background: 'linear-gradient(135deg, #f857a6 0%, #ff5858 100%)' }}>
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                      <path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z" fill="white"/>
                    </svg>
                  </div>
                  <div className="metric-label">Overall Risk Index</div>
                  <div className="metric-value">{response.risk_indices.overall_risk_index.toFixed(2)}</div>
                </div>
              </div>
            </div>

            {/* Model Probabilities */}
            <div className="probabilities-section">
              <h3 className="metrics-title">Risk Category Probabilities</h3>
              <div className="probability-bars">
                <div className="probability-item">
                  <div className="probability-header">
                    <span className="probability-label">Low Risk</span>
                    <span className="probability-value">{(response.model_probabilities.low * 100).toFixed(1)}%</span>
                  </div>
                  <div className="probability-bar">
                    <div 
                      className="probability-fill" 
                      style={{ 
                        width: `${response.model_probabilities.low * 100}%`,
                        background: 'var(--success)'
                      }}
                    ></div>
                  </div>
                </div>

                <div className="probability-item">
                  <div className="probability-header">
                    <span className="probability-label">Moderate Risk</span>
                    <span className="probability-value">{(response.model_probabilities.moderate * 100).toFixed(1)}%</span>
                  </div>
                  <div className="probability-bar">
                    <div 
                      className="probability-fill" 
                      style={{ 
                        width: `${response.model_probabilities.moderate * 100}%`,
                        background: 'var(--warning)'
                      }}
                    ></div>
                  </div>
                </div>

                <div className="probability-item">
                  <div className="probability-header">
                    <span className="probability-label">High Risk</span>
                    <span className="probability-value">{(response.model_probabilities.high * 100).toFixed(1)}%</span>
                  </div>
                  <div className="probability-bar">
                    <div 
                      className="probability-fill" 
                      style={{ 
                        width: `${response.model_probabilities.high * 100}%`,
                        background: 'var(--danger)'
                      }}
                    ></div>
                  </div>
                </div>
              </div>
            </div>

            {/* RAG Report */}
            {response.rag_report && (
              <div className="report-section">
                <h3 className="metrics-title">Personalized Recommendations</h3>
                <div className="report-content">
                  <pre className="report-text">{response.rag_report}</pre>
                </div>
              </div>
            )}

            {/* Raw JSON - Collapsible */}
            <details className="json-details">
              <summary className="json-summary">View Complete Technical Data (JSON)</summary>
              <pre className="json-content">{JSON.stringify(response, null, 2)}</pre>
            </details>
          </div>
        )}
      </div>
    </div>
  );
}