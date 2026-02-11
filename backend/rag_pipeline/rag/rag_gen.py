# rag/rag_gen.py
import os
import json
from typing import List, Dict, Any, Tuple
import chromadb
from chromadb.config import Settings
import ollama

CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "ergocare_kb"

OLLAMA_MODEL = "llama3.1:8b"
OLLAMA_EMBED_MODEL = "llama3.1:8b"


TOP_K = 5

def safe_json_load(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def detect_domains(user_data: Dict[str, Any]) -> List[str]:
    """
    Decide which KB domains should be queried based on user risk signals.
    """
    domains = ["policy"]  
    posture_risk = str(user_data.get("posture_risk", "")).lower()
    vision_risk = str(user_data.get("vision_risk", "")).lower()
    cognitive_risk = str(user_data.get("cognitive_risk", "")).lower()

    if posture_risk in ["medium", "moderate", "high"]:
        domains.append("posture")

    if vision_risk in ["medium", "moderate", "high"]:
        domains.append("vision")

    if cognitive_risk in ["medium", "moderate", "high"]:
        domains.append("cognitive")

    if user_data.get("neck_discomfort", "").lower() in ["yes", "true", "y"]:
        if "posture" not in domains:
            domains.append("posture")

    if user_data.get("eye_strain", "").lower() in ["yes", "true", "y"]:
        if "vision" not in domains:
            domains.append("vision")

    if user_data.get("stress", "").lower() in ["yes", "true", "y"]:
        if "cognitive" not in domains:
            domains.append("cognitive")

    return list(dict.fromkeys(domains))


def build_query(user_data: Dict[str, Any], domain: str) -> str:
    """
    Build domain-specific query string for retrieval.
    """
    base = f"""
User profile ergonomic signals:
- posture_risk: {user_data.get("posture_risk")}
- vision_risk: {user_data.get("vision_risk")}
- cognitive_risk: {user_data.get("cognitive_risk")}
- sitting_hours: {user_data.get("sitting_hours")}
- neck_discomfort: {user_data.get("neck_discomfort")}
- chair_support: {user_data.get("chair_support")}
- eye_strain: {user_data.get("eye_strain")}
- stress: {user_data.get("stress")}
- break_frequency: {user_data.get("break_frequency")}
"""

    if domain == "posture":
        return base + "\nRetrieve best evidence-based posture and sitting recommendations."
    if domain == "vision":
        return base + "\nRetrieve best evidence-based screen/vision ergonomics recommendations."
    if domain == "cognitive":
        return base + "\nRetrieve best evidence-based cognitive load and stress ergonomics recommendations."
    if domain == "policy":
        return "Retrieve disclaimer and safety policy for ergonomic recommendations."

    return base + "\nRetrieve relevant ergonomic guidance."


def embed_text(text: str) -> List[float]:
    """
    Uses Ollama embeddings endpoint.
    """
    resp = ollama.embeddings(model=OLLAMA_EMBED_MODEL, prompt=text)
    return resp["embedding"]


def init_chroma_collection():
    client = chromadb.PersistentClient(
        path=CHROMA_PATH,
        settings=Settings(anonymized_telemetry=False)
    )
    return client.get_or_create_collection(name=COLLECTION_NAME)


def retrieve_docs(collection, query: str, domain: str, k: int = TOP_K) -> List[Dict[str, Any]]:
    """
    Retrieve documents with metadata filtering by domain.
    Assumes ingestion stored metadata["domain"].
    """
    query_emb = embed_text(query)

    results = collection.query(
        query_embeddings=[query_emb],
        n_results=k,
        where={"domain": domain},
        include=["documents", "metadatas", "distances"]
    )

    docs = []
    for i in range(len(results["documents"][0])):
        docs.append({
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i]
        })

    return docs


def format_sources(docs: List[Dict[str, Any]]) -> str:
    seen = set()
    sources = []

    for d in docs:
        src = d.get("metadata", {}).get("source", "unknown_source")
        if src not in seen:
            seen.add(src)
            sources.append(f"- [SOURCE: {src}]")

    if not sources:
        return "- [SOURCE: none]"

    return "\n".join(sources)


def make_context_block(domain_docs: Dict[str, List[Dict[str, Any]]]) -> str:
    """
    Build context block for the LLM.
    """
    out = []
    for domain, docs in domain_docs.items():
        out.append(f"\n===== DOMAIN: {domain.upper()} =====")
        if not docs:
            out.append("NO DOCUMENTS FOUND.")
            continue

        for idx, d in enumerate(docs, start=1):
            src = d.get("metadata", {}).get("source", "unknown_source")
            out.append(f"\n[Doc {idx}] Source: {src}\n{d['text']}\n")

    return "\n".join(out)


def generate_report(user_data: Dict[str, Any], domain_docs: Dict[str, List[Dict[str, Any]]]) -> str:
    """
    Calls Ollama LLM with strict grounded instructions.
    """
    context = make_context_block(domain_docs)

    system_prompt = f"""
You are ErgoCare AI, an ergonomic recommendation assistant.

STRICT RULES:
1. Only recommend things supported by provided context documents.
2. Do NOT invent medical metrics like SES/PRI unless present in context.
3. If information is missing, say "Not enough evidence in KB".
4. Only include a domain section (Posture/Vision/Cognitive) if the user's risk is moderate/high OR symptoms indicate it.
5. Always include a Disclaimer section using policy docs if available.
6. Always output sources at the end.

Output Format:

### Ergonomic Recommendation Report
Risk Level: <Low/Moderate/High>

## Key Contributors
- ...

## Recommendations
### Posture
- ...
### Vision
- ...
### Cognitive
- ...

## Justification (Evidence-Based)
<short evidence justification>

## Evidence Sources
- [SOURCE: ...]

## Disclaimer
<disclaimer text>
"""

    user_prompt = f"""
USER_DATA (JSON):
{json.dumps(user_data, indent=2)}

KNOWLEDGE_BASE_CONTEXT:
{context}

Generate the report now.
"""

    resp = ollama.chat(
        model=OLLAMA_MODEL,
        messages=[
            {"role": "system", "content": system_prompt.strip()},
            {"role": "user", "content": user_prompt.strip()}
        ],
        options={
            "temperature": 0.2,
            "top_p": 0.9
        }
    )

    return resp["message"]["content"]


def compute_risk_level(user_data: Dict[str, Any]) -> str:
    """
    Basic overall risk logic (simple heuristic).
    """
    posture = str(user_data.get("posture_risk", "")).lower()
    vision = str(user_data.get("vision_risk", "")).lower()
    cognitive = str(user_data.get("cognitive_risk", "")).lower()

    if "high" in [posture, vision, cognitive]:
        return "High"
    if any(x in ["moderate", "medium"] for x in [posture, vision, cognitive]):
        return "Moderate"
    return "Low"


if __name__ == "__main__":
    """
    Expected input file: rag/input/user_data.json
    Example:
    {
      "posture_risk": "High",
      "vision_risk": "Low",
      "cognitive_risk": "Moderate",
      "sitting_hours": 7,
      "neck_discomfort": "Yes",
      "chair_support": "Poor",
      "eye_strain": "No",
      "stress": "Yes",
      "break_frequency": "Rare"
    }
    """

    input_path = "rag/input/user_data.json"
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Missing input file: {input_path}")

    user_data = safe_json_load(input_path)
    user_data["overall_risk_level"] = compute_risk_level(user_data)

    collection = init_chroma_collection()

    domains = detect_domains(user_data)

    domain_docs: Dict[str, List[Dict[str, Any]]] = {}

    for domain in domains:
        query = build_query(user_data, domain)
        docs = retrieve_docs(collection, query, domain, k=TOP_K)
        domain_docs[domain] = docs

    report = generate_report(user_data, domain_docs)

    all_docs = []
    for dlist in domain_docs.values():
        all_docs.extend(dlist)

    sources_block = format_sources(all_docs)

    if "## Evidence Sources" not in report:
        report += "\n\n## Evidence Sources\n" + sources_block

    print(report)
