import pymupdf as fitz


def extract_text_from_pdf(uploaded_file):
    pdf_bytes = uploaded_file.getvalue()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    texts = []

    for page in doc:
        text = page.get_text()
        texts.append(text)

    full_text = "\n".join(texts)

    return full_text