import pymupdf


def extract_text(pdf_path: str):
    doc = pymupdf.open(pdf_path)
    for num, txt in enumerate(doc):
        yield {
            'page_number': num + 1,
            'text': txt.get_text()
        }
