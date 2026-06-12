import re


def splitter(
    text: str,
    page_number: int,
    chunk_id: int,
    window_size: int = 5,
    overlap: int = 1
) -> tuple[list[dict], int]:
    """
    Splits a given text into chunks based on sentence boundaries.

    Args:
        text: The input text to be split.
        page_number: The page number associated with the original document.
        chunk_id: Starting ID for the segments of this page.
        window_size: Number of sentences included in each chunk.
        overlap: Number of overlapping sentences between adjacent chunks.

    Returns:
        A tuple containing a list of chunk dictionaries and the final incremented chunk_id.
    """
    if window_size <= overlap:
        raise ValueError("window_size must be greater than overlap.")

    # Split by punctuation followed by optional whitespace to handle cases without spaces accurately
    raw_sentences = re.split(r'(?<=[.!؟])\s*', text)

    sentences = [
        s.strip()
        for s in raw_sentences
        if s.strip()
    ]

    stride = window_size - overlap
    chunks = []

    for start in range(0, len(sentences), stride):
        chunk_sentences = sentences[start : start + window_size]

        if not chunk_sentences:
            continue

        chunks.append({
            "page_number": page_number,
            "chunk_id": chunk_id,
            "text": " ".join(chunk_sentences)
        })

        chunk_id += 1

    return chunks, chunk_id
