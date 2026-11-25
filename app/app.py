"""Resume–JD Matcher — Phase 9: Streamlit app.

Flow (4 kadam):
  1. User resume PDF upload karta hai + JD paste karta hai.
  2. "Check Match" dabane pe PDF ka text memory me nikala jata hai
     (upload kabhi disk pe nahi likha jata) aur JD validate hoti hai.
  3. Phase 6 match score nikalta hai, Phase 7 skills nikalta hai.
  4. Phase 8 ka format_results sab kuch ek dict me deta hai, app use
     dikhata hai.

Ye app ek educational prototype hai: score sirf TEXT similarity
batata hai, job milne ki probability ya candidate quality nahi.
"""

from pathlib import Path
import sys

import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.jd_input import validate_job_description  # noqa: E402
from src.pdf_extract import extract_text_from_pdf, has_extractable_text  # noqa: E402
from src.results import display_results, format_results  # noqa: E402
from src.similarity import match_score  # noqa: E402
from src.skill_extraction import (  # noqa: E402
    extract_skills,
    find_matched_skills,
    find_missing_skills,
    load_skills,
)


def run_match(resume_bytes, jd_text):
    """Resume PDF bytes + JD text se match result dict banao.

    Streamlit ke bina bhi test ho sakta hai (headless check).
    Returns: Phase 8 ka format_results dict
    (score, score_percent, level, matched_skills, missing_skills,
    matched_count, missing_count, summary).

    Raises:
        ValueError: corrupt/encrypted PDF, scanned PDF (koi text nahi),
            ya invalid JD (khaali / bahut chhoti).
    """
    resume_text = extract_text_from_pdf(resume_bytes)
    if not has_extractable_text(resume_text):
        raise ValueError(
            "Resume scanned lagta hai — isme padhne layak text nahi mila. "
            "Scanned resume ke liye OCR abhi supported nahi hai."
        )
    jd_clean = validate_job_description(jd_text)

    skills = load_skills()
    match_result = match_score(resume_text, jd_clean)
    resume_skills = extract_skills(resume_text, skills)
    jd_skills = extract_skills(jd_clean, skills)
    matched = find_matched_skills(resume_skills, jd_skills)
    missing = find_missing_skills(resume_skills, jd_skills)

    return format_results(match_result, matched, missing)


def main():
    st.title("Resume–JD Matcher")
    st.write("Resume aur Job Description kitne milte hain, ye check karo. "
             "Ye ek educational prototype hai — score sirf text similarity "
             "batata hai, job milne ki probability ya candidate quality nahi.")

    uploaded = st.file_uploader("Resume PDF upload karo", type=["pdf"])
    jd_text = st.text_area("Job Description paste karo", height=200)

    if st.button("Check Match"):
        if uploaded is None:
            st.error("Pehle resume PDF upload karo.")
            return
        if not jd_text.strip():
            st.error("Job description paste karo.")
            return
        try:
            result = run_match(uploaded.getvalue(), jd_text)
        except ValueError as e:
            st.error(str(e))
            return

        st.subheader("Result")
        st.write(f"Match Score: **{result['score_percent']}% "
                 f"({result['level']})**")
        if result["matched_skills"]:
            st.write("Matched Skills: " + ", ".join(result["matched_skills"]))
        else:
            st.write("Matched Skills: koi nahi")
        if result["missing_skills"]:
            st.write("Missing Skills: " + ", ".join(result["missing_skills"]))
        else:
            st.write("Missing Skills: koi nahi")

        st.subheader("Full Result")
        st.code(display_results(result))


if __name__ == "__main__":
    # Project root se chalao: .venv/bin/streamlit run app/app.py
    main()
