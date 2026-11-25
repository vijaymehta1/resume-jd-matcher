"""Resume PDF se text nikalna (Phase 2).

Kaam: diye gaye PDF (file path ya bytes) ka saara text nikalna.
- Text-layer wale PDFs ke liye kaam karta hai (Word/LaTeX se bane resume).
- Scanned / image-only PDFs me text layer nahi hota, isliye unse "" milega.
  Unke liye OCR chahiye (jaise Tesseract) jo is phase me installed nahi hai;
  OCR ek future option hai, is phase ka hissa nahi.

Uploaded file kabhi disk pe save nahi hoti: bytes seedha memory me khulte hain.
"""

from pathlib import Path

import pymupdf


def extract_text_from_pdf(pdf_source):
    """PDF ka text nikalta hai.

    pdf_source: file path (str ya Path) ya raw bytes
        (jaise Streamlit UploadedFile se .read() / .getvalue() mile).

    Returns:
        Saare pages ka text, pages ke beech "\\n" ke saath.
        Agar PDF me koi text nahi hai (blank ya scanned) to "".

    Raises:
        ValueError: agar input valid PDF nahi hai, corrupt hai,
            ya encrypted hai (bina password ke khul nahi sakta).
    """
    if isinstance(pdf_source, (str, Path)):
        path = Path(pdf_source)
        if not path.is_file():
            raise ValueError("File nahi mili: " + str(path))
        pdf_bytes = path.read_bytes()
    elif isinstance(pdf_source, (bytes, bytearray)):
        pdf_bytes = bytes(pdf_source)
    else:
        raise ValueError("PDF file path ya bytes do.")

    if not pdf_bytes:
        raise ValueError("Khaali file hai, PDF nahi hai.")

    try:
        doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    except Exception:
        raise ValueError("Ye valid PDF nahi hai.")

    try:
        if doc.is_encrypted:
            raise ValueError("Ye PDF encrypted hai, bina password ke khul nahi sakti.")
        pages_text = []
        for page in doc:
            pages_text.append(page.get_text().strip())
        return "\n".join(pages_text).strip()
    finally:
        doc.close()


def has_extractable_text(text):
    """Batata hai ki nikle hue text me padhne layak kuch hai ya nahi.

    Scanned PDF se "" milta hai, to ye False dega; matlab
    us resume ka text OCR ke bina nahi padha ja sakta.
    """
    return bool(text and text.strip())
