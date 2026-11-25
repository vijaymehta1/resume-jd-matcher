"""Phase 3 tests — plain asserts, pytest nahi.
Run: .venv/bin/python tests/test_jd_input.py   (project root se)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.jd_input import clean_job_description, validate_job_description

VALID_JD = (
    "We are hiring a Python Developer with experience in Machine Learning, "
    "SQL and data analysis. The candidate will build models and work with "
    "large datasets using Pandas and Scikit-learn."
)


def expect_error(fn, arg, label):
    try:
        fn(arg)
    except ValueError:
        print(f"{label}: PASS")
        return
    raise AssertionError(f"{label}: FAIL — ValueError nahi aaya")


# Case 1: valid JD pass kare aur cleaned text return kare
result = validate_job_description(VALID_JD)
assert result == VALID_JD.strip(), "valid JD waisi ki waisi return honi chahiye"
print("Case 1 (valid JD): PASS")

# Case 2: khaali string -> ValueError
expect_error(validate_job_description, "", "Case 2 (khaali string)")

# Case 3: sirf whitespace -> ValueError
expect_error(validate_job_description, "   \n\t  ", "Case 3 (whitespace-only)")

# Case 4: bahut chhoti JD -> ValueError
expect_error(validate_job_description, "Python developer",
             "Case 4 (chhoti JD)")

# Case 5: lambi JD (~5000 chars) pass kare, truncate na ho
long_jd = ("We need a data scientist. " * 200).strip()
assert len(long_jd) > 5000, "test JD 5000 chars se badi honi chahiye"
result = validate_job_description(long_jd)
assert result == long_jd, "lambi JD poori return honi chahiye, truncate nahi"
print("Case 5 (lambi JD ~5000 chars): PASS")

# Case 6: None -> ValueError
expect_error(validate_job_description, None, "Case 6 (None input)")
expect_error(clean_job_description, None, "Case 6b (clean + None)")

# Case 7: number input -> ValueError
expect_error(validate_job_description, 12345, "Case 7 (number input)")

# Case 8: gadbad whitespace single space me badle
messy = "Python\n\n   SQL\t\t ML"
assert clean_job_description(messy) == "Python SQL ML", "whitespace collapse"
print("Case 8 (messy whitespace): PASS")

print("\nSab 8/8 cases PASS")
