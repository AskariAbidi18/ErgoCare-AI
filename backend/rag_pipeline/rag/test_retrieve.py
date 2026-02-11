from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

DB_PATH = "vectordb/chroma_ergo"

def main():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    vectordb = Chroma(
        persist_directory=DB_PATH,
        embedding_function=embeddings
    )

    query = "What are the rules for avoiding diagnostic medical claims?"
    results = vectordb.similarity_search(query, k=3)

    for i, doc in enumerate(results):
        print("\n==============================")
        print(f"RESULT {i+1}")
        print("SOURCE:", doc.metadata.get("source"))
        print(doc.page_content[:800])
        print("\n==============================")

if __name__ == "__main__":
    main()
