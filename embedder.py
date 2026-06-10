from pathlib import Path
from sentence_transformers import SentenceTransformer
import chromadb

from ingest import load_documents, build_chunks, DOCUMENTS_DIR

COLLECTION_NAME = "running_shoes"
CHROMA_PATH = "chroma_db"
MODEL_NAME = "all-MiniLM-L6-v2"


def build_vector_store() -> chromadb.Collection:
    docs = load_documents(DOCUMENTS_DIR)
    chunks = build_chunks(docs)
    print(f"Chunks to embed: {len(chunks)}")

    model = SentenceTransformer(MODEL_NAME)
    texts = [c["text"] for c in chunks]
    print("Embedding... (first run downloads ~90 MB model)")
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_list=True)

    client = chromadb.PersistentClient(path=CHROMA_PATH)

    # Always rebuild from scratch so re-runs stay consistent with the source docs
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    collection.add(
        ids=[f"{c['source']}_{c['chunk_index']}" for c in chunks],
        documents=texts,
        embeddings=embeddings,
        metadatas=[{"source": c["source"], "chunk_index": c["chunk_index"]} for c in chunks],
    )

    print(f"Stored {collection.count()} vectors in '{CHROMA_PATH}/{COLLECTION_NAME}'")
    return collection


if __name__ == "__main__":
    build_vector_store()
