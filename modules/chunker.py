def splitter(text: str, page_number: int, chunk_id: int):
    sentences = []
    for line in text.splitlines():
        if not line.strip():
            continue
        sentences.append(line)
    sentences = tuple(sentences)

    paragraphs = []  # chunks

    for i in range(2, len(sentences), 5):
        paragraphs.append({
            'page_number': page_number,
            'chunk_id': chunk_id,
            'text': ' '.join(sentences[i - 2:i + 5])
        })
        chunk_id += 1

    return paragraphs, chunk_id
