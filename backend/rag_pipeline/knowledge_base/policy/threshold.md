# ErgoCare AI – Threshold Policy

## Purpose
This document defines threshold rules for classifying ergonomic risk severity.

Thresholding must remain:
- Transparent
- Stable
- Clinically sensible
- Adjustable after stakeholder review

---

## Risk Level Categories
All risk models must map output scores into:

- Low Risk
- Moderate Risk
- High Risk

---

## Threshold Philosophy
Thresholds should be chosen based on:
- distribution of collected data
- ergonomic domain reasoning
- stakeholder validation

Thresholds must not be tuned aggressively for "high risk detection" unless validated.

---

## Example Threshold Template

### Posture Risk
- Low: PRI < 0.33
- Moderate: 0.33 <= PRI < 0.66
- High: PRI >= 0.66

### Visual Strain
- Low: SES < 0.33
- Moderate: 0.33 <= SES < 0.66
- High: SES >= 0.66

### Cognitive Stress
- Low: CLI < 0.33
- Moderate: 0.33 <= CLI < 0.66
- High: CLI >= 0.66

---

## Custom Threshold Support
Thresholds may be domain-specific.

Example:
- Musculoskeletal discomfort may use intensity-based cutoffs rather than normalized ranges.

---

## Revision Policy
Threshold updates must:
- be versioned
- include justification notes
- include stakeholder review record
