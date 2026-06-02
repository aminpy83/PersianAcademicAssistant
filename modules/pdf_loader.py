from pymupdf import open

def extract_text(pdf_path: str):
    doc = open(pdf_path)
    for num, txt in enumerate(doc):
        yield {
            'page_number': num+1,
            'text': txt.get_text()
        }