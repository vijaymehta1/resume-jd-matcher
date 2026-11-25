"""Phase 6 ke tests — cosine similarity (plain asserts, pytest nahi).

Chalane ka command (project root se):
    .venv/bin/python tests/test_similarity.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np

from src.similarity import cosine_similarity_score, match_score
from src.vectorizer import fit_vectorizer

IDENTICAL_RESUME = "Python machine learning pandas sql"
IDENTICAL_JD = "Python machine learning pandas sql"

DIFFERENT_RESUME = "Python machine learning pandas sql"
DIFFERENT_JD = "cooking baking recipes kitchen chef"

# Aadha overlap: score 0.3-0.6 ke beech aata hai (Medium band)
PARTIAL_RESUME = "Python machine learning data analysis sql pandas"
PARTIAL_JD = "Python machine learning deep learning neural networks tensorflow"


def test_case(name, fn):
    fn()
    print(f"{name}: PASS")


def test_identical_texts_score_one():
    result = match_score(IDENTICAL_RESUME, IDENTICAL_JD)
    assert result["score"] >= 0.99, f"identical ka score 1.0 hona chahiye, mila {result['score']}"
    assert result["score_percent"] >= 99.0
    assert result["level"] == "High"


def test_different_texts_score_zero():
    result = match_score(DIFFERENT_RESUME, DIFFERENT_JD)
    assert result["score"] == 0.0, f"alag texts ka score 0.0 hona chahiye, mila {result['score']}"
    assert result["level"] == "Low"


def test_empty_resume_zero():
    result = match_score("", "Python developer needed for backend work")
    assert result["score"] == 0.0
    assert result["level"] == "Low"


def test_empty_jd_zero():
    result = match_score("Python developer with django experience", "")
    assert result["score"] == 0.0
    assert result["level"] == "Low"


def test_whitespace_only_zero():
    result = match_score("   \n\t  ", "Python developer needed")
    assert result["score"] == 0.0
    assert result["level"] == "Low"


def test_score_always_between_zero_and_one():
    pairs = [
        (IDENTICAL_RESUME, IDENTICAL_JD),
        (DIFFERENT_RESUME, DIFFERENT_JD),
        (PARTIAL_RESUME, PARTIAL_JD),
        ("Python sql", "Java spring hibernate"),
        ("data science machine learning", "data science machine learning deep learning"),
    ]
    for resume, jd in pairs:
        score = match_score(resume, jd)["score"]
        assert 0.0 <= score <= 1.0, f"score range se bahar: {score}"


def test_partial_score_in_between():
    identical = match_score(IDENTICAL_RESUME, IDENTICAL_JD)["score"]
    different = match_score(DIFFERENT_RESUME, DIFFERENT_JD)["score"]
    partial = match_score(PARTIAL_RESUME, PARTIAL_JD)["score"]
    assert different < partial < identical, (
        f"partial score beech me hona chahiye: {different} < {partial} < {identical}")


def test_level_bands():
    assert match_score(IDENTICAL_RESUME, IDENTICAL_JD)["level"] == "High"
    assert match_score(DIFFERENT_RESUME, DIFFERENT_JD)["level"] == "Low"
    partial = match_score(PARTIAL_RESUME, PARTIAL_JD)
    assert 0.3 <= partial["score"] <= 0.6, f"partial score Medium band me hona chahiye: {partial['score']}"
    assert partial["level"] == "Medium"
    high = match_score("Python sql pandas data analysis machine learning",
                       "Python sql pandas data analysis")
    assert high["score"] > 0.6 and high["level"] == "High"


def test_passed_fitted_vectorizer():
    vectorizer, _ = fit_vectorizer([PARTIAL_RESUME, PARTIAL_JD])
    with_vec = match_score(PARTIAL_RESUME, PARTIAL_JD, vectorizer=vectorizer)
    without_vec = match_score(PARTIAL_RESUME, PARTIAL_JD)
    assert with_vec["score"] == without_vec["score"], (
        f"fitted vectorizer se same score aana chahiye: {with_vec} vs {without_vec}")


def test_cosine_direct_vectors():
    # Bilkul alag direction -> 0.0 ; ek hi direction -> 1.0
    assert cosine_similarity_score(np.array([[1.0, 0.0]]),
                                   np.array([[0.0, 1.0]])) == 0.0
    assert cosine_similarity_score(np.array([[1.0, 2.0]]),
                                   np.array([[1.0, 2.0]])) >= 0.99


if __name__ == "__main__":
    test_case("Case 1 (identical texts -> 1.0, High)", test_identical_texts_score_one)
    test_case("Case 2 (different texts -> 0.0, Low)", test_different_texts_score_zero)
    test_case("Case 3 (empty resume -> 0.0)", test_empty_resume_zero)
    test_case("Case 4 (empty JD -> 0.0)", test_empty_jd_zero)
    test_case("Case 5 (whitespace-only -> 0.0)", test_whitespace_only_zero)
    test_case("Case 6 (score hamesha 0-1 ke beech)", test_score_always_between_zero_and_one)
    test_case("Case 7 (partial score beech me)", test_partial_score_in_between)
    test_case("Case 8 (level bands Low/Medium/High)", test_level_bands)
    test_case("Case 9 (fitted vectorizer pass karke)", test_passed_fitted_vectorizer)
    test_case("Case 10 (cosine direct vectors)", test_cosine_direct_vectors)
    print("\nSab 10/10 cases PASS")
