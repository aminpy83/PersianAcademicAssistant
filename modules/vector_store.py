from faiss import IndexFlatL2


def build_index(vectors):
    dimension = vectors.shape[1]

    index = IndexFlatL2(dimension)

    index.add(vectors)

    return index


def search(index, query_vector, k=3):
    ...
