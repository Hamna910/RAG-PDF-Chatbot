from pypdf import PdfReader


def load_pdf(pdf_path):
    """
    Load PDF and extract text.
    Returns:
        text (str): Extracted text
        scanned_pages (list): Pages where no text was found
    """

    reader = PdfReader(pdf_path)

    text = ""
    scanned_pages = []

    for page_num, page in enumerate(reader.pages):

        page_text = page.extract_text()

        if page_text and page_text.strip():
            text += page_text + "\n"

        else:
            scanned_pages.append(page_num)

    return text, scanned_pages