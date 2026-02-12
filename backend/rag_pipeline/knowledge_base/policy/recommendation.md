# ErgoCare AI – Recommendation Mapping Manual

## Purpose
This document defines how risk indicators map to ergonomic recommendations.
It ensures that all interventions are consistent, explainable, and clinically sensible.

---

## Recommendation Principles
All recommendations must be:
- Low-risk and preventive
- Practical for academic faculty environments
- Easy to implement without special equipment
- Non-diagnostic

---

## Postural Risk Domain

### Trigger Conditions
Postural Risk is considered High when:
- Posture Risk Index >= threshold_high
- Sitting duration >= 6 hours/day
- Frequent neck bending or forward head posture indicators are present

### Recommendations
1. Micro-breaks every 30–45 minutes
2. Chair height adjustment guidance
3. Lumbar support usage
4. Screen repositioning to eye level
5. Stretching routine (neck, shoulder, lower back)

### Example Mapping
If:
- High posture risk + sitting > 6 hrs/day
Then recommend:
- micro-break schedule + posture correction + lumbar support

---

## Visual Strain Domain

### Trigger Conditions
Visual Strain is High when:
- Screen exposure score is high
- Frequent headaches or eye fatigue is reported
- Poor lighting conditions are reported

### Recommendations
1. 20-20-20 rule
2. Reduce screen glare and adjust brightness
3. Increase font size and contrast
4. Encourage proper monitor distance (arm-length)
5. Encourage blinking reminders

---

## Cognitive Stress Domain

### Trigger Conditions
Cognitive Stress is High when:
- Cognitive load index is high
- Workload stress score is high
- Sleep disruption or fatigue indicators exist

### Recommendations
1. Task batching and prioritization
2. Short recovery breaks
3. Work boundary practices (end-of-day cutoff)
4. Break scheduling aligned with mental fatigue
5. Encourage institutional workload support if severe

---

## Musculoskeletal Discomfort Domain

### Trigger Conditions
Discomfort is High when:
- Discomfort score high
- Pain reported frequently (daily/weekly)
- Multiple pain regions reported (neck + shoulder + lower back)

### Recommendations
1. Gentle stretching and mobility exercises
2. Reduce continuous sitting time
3. Evaluate workstation ergonomics
4. Encourage physiotherapy consultation if persistent

---

## Safety Escalation Rule
If:
- pain frequency = daily AND pain intensity = high
Then:
- recommend professional consultation with physiotherapist/doctor
- include safety disclaimer

---

## Output Constraints
- Avoid medical diagnosis terms
- Avoid suggesting medications
- Avoid claiming permanent damage

---

## Version Notes
All thresholds must be defined in the Feature Definitions file.
