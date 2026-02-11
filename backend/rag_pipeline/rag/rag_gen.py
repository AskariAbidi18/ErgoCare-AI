from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_ollama import ChatOllama


DB_PATH = "vectordb/chroma_ergo"

SYSTEM_PROMPT = """
You are ErgoCare AI, an ergonomic decision-support assistant.

STRICT RULES:
- You are NOT a doctor and you must NOT diagnose any condition.
- You must provide preventive ergonomic guidance only.
- You must use ONLY the provided retrieved context.
- If context is insufficient, say: "Insufficient evidence found in the current knowledge base."
- Avoid fear-based language.
- Always include a disclaimer at the end.

OUTPUT FORMAT:
### Ergonomic Recommendation Report
Risk Level: <Low/Moderate/High>
Key Contributors:
- ...
Recommendations:
- ...
Justification (Evidence-Based):
- ...
Evidence Sources:
- ...
Disclaimer:
- ErgoCare AI provides ergonomic awareness and preventive recommendations. It is not a diagnostic tool and does not replace professional medical advice.
"""


def retrieve_context(query: str, k: int = 5):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    vectordb = Chroma(
        persist_directory=DB_PATH,
        embedding_function=embeddings
    )

    docs = vectordb.similarity_search(query, k=k)

    context = "\n\n".join(
        [f"[SOURCE: {doc.metadata.get('source')}]\n{doc.page_content}" for doc in docs]
    )

    sources = list(set([doc.metadata.get("source") for doc in docs]))
    return context, sources


def generate_report(query: str, risk_level: str):
    context, sources = retrieve_context(query)

    llm = ChatOllama(
        model="llama3.1:8b",
        temperature=0.2
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", """
User Query / Scenario:
{query}

Risk Level (from scoring model):
{risk_level}

Retrieved Context:
{context}
""")
    ])

    chain = prompt | llm | StrOutputParser()

    result = chain.invoke({
        "query": query,
        "risk_level": risk_level,
        "context": context
    })

    return result


if __name__ == "__main__":
    test_query = "User has high posture risk, sits 7 hours daily, reports neck discomfort and poor chair support."
    print(generate_report(test_query, "High"))
