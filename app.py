from modules.pdf_loader import extract_text
from modules.text_cleaner import cleaner

text = extract_text("documents/persian_sample_for_project.pdf")

for page in text:
    print(cleaner(page))

