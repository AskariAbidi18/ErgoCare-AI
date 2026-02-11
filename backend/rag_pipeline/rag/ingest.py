import os
import shutil
from pathlib import Path
from typing import List
import numpy as np

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import Chroma

from langchain_huggingface import HuggingFaceEmbeddings


BASE_DIR = Path(__file__).resolve().parent.parent
KB_DIR = BASE_DIR / "knowledge_base"
CHROMA_DIR = BASE_DIR / "chroma_db"

POLICY_DIR = KB_DIR / "policy"
DOCS_DIR = KB_DIR / "docs"


DOMAIN_ANCHORS = {
    "posture": (
        "neck pain, back pain, sitting posture, chair support, lumbar support, "
        "spine alignment, musculoskeletal discomfort, shoulder pain, awkward posture, "
        "ergonomic chair, posture correction"
    ),
    "vision": (
        "eye strain, screen exposure, computer vision syndrome, dry eyes, "
        "brightness, glare, monitor height, blue light, visual fatigue, blurred vision"
    ),
    "cognitive": (
        "stress, burnout, mental workload, fatigue, anxiety, concentration issues, "
        "work pressure, cognitive load, emotional exhaustion"
    ),
    "general": (
        "ergonomics guidelines, workplace health, preventive habits, health safety, "
        "general recommendations, ergonomic risk prevention"
    )
}


def cosine_sim(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def classify_domain(text: str, embeddings_model) -> str:
    text = text.strip()
    if not text:
        return "general"

    text_emb = embeddings_model.embed_query(text[:1500])

    best_domain = "general"
    best_score = -1

    for domain, anchor_text in DOMAIN_ANCHORS.items():
        anchor_emb = embeddings_model.embed_query(anchor_text)
        score = cosine_sim(text_emb, anchor_emb)

        if score > best_score:
            best_score = score
            best_domain = domain

    # Threshold: if too weak similarity, mark general
    if best_score < 0.35:
        return "general"

    return best_domain


def collect_files(folder: Path, exts: List[str]) -> List[Path]:
    all_files = []
    for root, _, files in os.walk(folder):
        for f in files:
            if any(f.lower().endswith(ext) for ext in exts):
                all_files.append(Path(root) / f)
    return all_files


def load_md_file(file_path: Path):
    loader = TextLoader(str(file_path), encoding="utf-8")
    return loader.load()


def load_pdf_file(file_path: Path):
    loader = PyPDFLoader(str(file_path))
    return loader.load()


def main():
    print("=== Base Ingestion (PDF + MD) ===")

    if not POLICY_DIR.exists():
        raise FileNotFoundError(f"Policy folder not found: {POLICY_DIR}")

    if not DOCS_DIR.exists():
        raise FileNotFoundError(f"Docs folder not found: {DOCS_DIR}")

    # Reset Chroma DB
    if CHROMA_DIR.exists():
        print(f"[INFO] Removing old Chroma DB at: {CHROMA_DIR}")
        shutil.rmtree(CHROMA_DIR)

    md_files = collect_files(POLICY_DIR, [".md"])
    pdf_files = collect_files(DOCS_DIR, [".pdf"])

    print(f"[INFO] Found {len(md_files)} policy markdown files")
    print(f"[INFO] Found {len(pdf_files)} PDF documents")

    # Load embeddings once
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    all_docs = []

    # Load markdown policy docs
    for f in md_files:
        docs = load_md_file(f)

        for d in docs:
            d.metadata["source"] = str(f)
            d.metadata["domain"] = "policy"
            d.metadata["file_type"] = "md"

        all_docs.extend(docs)

    # Load PDFs and classify their domain
    for f in pdf_files:
        docs = load_pdf_file(f)

        for d in docs:
            predicted_domain = classify_domain(d.page_content, embeddings)

            d.metadata["source"] = str(f)
            d.metadata["domain"] = predicted_domain
            d.metadata["file_type"] = "pdf"

        all_docs.extend(docs)

    print(f"[INFO] Total raw loaded docs: {len(all_docs)}")

    # Chunking
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,
        chunk_overlap=200
    )

    chunked_docs = splitter.split_documents(all_docs)

    print(f"[INFO] Total chunks created: {len(chunked_docs)}")

    # Store into Chroma
    vectordb = Chroma.from_documents(
        documents=chunked_docs,
        embedding=embeddings,
        persist_directory=str(CHROMA_DIR)
    )

    vectordb.persist()

    print("=== Ingestion Completed Successfully ===")
    print(f"[INFO] Vector DB saved at: {CHROMA_DIR}")

    # Domain distribution stats
    domain_count = {}
    for d in chunked_docs:
        dom = d.metadata.get("domain", "unknown")
        domain_count[dom] = domain_count.get(dom, 0) + 1

    print("\n=== Domain Distribution ===")
    for k, v in sorted(domain_count.items(), key=lambda x: x[1], reverse=True):
        print(f"{k:10s} -> {v}")


if __name__ == "__main__":
    main()
