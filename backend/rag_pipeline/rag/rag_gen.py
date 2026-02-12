import json
from pathlib import Path
from typing import Dict, List

from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.llms import Ollama


BASE_DIR = Path(__file__).resolve().parent.parent
CHROMA_DIR = BASE_DIR / "chroma_db"

def retrieve_docs(vectordb, query: str, k: int = 5, domain: str = None):
    if domain:
        return vectordb.similarity_search(query, k=k, filter={"domain": domain})
    return vectordb.similarity_search(query, k=k)


def format_context(docs) -> str:
    context_blocks = []
    for i, d in enumerate(docs):
        source = d.metadata.get("source", "unknown")
        domain = d.metadata.get("domain", "unknown")

        context_blocks.append(
            f"[DOC {i+1}] (domain={domain})\nSOURCE: {source}\nCONTENT:\n{d.page_content}\n"
        )
    return "\n\n".join(context_blocks)


def extract_sources(docs) -> List[str]:
    seen = set()
    sources = []
    for d in docs:
        src = d.metadata.get("source", "unknown")
        if src not in seen:
            seen.add(src)
            sources.append(src)
    return sources

def generate_report(llm, vectordb, user_data: Dict):
    """
    Generates a structured ergonomic recommendation report using:
    - ML pipeline outputs (risk indices + drivers)
    - Retrieved ergonomic/policy documents from Chroma
    """

    # ----------------------------
    # Helper: format numeric risk score to label
    # ----------------------------
    def score_to_label(score: float) -> str:
        if score < 35:
            return "Low"
        elif score < 70:
            return "Moderate"
        return "High"

    # ----------------------------
    # Extract indices (safe fallback)
    # ----------------------------
    posture_score = float(user_data.get("posture_risk_index", 0))
    vision_score = float(user_data.get("visual_strain_index", 0))
    cognitive_score = float(user_data.get("cognitive_load_index", 0))
    msk_score = float(user_data.get("msk_risk_index", 0))
    lifestyle_score = float(user_data.get("lifestyle_risk_index", 0))
    overall_score = float(user_data.get("overall_risk_index", 0))

    posture_label = score_to_label(posture_score)
    vision_label = score_to_label(vision_score)
    cognitive_label = score_to_label(cognitive_score)
    msk_label = score_to_label(msk_score)
    lifestyle_label = score_to_label(lifestyle_score)
    overall_label = score_to_label(overall_score)

    primary_domain = user_data.get("primary_domain", "general")
    high_domains = user_data.get("high_domains", [])
    moderate_domains = user_data.get("moderate_domains", [])

    # ----------------------------
    # Strong query for retrieval
    # ----------------------------
    query = f"""
User ergonomic risk assessment (ErgoCare AI):

Overall Risk Score: {overall_score:.1f} ({overall_label})
Posture Risk Score: {posture_score:.1f} ({posture_label})
Vision Risk Score: {vision_score:.1f} ({vision_label})
Cognitive Stress Score: {cognitive_score:.1f} ({cognitive_label})
Musculoskeletal Pain Score: {msk_score:.1f} ({msk_label})
Lifestyle Risk Score: {lifestyle_score:.1f} ({lifestyle_label})

Primary domain: {primary_domain}
High domains: {high_domains}
Moderate domains: {moderate_domains}

Generate practical ergonomic recommendations, workstation fixes, break scheduling,
stretching guidance, and preventive strategies.
Keep it non-diagnostic.
"""

    # ----------------------------
    # Retrieval Strategy (weighted)
    # ----------------------------
    policy_docs = retrieve_docs(
        vectordb,
        query="clinical safety disclaimer do not diagnose non medical ergonomic report format",
        k=4,
        domain="policy"
    )

    general_docs = retrieve_docs(vectordb, query=query, k=4, domain="general")

    # Primary domain gets more retrieval weight
    primary_docs = retrieve_docs(vectordb, query=query, k=8, domain=primary_domain)

    posture_docs = retrieve_docs(vectordb, query=query, k=3, domain="posture")
    vision_docs = retrieve_docs(vectordb, query=query, k=3, domain="vision")
    cognitive_docs = retrieve_docs(vectordb, query=query, k=3, domain="cognitive")

    retrieved_docs = (
        policy_docs
        + general_docs
        + primary_docs
        + posture_docs
        + vision_docs
        + cognitive_docs
    )

    context = format_context(retrieved_docs)
    sources = extract_sources(retrieved_docs)

    # ----------------------------
    # Hard-constraint system prompt
    # ----------------------------
    system_prompt = f"""
You are ErgoCare AI, an ergonomic decision-support assistant.

You MUST follow these rules:
1. Do NOT diagnose diseases or medical conditions.
2. Do NOT prescribe medications or medical treatments.
3. Be preventive, supportive, and non-alarming.
4. DO NOT write an academic paper or research summary.
5. DO NOT write introduction, abstract, methodology, conclusion, future work.
6. Only use information supported by CONTEXT.
7. If context does not support a claim, do NOT invent it.
8. Recommendations must be specific, actionable, and easy to follow.
9. Evidence sources MUST be ONLY from the retrieved sources list.

OUTPUT FORMAT (STRICT - DO NOT CHANGE STRUCTURE):

### Ergonomic Recommendation Report

## Overall Risk Level
Risk Level: <Low/Moderate/High>
Confidence: <Very High/High/Moderate/Low>

## Key Contributors
- <factor 1>
- <factor 2>
- <factor 3>

## Recommendations

### Posture
- Risk Level:
- Recommendations:
- Why This Helps:

### Vision
- Risk Level:
- Recommendations:
- Why This Helps:

### Cognitive / Stress
- Risk Level:
- Recommendations:
- Why This Helps:

### Musculoskeletal Pain
- Risk Level:
- Recommendations:
- Why This Helps:

### Lifestyle
- Risk Level:
- Recommendations:
- Why This Helps:

## Break Schedule (Practical)
- <timed break schedule suggestions>

## Workstation Checklist
- <chair height, screen height, keyboard, feet, desk>

## Evidence Sources
- [SOURCE: file_path]
- [SOURCE: file_path]

## Disclaimer
<short preventive disclaimer>

FAILURE CONDITION:
If you output anything outside this format, the answer is invalid.
"""

    # ----------------------------
    # User prompt includes user data + retrieved context
    # ----------------------------
    user_prompt = f"""
USER DATA (JSON):
{json.dumps(user_data, indent=2)}

DERIVED RISK LABELS:
- Overall: {overall_label} ({overall_score:.1f})
- Posture: {posture_label} ({posture_score:.1f})
- Vision: {vision_label} ({vision_score:.1f})
- Cognitive: {cognitive_label} ({cognitive_score:.1f})
- MSK Pain: {msk_label} ({msk_score:.1f})
- Lifestyle: {lifestyle_label} ({lifestyle_score:.1f})

CONTEXT DOCUMENTS:
{context}

IMPORTANT INSTRUCTIONS:
- You MUST generate recommendations personalized to the risk scores.
- If a risk domain is Low, explicitly state:
  "No major <domain>-specific recommendations required."
- Key contributors should be taken from high/moderate domains and pain fields.
- Do NOT output research citations like (Gerr et al., 2005).
- Evidence sources must ONLY be from the available retrieved sources list.

AVAILABLE RETRIEVED SOURCES:
{chr(10).join(["- " + s for s in sources])}

Now generate the final ergonomic report.
"""

    # ----------------------------
    # Invoke LLM safely
    # ----------------------------
    response = llm.invoke(system_prompt + "\n\n" + user_prompt)

    # Ollama sometimes returns plain string, sometimes object
    if hasattr(response, "content"):
        response = response.content

    return response

if __name__ == "__main__":
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    vectordb = Chroma(
        persist_directory=str(CHROMA_DIR),
        embedding_function=embeddings
    )

    llm = Ollama(model="llama3.1:8b")

    user_data = {
        "posture_risk": "High",
        "vision_risk": "Low",
        "cognitive_risk": "Moderate",
        "sitting_hours": 7,
        "neck_discomfort": "Yes",
        "back_discomfort": "Sometimes",
        "eye_strain": "No",
        "stress_level": "Moderate"
    }

    report = generate_report(llm, vectordb, user_data)
    print(report)
