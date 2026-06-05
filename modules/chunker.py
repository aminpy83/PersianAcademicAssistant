import re


def splitter(
        text: str,
        page_number: int,
        chunk_id: int,
        window_size: int = 5,
        overlap: int = 1
):

    sentences = re.split(
        r'(?<=[.!؟])\s+',
        text
    )

    sentences = [
        s.strip()
        for s in sentences
        if s.strip()
    ]

    stride = window_size - overlap

    chunks = []

    for start in range(
            0,
            len(sentences),
            stride
    ):

        chunk_sentences = sentences[
            start:start + window_size
        ]

        if not chunk_sentences:
            continue

        chunks.append({
            "page_number": page_number,
            "chunk_id": chunk_id,
            "text": " ".join(chunk_sentences)
        })

        chunk_id += 1

    return chunks, chunk_id