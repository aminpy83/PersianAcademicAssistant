from modules.embedding import get_embedding
from modules.vector_store import search


def retrieve(query: str, index, chunks: list, k: int = 3):
    query_vector = get_embedding(query).astype("float32")

    indices = search(index, query_vector, k)

    results = []
    for idx in indices:
        results.append(
            chunks[idx]
        )

    return results
