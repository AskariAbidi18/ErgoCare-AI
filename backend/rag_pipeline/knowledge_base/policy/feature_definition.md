# ErgoCare AI – Feature Definitions

## Purpose
This document defines engineered features used in risk scoring.
All features must remain human-interpretable and traceable back to questionnaire responses.

---

## Posture Risk Index (PRI)

### Definition
A composite score representing posture-related ergonomic strain.

### Inputs
- Sitting duration per day
- Frequency of bending/leaning posture
- Chair support quality
- Desk height mismatch indicator

### Interpretation
- Low: user reports good posture and adequate support
- Moderate: occasional strain factors exist
- High: prolonged sitting + poor posture indicators

---

## Screen Exposure Score (SES)

### Definition
Represents visual strain likelihood due to screen usage patterns.

### Inputs
- Total screen time per day
- Break frequency
- Lighting quality
- Eye discomfort frequency

### Interpretation
- High SES indicates increased likelihood of visual fatigue

---

## Cognitive Load Index (CLI)

### Definition
Represents mental workload stress level based on self-reported work demands.

### Inputs
- perceived workload rating
- multitasking frequency
- deadlines pressure rating
- fatigue indicator

---

## Workload Stress Score (WSS)

### Definition
Captures overall work-related stress exposure.

### Inputs
- working hours
- work-life balance rating
- sleep quality proxy
- job strain indicator

---

## Musculoskeletal Discomfort Score (MDS)

### Definition
Represents discomfort severity across body regions.

### Inputs
- pain intensity ratings
- pain frequency
- number of body regions affected
- functional limitation indicator

---

## General Constraints
- Features must remain explainable.
- Any transformation (normalization/scaling) must be documented.
- Thresholds must be defined explicitly in the Threshold Policy file.
