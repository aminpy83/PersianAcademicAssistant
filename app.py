from modules.pdf_loader import extract_text
from modules.text_cleaner import cleaner
from modules.chunker import splitter
from modules.embedding import get_embedding
from pprint import pprint

pdf = extract_text("documents/persian_sample_for_project.pdf")

for page in pdf:
    normals = cleaner(page['text'])
    # pprint(normals)
    chunks = splitter(normals, page['page_number'])
    # pprint(chunks)
    vector = get_embedding(chunks[0]['text'])
    print(type(vector))
    print(vector.shape)