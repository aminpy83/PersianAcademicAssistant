from pymupdf import open


def extract_text(pdf_path: str):
    doc = open(pdf_path)
    for num, txt in enumerate(doc):
        yield (f'num: {num + 1} \n \
               {txt.get_text()}')
