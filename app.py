from modules.pdf_loader import extract_text
from modules.text_cleaner import cleaner
from modules.chunker import splitter
from pprint import pprint

text = extract_text("documents/persian_sample_for_project.pdf")

for page in text:
    normals = cleaner(page)
    chunks = splitter(normals)
    pprint(chunks)
