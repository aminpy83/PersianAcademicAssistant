def splitter(text: str):
    sentences = []
    for line in text.splitlines():
        if not line.replace(' ', ''):
            continue
        sentences.append(line)
    sentences = tuple(sentences)

    paragraphs = {}
    ind = 1
    for i in range(2, len(sentences), 5):
        paragraphs[f'chunk{ind}'] = sentences[i - 2:i + 5]
        # pprint(f'chunk {ind}: {paragraphs[f'chunk{ind}']}')
        ind += 1
    return paragraphs
