"""Phase 7 ke tests — skill extraction (plain asserts, pytest nahi).

Chalane ka command (project root se):
    .venv/bin/python tests/test_skill_extraction.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.skill_extraction import (
    extract_skills,
    find_matched_skills,
    find_missing_skills,
    load_skills,
)

SKILLS = load_skills()

RESUME_TEXT = (
    "I am a Python developer with experience in SQL, Pandas and "
    "Machine Learning. I also know C++ and Docker, and I use Git daily."
)
JD_TEXT = (
    "We need a Python developer with Machine Learning, Deep Learning, "
    "TensorFlow and AWS experience. SQL is a plus."
)


def test_case(name, fn):
    fn()
    print(f"{name}: PASS")


def test_extracts_python_sql():
    found = extract_skills(RESUME_TEXT, SKILLS)
    assert "Python" in found and "SQL" in found, found


def test_case_insensitive():
    found = extract_skills("I know PYTHON and pandas.", SKILLS)
    assert "Python" in found and "Pandas" in found, found


def test_java_not_inside_javascript():
    found = extract_skills("I build apps in JavaScript and React.", SKILLS)
    assert "JavaScript" in found, found
    assert "Java" not in found, found


def test_multiword_skill():
    found = extract_skills("My field is Machine Learning.", SKILLS)
    assert "Machine Learning" in found, found


def test_skill_not_in_text_not_returned():
    found = extract_skills("I only know Python.", SKILLS)
    assert "Docker" not in found and "TensorFlow" not in found, found


def test_special_char_skills():
    found = extract_skills("I write C++ and use Node.js.", SKILLS)
    assert "C++" in found and "Node.js" in found, found


def test_missing_skills():
    resume = extract_skills(RESUME_TEXT, SKILLS)
    jd = extract_skills(JD_TEXT, SKILLS)
    missing = find_missing_skills(resume, jd)
    assert "Deep Learning" in missing and "TensorFlow" in missing, missing
    assert "Python" not in missing and "SQL" not in missing, missing


def test_matched_skills():
    resume = extract_skills(RESUME_TEXT, SKILLS)
    jd = extract_skills(JD_TEXT, SKILLS)
    matched = find_matched_skills(resume, jd)
    assert "Python" in matched and "SQL" in matched, matched
    assert "Machine Learning" in matched, matched
    assert "AWS" not in matched, matched


def test_load_skills():
    skills = load_skills()
    assert isinstance(skills, list) and len(skills) > 0, skills
    for must in ("Python", "SQL", "Machine Learning", "Docker", "Git"):
        assert must in skills, must


if __name__ == "__main__":
    test_case("Case 1 (Python + SQL mile)", test_extracts_python_sql)
    test_case("Case 2 (case-insensitive: PYTHON)", test_case_insensitive)
    test_case("Case 3 (Java, JavaScript ke andar nahi)", test_java_not_inside_javascript)
    test_case("Case 4 (multi-word: Machine Learning)", test_multiword_skill)
    test_case("Case 5 (na ho skill, na mile)", test_skill_not_in_text_not_returned)
    test_case("Case 6 (C++ aur Node.js mile)", test_special_char_skills)
    test_case("Case 7 (missing skills: Deep Learning, TensorFlow)", test_missing_skills)
    test_case("Case 8 (matched skills: Python, SQL, ML)", test_matched_skills)
    test_case("Case 9 (load_skills: list non-empty)", test_load_skills)
    print("\nSab 9/9 cases PASS")
