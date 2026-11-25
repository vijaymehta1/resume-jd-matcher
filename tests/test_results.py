"""Phase 8 ke tests — results display (plain asserts, pytest nahi).

Chalane ka command (project root se):
    .venv/bin/python tests/test_results.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.results import display_results, format_results

# Phase 6 ke match_score jaisa dict (score yahin se aata hai)
SAMPLE_MATCH = {"score": 0.42, "score_percent": 42.0, "level": "Medium"}
MATCHED = ["Python", "SQL", "Pandas"]
MISSING = ["Docker", "FastAPI"]


def test_case(name, fn):
    fn()
    print(f"{name}: PASS")


def test_score_kept_exact():
    result = format_results(SAMPLE_MATCH, MATCHED, MISSING)
    assert result["score"] == 0.42, f"score waisa ka waisa rehna chahiye: {result['score']}"
    assert result["score_percent"] == 42.0
    assert result["level"] == "Medium"


def test_counts_right():
    result = format_results(SAMPLE_MATCH, MATCHED, MISSING)
    assert result["matched_count"] == 3, f"matched_count 3 hona chahiye: {result['matched_count']}"
    assert result["missing_count"] == 2, f"missing_count 2 hona chahiye: {result['missing_count']}"


def test_summary_line():
    result = format_results(SAMPLE_MATCH, MATCHED, MISSING)
    summary = result["summary"]
    assert "42.0%" in summary, f"summary me percent hona chahiye: {summary}"
    assert "Medium" in summary, f"summary me level hona chahiye: {summary}"
    assert "3 skills matched" in summary
    assert "2 missing" in summary


def test_display_contains_everything():
    result = format_results(SAMPLE_MATCH, MATCHED, MISSING)
    text = display_results(result)
    assert "42.0%" in text, "text me score percent hona chahiye"
    assert "Python" in text and "SQL" in text and "Pandas" in text
    assert "Docker" in text and "FastAPI" in text
    assert "Matched Skills" in text
    assert "Missing Skills" in text


def test_empty_missing_skills():
    result = format_results(SAMPLE_MATCH, MATCHED, [])
    assert result["missing_count"] == 0
    text = display_results(result)
    assert "Saari JD skills resume me hain." in text
    assert "Missing Skills: koi nahi" in text


def test_empty_matched_skills():
    result = format_results(SAMPLE_MATCH, [], MISSING)
    assert result["matched_count"] == 0
    text = display_results(result)
    assert "Matched Skills: koi nahi" in text
    assert "In missing skills ko seekhne se match badhega." in text


def test_display_returns_string():
    result = format_results(SAMPLE_MATCH, MATCHED, MISSING)
    text = display_results(result)
    assert isinstance(text, str), "display_results ko string return karni chahiye"
    assert len(text.splitlines()) >= 5, "text me kam se kam 5 lines honi chahiye"


if __name__ == "__main__":
    test_case("Case 1 (score bilkul waisa ka waisa)", test_score_kept_exact)
    test_case("Case 2 (matched/missing counts sahi)", test_counts_right)
    test_case("Case 3 (summary line me percent + level)", test_summary_line)
    test_case("Case 4 (display text me score + skills)", test_display_contains_everything)
    test_case("Case 5 (missing skills khaali)", test_empty_missing_skills)
    test_case("Case 6 (matched skills khaali)", test_empty_matched_skills)
    test_case("Case 7 (display string return karta hai)", test_display_returns_string)
    print("\nSab 7/7 cases PASS")
