# ErgoCare AI – LLM Generation Policy

## Objective
This document defines how LLM-generated text should be produced for reports and explanations.

The goal is to ensure:
- Safety
- Consistency
- Interpretability
- Clinical sensibility
- Non-diagnostic language

---

## Allowed Outputs
The LLM is allowed to generate:
- Explanation of risk factors
- Preventive ergonomic recommendations
- Summaries of ergonomic habits
- Evidence-based justification text (when RAG context exists)
- Report-friendly narrative text

---

## Forbidden Outputs
The LLM must not:
- Diagnose disorders or conditions
- Suggest medications or treatments
- Suggest surgical procedures
- Use medical certainty language ("this confirms", "this indicates disease")
- Provide mental health therapy guidance

---

## Evidence Grounding Rule
If a recommendation requires justification, the LLM must:
- Use retrieved context from the knowledge base
- Reference sources where possible
- Avoid inventing citations

If insufficient evidence exists in retrieved context:
- The system must provide a generic ergonomic explanation OR state that evidence is not available in the current guideline set.

---

## Confidence and Uncertainty Language
When uncertain, the model must use cautious phrasing:
- "may"
- "can help"
- "could reduce discomfort"
- "is commonly recommended"

Avoid definitive claims:
- "will cure"
- "will fix"
- "this guarantees"

---

## Output Formatting Requirements
Each generated section should contain:
- Risk severity label (Low / Moderate / High)
- Key contributing factors
- Recommendations
- Short justification text

Recommended format:

### Section Title
- Risk Level:
- Main Contributors:
- Recommendations:
- Why This Helps:

---

## Required Disclaimer
Every report must include the standard disclaimer defined in the Clinical Safety Policy.
