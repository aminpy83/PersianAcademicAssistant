def splitter(
        text: str,
        page_number: int,
        chunk_id: int,
        window_size: int = 7,
        overlap: int = 2
):
    stride = window_size - overlap
    lines = []

    for line in text.splitlines():
        if line.strip():
            lines.append(line.strip())

    chunks = []

    for start in range(0, len(lines), stride):

        chunk_text = " ".join(
            lines[start:start + window_size]
        )

        if not chunk_text:
            continue

        chunks.append({
            "page_number": page_number,
            "chunk_id": chunk_id,
            "text": chunk_text,
            "line_start": start,
            "line_end": start + window_size
        })

        chunk_id += 1

    return chunks, chunk_id