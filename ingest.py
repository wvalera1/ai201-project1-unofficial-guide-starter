from pathlib import Path
from chunker import chunk_text

DOCUMENTS_DIR = Path("documents")
CHUNK_SIZE = 200
OVERLAP = 50
MIN_TOKENS = 20


def load_documents(docs_dir: Path) -> list[dict]:
    docs = []
    for path in sorted(docs_dir.glob("*.txt")):
        raw = path.read_text(encoding="utf-8")
        text = " ".join(raw.split())  # normalize whitespace
        docs.append({"source": path.name, "text": text})
    return docs


def build_chunks(docs: list[dict]) -> list[dict]:
    chunks = []
    for doc in docs:
        for i, chunk in enumerate(chunk_text(doc["text"], CHUNK_SIZE, OVERLAP)):
            if len(chunk.split()) < MIN_TOKENS:
                continue
            chunks.append({
                "source": doc["source"],
                "chunk_index": i,
                "text": chunk,
                "token_count": len(chunk.split()),
            })
    return chunks


def inspect_chunks(chunks: list[dict], n: int = 3) -> None:
    print(f"\n--- Chunk Inspection (first {n}) ---")
    for c in chunks[:n]:
        print(f"\n[{c['source']} | chunk {c['chunk_index']} | {c['token_count']} tokens]")
        print(c["text"])

    if chunks:
        counts = [c["token_count"] for c in chunks]
        print(f"\nToken count range : {min(counts)}–{max(counts)}")
        print(f"Average token count: {sum(counts) / len(counts):.1f}")


if __name__ == "__main__":
    docs = load_documents(DOCUMENTS_DIR)
    print(f"Loaded {len(docs)} document(s) from '{DOCUMENTS_DIR}'")

    if not docs:
        print("No .txt files found. Add your sources to the documents/ folder and re-run.")
    else:
        chunks = build_chunks(docs)
        print(f"Total chunks       : {len(chunks)}")
        inspect_chunks(chunks)
