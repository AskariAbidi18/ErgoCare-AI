import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

KB_PATH = "knowledge_base"
DB_PATH = "vectordb/chroma_ergo"

def load_markdown_files(base_path):
    docs = []
    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith(".md"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    text = f.read()

                docs.append({
                    "text": text,
                    "metadata": {
                        "source": path,
                        "type": "policy" if "policy" in root else "internal_doc"
                    }
                })
    return docs


def main():
    print("[INFO] Loading markdown files...")
    print(f"[INFO] {KB_PATH}")
    print(f"[INFO] {DB_PATH}")

    raw_docs = load_markdown_files(KB_PATH)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=120
    )

    texts = []
    metadatas = []

    print("[INFO] Chunking documents...")
    for doc in raw_docs:
        chunks = splitter.split_text(doc["text"])
        for i, chunk in enumerate(chunks):
            texts.append(chunk)
            metadatas.append({
                **doc["metadata"],
                "chunk_id": i
            })
    print(f"[DEBUG] Number of chunks: {len(texts)}")


    print("[INFO] Loading embedding model...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    print("[INFO] Storing embeddings in ChromaDB...")
    vectordb = Chroma.from_texts(
        texts=texts,
        embedding=embeddings,
        metadatas=metadatas,
        persist_directory=DB_PATH
    )

    vectordb.persist()
    print(f"[DONE] Stored {len(texts)} chunks into {DB_PATH}")


if __name__ == "__main__":
    main()