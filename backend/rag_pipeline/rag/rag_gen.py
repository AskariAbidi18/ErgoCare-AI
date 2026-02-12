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
    # Create a retrieval query from user data
    query = f"""
    Generate ergonomic recommendations for:
    posture_risk={user_data.get("posture_risk")}
    vision_risk={user_data.get("vision_risk")}
    cognitive_risk={user_data.get("cognitive_risk")}
    sitting_hours={user_data.get("sitting_hours")}
    neck_discomfort={user_data.get("neck_discomfort")}
    back_discomfort={user_data.get("back_discomfort")}
    eye_strain={user_data.get("eye_strain")}
    stress_level={user_data.get("stress_level")}
    """

    # Always retrieve policy docs
    policy_docs = retrieve_docs(vectordb, query="clinical safety disclaimer report formatting", k=6, domain="policy")

    # Retrieve domain docs separately
    posture_docs = retrieve_docs(vectordb, query=query, k=6, domain="posture")
    vision_docs = retrieve_docs(vectordb, query=query, k=6, domain="vision")
    cognitive_docs = retrieve_docs(vectordb, query=query, k=6, domain="cognitive")
    general_docs = retrieve_docs(vectordb, query=query, k=4, domain="general")

    # Merge all retrieved docs
    retrieved_docs = policy_docs + posture_docs + vision_docs + cognitive_docs + general_docs

    context = format_context(retrieved_docs)
    sources = extract_sources(retrieved_docs)

    system_prompt = f"""
You are ErgoCare AI, an ergonomic recommendation assistant.

You MUST follow these rules:
1. Do NOT diagnose diseases or medical conditions.
2. Do NOT prescribe medications or treatments.
3. Be preventive, supportive, and non-alarming.
4. Output must be structured and easy to understand.
5. ONLY cite sources that appear in the context documents.
6. If context does not support a claim, do NOT invent it.

You are given policy and ergonomic documents in CONTEXT.
Use them strictly.

OUTPUT FORMAT (STRICT):

### Ergonomic Recommendation Report

## Overall Risk Level
Risk Level: <Low/Moderate/High>

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

## Evidence Sources
- [SOURCE: file_path]
- [SOURCE: file_path]

## Disclaimer
<include disclaimer based on policy>

IMPORTANT:
- If risk level is Low, keep recommendations minimal.
- If Vision risk is Low, explicitly say "No major vision-specific recommendations required."
- Evidence sources MUST be only from the context sources list.
"""

    user_prompt = f"""
USER DATA (JSON):
{json.dumps(user_data, indent=2)}

CONTEXT DOCUMENTS:
{context}

Now generate the final ergonomic report.
"""

    response = llm.invoke(system_prompt + "\n\n" + user_prompt)

    # Append verified sources list (extra safety)
    response += "\n\n(Available Retrieved Sources)\n"
    for s in sources:
        response += f"- {s}\n"

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
