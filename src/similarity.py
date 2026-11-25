"""Phase 6: Cosine Similarity — resume aur JD kitne milte-julte hain.

Plain words me cosine similarity:
- Har document ko TF-IDF vector samjho — ek teer (arrow) jo ek
  direction me point karta hai.
- Cosine similarity do teeron ke beech ka angle batata hai:
  angle 0 (ek hi direction) = 1.0, matlab dono text ek jaise hain;
  angle 90 degree (bilkul alag direction) = 0.0, matlab dono me
  ek bhi common word nahi hai.
- TF-IDF vectors me kabhi negative value nahi hoti, isliye score
  hamesha 0 aur 1 ke beech rehta hai.

SAF SAMAJH: ye score sirf TEXT ki milti-julti batata hai — na ye
job milne ki probability hai, na candidate ki quality ka measure.
Ek achha resume galat shabdon me likha ho to score kam aa sakta hai,
aur ek kharab resume sahi keywords se bhara ho to score zyada.
"""

from sklearn.metrics.pairwise import cosine_similarity

from src.preprocessing import preprocess_text
from src.vectorizer import fit_vectorizer


def cosine_similarity_score(vec_a, vec_b):
    """Do TF-IDF vectors ke beech cosine similarity (sklearn se).

    TF-IDF vectors ke liye score hamesha 0 aur 1 ke beech hota hai;
    floating point ki chhoti galti ko range me clip kar dete hain.
    """
    score = float(cosine_similarity(vec_a, vec_b)[0][0])
    return max(0.0, min(1.0, score))


def _level(score):
    """Score ko Low / Medium / High band me daalo."""
    if score < 0.3:
        return "Low"
    if score <= 0.6:
        return "Medium"
    return "High"


def match_score(resume_text, jd_text, vectorizer=None):
    """Resume aur JD ka match score nikalo.

    vectorizer=None ho to Phase 5 ka TF-IDF in dono texts pe fit
    hota hai; pehle se fitted vectorizer diya ho to usi se dono
    texts transform hote hain. Preprocessing dobara nahi likhi —
    vectorizer ke andar Phase 4 ka preprocess_text hi chalta hai.

    Returns: {"score": 0.42, "score_percent": 42.0, "level": "Medium"}
    Khaali resume ya khaali JD (preprocessing ke baad) ka score 0.0
    hota hai, level "Low".
    """
    # Dono me se koi ek bhi khaali ho to fit karne ka matlab nahi
    if not preprocess_text(resume_text) or not preprocess_text(jd_text):
        return {"score": 0.0, "score_percent": 0.0, "level": "Low"}

    if vectorizer is None:
        _, matrix = fit_vectorizer([resume_text, jd_text])
    else:
        matrix = vectorizer.transform([resume_text, jd_text])

    score = cosine_similarity_score(matrix[0], matrix[1])
    return {
        "score": round(score, 4),
        "score_percent": round(score * 100, 1),
        "level": _level(score),
    }
