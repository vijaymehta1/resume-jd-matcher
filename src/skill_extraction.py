"""Phase 7: Skill extraction — resume aur JD me kaunsi skills hain.

Cosine score (Phase 6) sirf ye batata hai ki text KITNA match karta
hai. Skills batati hain ki KAUNSI skills match hui aur kaunsi JD me
maangi gayi par resume me nahi — user ke liye ye hi asli kaam ki
baat hai (kya seekhna baaki hai, ye yahin se pata chalta hai).

Skill list `data/skills.json` me hai — user apni skills us file me
add ya hata sakta hai, code badle bina.

Matching ke rules:
- Case-insensitive: "PYTHON" bhi "Python" se match karta hai.
- Word boundary: "Java" sirf tab match karega jab wo alag word ho —
  "JavaScript" ke andar "Java" nahi milega.
- Text aur skill dono ko Phase 4 ke `preprocess_text` se guzara
  jata hai (lowercase, clean), isliye "C++", "C#" aur "Node.js" bhi
  sahi se match karte hain, aur "Scikit-learn" bhi (clean karne pe
  "scikit learn" banta hai, dono taraf ek jaisa).
"""

import json
import re
from pathlib import Path

from src.preprocessing import preprocess_text

# data/skills.json ka default path: pehle diya hua path dekho, phir
# project root (src/ se do level upar) ke hisaab se.
_PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SKILLS_PATH = _PROJECT_ROOT / "data" / "skills.json"


def load_skills(path="data/skills.json"):
    """skills.json se skill names ki list load karo."""
    path = Path(path)
    if not path.exists():
        fallback = _PROJECT_ROOT / path
        path = fallback if fallback.exists() else path
    with open(path, encoding="utf-8") as f:
        skills = json.load(f)
    if not isinstance(skills, list) or not all(isinstance(s, str) for s in skills):
        raise ValueError("skills.json me strings ki list honi chahiye.")
    return skills


def _skill_pattern(skill):
    """Ek skill ke liye regex pattern banao.

    `\\b` (word boundary) "C++" jaise skills pe kaam nahi karta, kyunki
    `+` word character nahi hai — isliye lookaround use karte hain:
    skill ke pehle aur baad me koi word character nahi hona chahiye.
    Isi se "java" "javascript" ke andar match nahi karta, lekin
    "java" alag word ho to match karta hai.
    """
    cleaned = preprocess_text(skill)
    return re.compile(r"(?<!\w)" + re.escape(cleaned) + r"(?!\w)")


def extract_skills(text, skills):
    """Text me kaunsi skills (list se) milti hain, wo batao.

    Skills list ke order me return karta hai. Text jo bhi ho —
    resume ho ya JD — dono ko ek hi tareeke se check kiya jata hai.
    """
    if not isinstance(text, str):
        raise ValueError("Text ek string hona chahiye.")
    cleaned_text = preprocess_text(text)
    found = []
    for skill in skills:
        if _skill_pattern(skill).search(cleaned_text):
            found.append(skill)
    return found


def find_missing_skills(resume_skills, jd_skills):
    """JD me maangi gayi, par resume me na mili skills."""
    resume_set = set(resume_skills)
    return [s for s in jd_skills if s not in resume_set]


def find_matched_skills(resume_skills, jd_skills):
    """Resume aur JD dono me mili skills (overlap)."""
    jd_set = set(jd_skills)
    return [s for s in resume_skills if s in jd_set]
