import os
from dotenv import load_dotenv
from groq import Groq
from retriever import retrieve

load_dotenv()

MODEL = "llama-3.3-70b-versatile"
TOP_K = 20

SYSTEM_PROMPT = """\
You are a running shoe assistant. Answer questions using ONLY the numbered passages \
provided by the user. Do not use your general training knowledge about running shoes \
or any information not present in the passages.

Rules:
- If the answer is clearly stated in the passages, answer directly and concisely.
- If the answer is not in the passages, say exactly: \
"I don't have enough information in my sources to answer that."
- Do not invent shoe names, prices, specifications, or opinions.
- Every claim you make must be traceable to one of the provided passages.\
"""

_client: Groq | None = None


def _get_client() -> Groq:
    global _client
    if _client is None:
        _client = Groq(api_key=os.environ["GROQ_API_KEY"])
    return _client


def generate(query: str) -> dict:
    """Return {"answer": str, "sources": list[str]}.
    Sources come from retrieved chunk metadata — not from the LLM.
    """
    hits = retrieve(query, top_k=TOP_K)

    passages = "\n\n".join(
        f"[{i + 1}] (Source: {h['source']})\n{h['text']}"
        for i, h in enumerate(hits)
    )
    user_message = (
        f"Passages:\n{passages}\n\n"
        f"Question: {query}\n\n"
        f"Answer based only on the passages above."
    )

    response = _get_client().chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0.1,
    )

    answer = response.choices[0].message.content
    # Deduplicate while preserving rank order — programmatic attribution
    sources = list(dict.fromkeys(h["source"] for h in hits))

    return {"answer": answer, "sources": sources}


if __name__ == "__main__":
    for q in [
        "What are the best running shoes offered by Adidas?",
        "According to Supwell, are On Cloudboom Strike LS worth the $330 price tag?",
        "What are the best daily trainers for stability?",
    ]:
        print(f"\nQ: {q}")
        result = generate(q)
        print(f"A: {result['answer']}")
        print(f"Sources: {', '.join(result['sources'][:3])} ...")
