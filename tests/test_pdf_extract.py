"""Phase 2 ke tests (pytest nahi, plain asserts).

Run: .venv/bin/python tests/test_pdf_extract.py
"""

import sys
from pathlib import Path

import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.pdf_extract import extract_text_from_pdf, has_extractable_text


def make_pdf_with_text(lines):
    """Text wali 1-page PDF memory me banata hai, bytes deta hai."""
    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_textbox(pymupdf.Rect(72, 72, 500, 700), "\n".join(lines))
    pdf_bytes = doc.tobytes()
    doc.close()
    return pdf_bytes


def make_blank_pdf():
    """Khaali page wali PDF memory me banata hai."""
    doc = pymupdf.open()
    doc.new_page()
    pdf_bytes = doc.tobytes()
    doc.close()
    return pdf_bytes


def main():
    passed = 0

    # Case 1: valid resume PDF (bytes) — skills wala text milna chahiye
    resume_lines = [
        "Vijay Mehta",
        "Skills: Python, SQL, Machine Learning",
        "B.Tech Computer Science",
    ]
    text = extract_text_from_pdf(make_pdf_with_text(resume_lines))
    assert "Python" in text and "SQL" in text and "Machine Learning" in text, text
    assert has_extractable_text(text) is True
    print("Case 1 (valid PDF, bytes): PASS")
    passed += 1

    # Case 2: valid PDF file path se bhi chalna chahiye
    tmp_path = Path(__file__).resolve().parent / "_tmp_resume.pdf"
    tmp_path.write_bytes(make_pdf_with_text(resume_lines))
    try:
        text2 = extract_text_from_pdf(tmp_path)
        assert "Python" in text2, text2
        print("Case 2 (valid PDF, file path): PASS")
        passed += 1
    finally:
        tmp_path.unlink(missing_ok=True)

    # Case 3: blank-page PDF — text nahi, "" mile
    blank_text = extract_text_from_pdf(make_blank_pdf())
    assert blank_text == "", repr(blank_text)
    assert has_extractable_text(blank_text) is False
    print("Case 3 (blank PDF): PASS")
    passed += 1

    # Case 4: corrupt bytes — ValueError aana chahiye
    try:
        extract_text_from_pdf(b"not a pdf")
    except ValueError:
        print("Case 4 (corrupt bytes): PASS")
        passed += 1
    else:
        raise AssertionError("corrupt bytes pe ValueError nahi aaya")

    # Case 5: khaali bytes — ValueError aana chahiye
    try:
        extract_text_from_pdf(b"")
    except ValueError:
        print("Case 5 (empty bytes): PASS")
        passed += 1
    else:
        raise AssertionError("empty bytes pe ValueError nahi aaya")

    print(f"\nSab {passed}/5 cases PASS")


if __name__ == "__main__":
    main()
