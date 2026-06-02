def splitter(text: str):
    sentences = []
    for line in text.splitlines():
        if not line.replace(' ', ''):
            continue
        sentences.append(line)
    return sentences
