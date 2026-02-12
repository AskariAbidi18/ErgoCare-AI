from pathlib import Path
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.llms import Ollama

from rag_pipeline.rag.rag_gen import generate_report


BASE_DIR = Path(__file__).resolve().parent.parent
CHROMA_DIR = BASE_DIR / "chroma_db"


def run_rag_pipeline(user_data: dict) -> str:
    """
    Input: structured user_data (risk + discomfort info)
    Output: final ergonomic report (string)
    """

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectordb = Chroma(
        persist_directory=str(CHROMA_DIR),
        embedding_function=embeddings
    )

    llm = Ollama(model="llama3.1:8b")

    report = generate_report(llm, vectordb, user_data)

    return report


if __name__ == "__main__":
    sample_user_data = {
        "posture_risk": "High",
        "vision_risk": "Low",
        "cognitive_risk": "Moderate",
        "sitting_hours": 7,
        "neck_discomfort": "Yes",
        "back_discomfort": "Sometimes",
        "eye_strain": "No",
        "stress_level": "Moderate"
    }

    report = run_rag_pipeline(sample_user_data)
    print(report)
