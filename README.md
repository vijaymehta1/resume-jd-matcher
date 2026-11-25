# Resume–Job Description Matching System

Resume (PDF) + Job Description daalo → TF-IDF + Cosine Similarity se match score,
aur skills ka hisaab: kaunsi skills match hui, kaunsi JD me hain par resume me nahi.

**Ye ek educational NLP prototype hai — automated hiring ya rejection system NAHI hai.**
Score sirf text similarity batata hai, candidate ki quality ya job milne ki
probability nahi.

## Project structure

```
resume-jd-matcher/
├── README.md                  # ye file
├── requirements.txt           # saari libraries, fixed versions ke saath
├── .gitignore                 # git me kya nahi jayega (uploaded resumes kabhi nahi)
├── .venv/                     # virtual environment (git me nahi jata)
├── data/                      # Phase 7: skills.json ; Phase 10: sample resume + sample JD
├── src/                       # Phase 2 se: pdf_extract.py, preprocessing.py,
│   │                          # vectorizer.py, similarity.py, skills.py
│   └── __init__.py
├── app/                       # Phase 9: app.py (Streamlit app)
├── tests/                     # Phase 10: tests
└── reports/                   # Phase 13: internship report content
```

## Setup

```bash
# virtual environment banao (ek baar)
python3 -m venv .venv

# activate karo
source .venv/bin/activate        # Linux / Mac
# .venv\Scripts\activate        # Windows

# libraries install karo
pip install -r requirements.txt
```

## Run

Streamlit app Phase 9 me banega — abhi app run nahi hota.

```bash
# Phase 9 ke baad:
.venv/bin/streamlit run app/app.py
```

## Ek faisla (Phase 1 me liya gaya)

NLTK ya spaCy Phase 1 me install **nahi** kiye. Phase 4 ki preprocessing ke liye
shuru me sklearn ke built-in English stop words + simple regex tokenization kaafi
hain. Agar Phase 4 me lemmatization ki asli zaroorat padi to tab dobara dekhenge —
bina wajah heavy library nahi daalni.

## Privacy

Uploaded resume kabhi repo me save nahi hoga — sirf memory/temp me process hoga.
`.gitignore` me `*.pdf` isiliye block hai (sirf `data/sample_resume.pdf` test file
ko chhoot hai).

## Status

- Phase 1: Project setup — done
- Phase 2: Resume PDF text extraction (`src/pdf_extract.py`, PyMuPDF) — done
- Phase 3: Job description input — cleaning + validation (`src/jd_input.py`) — done
- Phase 4: NLP preprocessing (`src/preprocessing.py`) — done. Lemmatization nahi hai: TF-IDF is prototype ke liye bina lemmatization ke theek kaam karta hai, NLTK/spaCy bhaari download hota.
- Phase 5: TF-IDF vectorization (`src/vectorizer.py`) — done. Phase 4 ka preprocess_text preprocessor hai aur tokenize tokenizer hai, taaki "c++"/"c#"/"node.js" ek term rahein.
- Phase 6: Cosine similarity (`src/similarity.py`) — done. `match_score` resume aur JD ka score 0-1 me deta hai (Low < 0.3, Medium 0.3-0.6, High > 0.6); score sirf TEXT similarity hai, job milne ki probability ya candidate quality nahi.
- Phase 7: Skill extraction (`src/skill_extraction.py` + `data/skills.json`) — done. `extract_skills` case-insensitive, word-boundary matching karta hai ("Java" JavaScript ke andar nahi milta; "C++"/"Node.js"/"Scikit-learn" sahi match hote hain); `find_missing_skills` aur `find_matched_skills` JD vs resume ka hisaab dete hain. Skills list `data/skills.json` me editable hai.
- Phase 8: Results display (`src/results.py`) — done. `format_results` Phase 6 ka score bilkul waisa ka waisa rakhta hai aur matched/missing skills + counts + summary line ek dict me deta hai; `display_results` saaf text block return karta hai (score, matched skills, missing skills, tip line). Ye phase kuch compute nahi karta, sirf dikhata hai.
- Phase 9: Streamlit app (`app/app.py`) — done. Resume PDF upload + JD text area + "Check Match" button; `run_match(resume_bytes, jd_text)` saara kaam karta hai (PDF text nikalna, JD validate, match score, skills, format_results) aur Phase 8 ka dict deta hai; upload kabhi disk pe nahi likha jata; corrupt/scanned PDF aur invalid JD pe st.error dikhta hai, traceback nahi. Verify: headless check me sample resume + JD pe score 48.6% (Medium), 7 matched / 1 missing (FastAPI); live smoke test HTTP 200.
- Phase 10: Testing (`tests/test_match_pipeline.py`) — done. `run_match` ka end-to-end test: 11 cases PASS (valid pipeline, consistency, identical resume-JD score 1.0 High, no overlap score 0.0 Low, empty/corrupt/blank PDF pe ValueError, empty/short JD pe ValueError, missing/matched skills logic, summary text). PDFs memory me bante hain, disk pe kuch nahi. Regression: Phases 2–8 ke tests (5/5, 8/8, 15/15, 6/6, 10/10, 9/9, 7/7) sab PASS — kul 71 cases.
- Phase 11: Deployment preparation — done. `.streamlit/config.toml`
  (minimal) aur `DEPLOYMENT.md` (GitHub `vijaymehta1/resume-jd-matcher`
  → Streamlit Cloud steps, deploy ke baad test karne ka tareeka)
  banaye. Verify kiya: `data/skills.json`, `requirements.txt`,
  `app/app.py` aur saare `src/` modules tracked hain; `.gitignore`
  runtime pe chahiye hone wali koi file nahi rokta. Asli push/deploy
  abhi baaki hai — GitHub authorization pending hai.
- Phase 12–13: pending
