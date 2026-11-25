"""Phase 8: Results display — jo Phases 6 aur 7 ne nikala, use dikhao.

Ye phase sirf DISPLAY karta hai — score ya skill lists ko badalta
nahi. Phase 6 ka match score aur Phase 7 ki matched/missing skills
ek jagah ikatthi karke dikhana hi iska kaam hai, taaki Phase 9 ka
Streamlit app ek hi dict se sab kuch dikha sake.
"""

# Phase 6 ke score se milta-julta level wapas laane ke liye band wahi
# hain jo similarity.py me hain: Low < 0.3, Medium 0.3-0.6, High > 0.6.


def format_results(match_result, matched_skills, missing_skills):
    """Match score + skill lists ko ek display-ready dict banao.

    `match_result` Phase 6 ke `match_score` ka dict hai
    ({"score", "score_percent", "level"}) — iska score bilkul waisa
    ka waisa rakha jata hai, koi naya score nahi banaya jata.
    """
    score = match_result["score"]
    score_percent = match_result["score_percent"]
    level = match_result["level"]
    matched = list(matched_skills)
    missing = list(missing_skills)
    return {
        "score": score,
        "score_percent": score_percent,
        "level": level,
        "matched_skills": matched,
        "missing_skills": missing,
        "matched_count": len(matched),
        "missing_count": len(missing),
        "summary": (
            f"Match {score_percent}% ({level}) — "
            f"{len(matched)} skills matched, {len(missing)} missing."
        ),
    }


def display_results(result_dict):
    """Result dict ko ek saaf, padhne layak text block banao.

    Ye function kuch print nahi karta — string return karta hai,
    taaki test karna aasan ho. Phase 9 ka Streamlit app isi text ko
    dikhayega.
    """
    score = result_dict["score"]
    score_percent = result_dict["score_percent"]
    level = result_dict["level"]
    matched = result_dict["matched_skills"]
    missing = result_dict["missing_skills"]

    lines = [
        "Resume–JD Match Result",
        f"Match Score: {score_percent}% ({level})  [score: {score}]",
    ]
    if matched:
        lines.append("Matched Skills: " + ", ".join(matched))
    else:
        lines.append("Matched Skills: koi nahi")
    if missing:
        lines.append("Missing Skills: " + ", ".join(missing))
    else:
        lines.append("Missing Skills: koi nahi")
    if missing:
        lines.append("Tip: In missing skills ko seekhne se match badhega.")
    else:
        lines.append("Tip: Saari JD skills resume me hain.")
    return "\n".join(lines)
