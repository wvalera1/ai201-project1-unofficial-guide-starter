import html
import re
import random
from pathlib import Path
from chunker import chunk_text

DOCUMENTS_DIR = Path("documents")
CHUNK_SIZE = 200
OVERLAP = 50
MIN_TOKENS = 20

_REDDIT_BOILERPLATE = re.compile(
    r"^(Go to \w+|r/\w+|u/\S+ avatar|•|\d+[ymd]o?\s+ago|\d+)$"
)


_TYPOGRAPHIC = str.maketrans({
    "‘": "'", "’": "'",   # curly single quotes
    "“": '"', "”": '"',   # curly double quotes
    "–": "-", "—": "-",   # en-dash, em-dash
    "…": "...",                # ellipsis
    " ": " ",                  # non-breaking space
})


def clean_text(text: str) -> str:
    lines = text.splitlines()
    kept = [l.strip() for l in lines if not _REDDIT_BOILERPLATE.match(l.strip())]
    text = " ".join(kept)
    text = html.unescape(text)           # &amp; &nbsp; &#39; etc.
    text = text.translate(_TYPOGRAPHIC)  # curly quotes → straight, dashes → hyphens
    text = re.sub(r"[^\x00-\x7F]+", " ", text)  # drop remaining non-ASCII
    text = " ".join(text.split())        # normalize whitespace
    return text


def load_documents(docs_dir: Path) -> list[dict]:
    docs = []
    for path in sorted(docs_dir.glob("*.txt")):
        raw = path.read_text(encoding="utf-8", errors="replace")
        text = clean_text(raw)
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


def inspect_chunks(chunks: list[dict], n: int = 5) -> None:
    print(f"\n--- First {n} Chunks ---")
    for c in chunks[:n]:
        print(f"\n[{c['source']} | chunk {c['chunk_index']} | {c['token_count']} tokens]")
        print(c["text"])

    print(f"\n--- 5 Random Chunks (checkpoint) ---")
    for c in random.sample(chunks, min(5, len(chunks))):
        print(f"\n[{c['source']} | chunk {c['chunk_index']} | {c['token_count']} tokens]")
        print(c["text"])

    if chunks:
        counts = [c["token_count"] for c in chunks]
        print(f"\nToken count range : {min(counts)}-{max(counts)}")
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
