import fitz
import pytesseract
from PIL import Image


def extract_text_from_scanned(pdf_path, scanned_pages):
    """
    Extract text from scanned PDF pages using OCR.
    """

    doc = fitz.open(pdf_path)

    extracted_text = ""

    for page_num in scanned_pages:

        page = doc.load_page(page_num)

        pix = page.get_pixmap(dpi=300)

        image = Image.frombytes(
            "RGB",
            [pix.width, pix.height],
            pix.samples
        )

        page_text = pytesseract.image_to_string(image)

        extracted_text += page_text + "\n"

    return extracted_text