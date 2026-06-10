def chunk_text(text: str, chunk_size: int = 200, overlap: int = 50) -> list[str]:
    """Split text into overlapping windows measured in whitespace-delimited tokens."""
    words = text.split()
    if not words:
        return []
    chunks = []
    start = 0
    step = chunk_size - overlap
    while start < len(words):
        chunk = " ".join(words[start : start + chunk_size])
        chunks.append(chunk)
        start += step
    return chunks
