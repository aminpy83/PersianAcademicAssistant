from modules.pdf_loader import extract_text
from modules.text_cleaner import cleaner
from modules.chunker import splitter
from pprint import pprint

pdf = extract_text("documents/persian_sample_for_project.pdf")

for page in pdf:
    normals = cleaner(page['text'])
    chunks = splitter(normals)
    pprint(chunks)
    print(f'page number: {page['page_number']} \n'
          f'page chunks: {len(chunks)}')