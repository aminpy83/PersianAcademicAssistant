import numpy as np
from modules.pdf_loader import extract_text
from modules.text_cleaner import cleaner
from modules.chunker import splitter
from modules.embedding import get_embedding
from modules.vector_store import build_index, search
from modules.reetriver import retrieve
from pprint import pprint

pdf = extract_text("documents/persian_sample_for_project.pdf")

all_chunks = []
all_vectors = []
chunk_id = 1
for page in pdf:
    normals = cleaner(page['text'])
    chunks, chunk_id = splitter(normals, page['page_number'], chunk_id)

    for chunk in chunks:
        vector = get_embedding(chunk['text']).astype("float32")

        chunk['embedding'] = vector

        all_chunks.append(chunk)
        all_vectors.append(vector)

all_vectors = np.array(all_vectors, dtype="float32")

index = build_index(all_vectors)
print(index.ntotal)
query = "معماری پیشنهادی چیست؟"

results = retrieve(
    query=query,
    index=index,
    chunks=all_chunks,
    k=3
)

for item in results:
    print("=" * 50)
    print(item["page_number"])
    print(item["chunk_id"])
    print(item["text"])
