# ErgoCare AI – Citation and Evidence Policy

## Purpose
This policy ensures all RAG-generated text remains evidence-grounded and traceable.

---

## Citation Requirement
If a recommendation is justified using retrieved documents, the system must output:
- Document title
- Section heading (if available)
- Publication year (if available)

---

## No Hallucinated Citations
The system must never fabricate:
- organizations
- authors
- guideline titles
- years
- study results

If evidence is not found, output:
"Supporting guideline evidence was not found in the current knowledge base."

---

## Citation Format (Recommended)
Use a simple readable format:

Evidence Source:
- [NIOSH] Workstation Ergonomics Guide (Section: Monitor Placement)

---

## Prioritized Evidence Hierarchy
When multiple sources exist, prefer:
1. WHO / NIOSH / OSHA / ISO / Government Guidelines
2. Systematic Reviews / Meta-analyses
3. Institutional documents (NIMHANS internal notes)
4. Peer-reviewed single studies
5. Blog-style or non-peer reviewed sources (avoid)

---

## Evidence Safety Rule
If evidence suggests uncertain results, include uncertainty language:
- "Evidence suggests..."
- "Commonly recommended practice includes..."
