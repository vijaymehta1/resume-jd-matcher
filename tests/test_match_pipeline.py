"""Phase 10 ke tests — poora match pipeline end-to-end.

`run_match` (app/app.py) ko resume PDF bytes + JD text deke check
karte hain: PDF nikalna -> JD validate -> TF-IDF + cosine score ->
skills -> result dict. Yehi wo rasta hai jo Streamlit app me chalta
hai, isliye iska test sabse zyada bharosa deta hai.

PDFs memory me bante hain (PyMuPDF) — disk pe kuch nahi likha jata.

Chalane ka command (project root se):
    .venv/bin/python tests/test_match_pipeline.py
"""

import importlib.util
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pymupdf

ROOT = Path(__file__).resolve().parents[1]

# app.py ko importlib se load karo (Phase 9 ki headless check jaisa),
# taaki Streamlit chalaye bina run_match test ho sake.
_spec = importlib.util.spec_from_file_location("rm_app", ROOT / "app" / "app.py")
_app = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_app)
run_match = _app.run_match

RESUME_TEXT = (
    "Rahul Sharma. Python developer with 3 years of experience in "
    "Machine Learning, Pandas, SQL and Git. Built data analysis "
    "projects using Python, NumPy and Statistics. Worked with Flask "
    "and MongoDB."
)

JD_TEXT = (
    "We are looking for a Python developer with strong skills in "
    "Machine Learning, Pandas and SQL. Experience with Docker and AWS "
    "is required. Knowledge of Git is a plus."
)

# Resume jisme JD se ek bhi word na mile (score 0.0 ke liye) —
# "experience" jaise aam words bhi nahi, taaki overlap bilkul zero ho.
NO_OVERLAP_RESUME = (
    "Chef cooking Italian food in restaurants. Baking bread, making "
    "pasta, grilling vegetables, serving customers daily."
)

EXPECTED_KEYS = {
    "score", "score_percent", "level", "matched_skills",
    "missing_skills", "matched_count", "missing_count", "summary",
}


def make_pdf_bytes(text):
    """Text se PDF bytes banao — memory me, disk pe nahi."""
    doc = pymupdf.open()
    page = doc.new_page()
    if text:
        page.insert_textbox((72, 72, 540, 750), text)
    return doc.tobytes()


def test_valid_pipeline():
    result = run_match(make_pdf_bytes(RESUME_TEXT), JD_TEXT)
    assert set(result.keys()) == EXPECTED_KEYS, f"keys galat: {result.keys()}"
    assert isinstance(result["score"], float)
    assert 0.0 <= result["score"] <= 1.0
    assert result["matched_count"] == len(result["matched_skills"])
    assert result["missing_count"] == len(result["missing_skills"])
    print(f"Case 1 (valid pipeline, score {result['score']}, "
          f"level {result['level']}): PASS")


def test_consistency():
    pdf = make_pdf_bytes(RESUME_TEXT)
    r1 = run_match(pdf, JD_TEXT)
    r2 = run_match(pdf, JD_TEXT)
    assert r1["score"] == r2["score"], "ek hi input pe score badal gaya"
    assert r1 == r2, "do baar same result aana chahiye"
    print("Case 2 (consistency, do baar same): PASS")


def test_identical_resume_jd():
    result = run_match(make_pdf_bytes(JD_TEXT), JD_TEXT)
    assert result["score"] > 0.6, f"identical text pe score {result['score']}"
    assert result["level"] == "High"
    print(f"Case 3 (identical resume-JD, score {result['score']}): PASS")


def test_no_overlap():
    result = run_match(make_pdf_bytes(NO_OVERLAP_RESUME), JD_TEXT)
    assert result["score"] == 0.0, f"no overlap pe score {result['score']}"
    assert result["level"] == "Low"
    print("Case 4 (no overlap, score 0.0): PASS")


def test_empty_pdf_bytes():
    try:
        run_match(b"", JD_TEXT)
    except ValueError:
        print("Case 5 (empty PDF bytes -> ValueError): PASS")
        return
    raise AssertionError("khaali PDF bytes pe ValueError aana chahiye tha")


def test_corrupt_pdf_bytes():
    try:
        run_match(b"not a pdf at all", JD_TEXT)
    except ValueError:
        print("Case 6 (corrupt bytes -> ValueError): PASS")
        return
    raise AssertionError("corrupt bytes pe ValueError aana chahiye tha")


def test_blank_pdf_scanned():
    try:
        run_match(make_pdf_bytes(""), JD_TEXT)
    except ValueError as e:
        assert "scanned" in str(e).lower(), f"message me scanned hona chahiye: {e}"
        print("Case 7 (blank/scanned PDF -> ValueError, scanned message): PASS")
        return
    raise AssertionError("blank PDF pe ValueError aana chahiye tha")


def test_empty_jd():
    try:
        run_match(make_pdf_bytes(RESUME_TEXT), "")
    except ValueError:
        print("Case 8 (empty JD -> ValueError): PASS")
        return
    raise AssertionError("khaali JD pe ValueError aana chahiye tha")


def test_short_jd():
    try:
        run_match(make_pdf_bytes(RESUME_TEXT), "Python developer needed")
    except ValueError:
        print("Case 9 (short JD -> ValueError): PASS")
        return
    raise AssertionError("chhoti JD pe ValueError aana chahiye tha")


def test_missing_skills_logic():
    result = run_match(make_pdf_bytes(RESUME_TEXT), JD_TEXT)
    assert "Docker" in result["missing_skills"], "Docker missing me hona chahiye"
    assert "AWS" in result["missing_skills"], "AWS missing me hona chahiye"
    assert "Python" in result["matched_skills"], "Python matched me hona chahiye"
    assert "Pandas" in result["matched_skills"], "Pandas matched me hona chahiye"
    print("Case 10 (missing/matched skills sahi): PASS")


def test_summary_text():
    result = run_match(make_pdf_bytes(RESUME_TEXT), JD_TEXT)
    assert str(result["score_percent"]) in result["summary"]
    assert result["level"] in result["summary"]
    print("Case 11 (summary me percent + level): PASS")


if __name__ == "__main__":
    test_valid_pipeline()
    test_consistency()
    test_identical_resume_jd()
    test_no_overlap()
    test_empty_pdf_bytes()
    test_corrupt_pdf_bytes()
    test_blank_pdf_scanned()
    test_empty_jd()
    test_short_jd()
    test_missing_skills_logic()
    test_summary_text()
    print("\nSab 11/11 cases PASS")
