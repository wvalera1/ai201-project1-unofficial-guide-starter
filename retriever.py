from sentence_transformers import SentenceTransformer
import chromadb

COLLECTION_NAME = "running_shoes"
CHROMA_PATH = "chroma_db"
MODEL_NAME = "all-MiniLM-L6-v2"
TOP_K = 20

_model: SentenceTransformer | None = None
_collection: chromadb.Collection | None = None


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def _get_collection() -> chromadb.Collection:
    global _collection
    if _collection is None:
        client = chromadb.PersistentClient(path=CHROMA_PATH)
        _collection = client.get_collection(COLLECTION_NAME)
    return _collection


def retrieve(query: str, top_k: int = TOP_K) -> list[dict]:
    """Return top_k chunks most relevant to query, each with text, source, and distance."""
    model = _get_model()
    collection = _get_collection()

    query_embedding = model.encode(query, convert_to_list=True)

    # results["documents"][0] is a list — the [0] index is because ChromaDB supports
    # batched queries; we only send one query at a time so we always take index 0.
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    return [
        {
            "text": doc,
            "source": meta["source"],
            "chunk_index": meta["chunk_index"],
            "distance": dist,
        }
        for doc, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        )
    ]


if __name__ == "__main__":
    test_queries = [
        "What are the most expensive shoes offered by Nike?",
        "According to Supwell, are On Cloudboom Strike LS worth the $330 price tag?",
        "What are the best daily trainers for stability, according to Running Warehouse?",
    ]
    for q in test_queries:
        print(f"\nQuery: {q}")
        hits = retrieve(q, top_k=3)
        for i, h in enumerate(hits, 1):
            print(f"  [{i}] {h['source']} (dist={h['distance']:.4f})")
            print(f"       {h['text'][:120]}...")
