"""Phase 3: Job Description input — saaf karna aur validate karna.

Streamlit app (Phase 9) me JD ek bade text box me paste hogi. Usse pehle
ye module do kaam karta hai:
  1. clean — extra spaces/newlines/tabs ko single space me badlo.
  2. validate — khaali ya bahut chhoti JD ko roko, lambi JD ko aane do.

Koi truncation nahi: 5000+ characters ki JD bhi poori accept hoti hai.
"""

import re

MIN_JD_LENGTH = 50  # isse chhoti JD ka matlab — poori JD paste nahi hui


def clean_job_description(text):
    """JD text ko saaf karo: aas-paas ki whitespace hatao, andar ki
    multiple spaces/newlines/tabs ko ek single space me badlo."""
    if not isinstance(text, str):
        raise ValueError("Job description text hona chahiye.")
    cleaned = re.sub(r"\s+", " ", text).strip()
    return cleaned


def validate_job_description(text):
    """JD ko pehle saaf karo, phir check karo. Valid ho to saaf text
    return karo, warna ValueError.

    Rules:
    - khaali ya sirf whitespace -> ValueError
    - saaf karne ke baad 50 characters se chhoti -> ValueError
    - lambi JD (5000+ chars bhi) -> accept, no truncation
    """
    cleaned = clean_job_description(text)
    if not cleaned:
        raise ValueError("Job description khaali hai, JD paste karo.")
    if len(cleaned) < MIN_JD_LENGTH:
        raise ValueError(
            "Job description bahut chhoti hai, poori JD paste karo.")
    return cleaned
