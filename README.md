# Resume–Job Description Matching System

An educational NLP prototype that compares a resume (PDF) with a job
description and tells you how well the two texts match — a match
score, which skills match, and which skills the job asks for but the
resume does not have.

**This is an educational prototype, NOT an automated hiring or
rejection system.** The score measures text similarity only. It is
not the probability of getting a job, and not a judgement of a
candidate's quality.

## How It Works

1. **Resume upload** — the user uploads a resume PDF. Text is
   extracted with PyMuPDF, in memory only. The file is never written
   to disk and never committed to the repository.
2. **Job description input** — the user pastes the JD as text. It is
   cleaned and validated (empty or under 50 characters is rejected).
3. **Preprocessing** — lowercasing, URL/email removal, tokenization
   with regex, and stopword removal using sklearn's built-in English
   stop words. Special care is taken so that `C++`, `C#` and
   `Node.js` survive as single tokens. No lemmatization: TF-IDF works
   fine for this prototype without it, and NLTK/spaCy would be a heavy
   download for no real gain here.
4. **TF-IDF vectorization** — resume and JD become numeric vectors.
   Words that appear in both documents get a low weight; rare,
   meaningful words (like `tensorflow`) get a high weight.
5. **Cosine similarity** — the angle between the two vectors gives a
   match score from 0 to 1: below 0.3 is Low, 0.3–0.6 is Medium,
   above 0.6 is High.
6. **Skill extraction** — a skill dictionary (`data/skills.json`,
   26 skills, editable without touching code) is matched against both
   texts with word-boundary regex, so `Java` never matches inside
   `JavaScript`. The result shows matched skills and missing skills
   (asked in the JD, absent from the resume).
7. **Results display** — score, matched skills, missing skills, and a
   tip line, in one clean summary. The display never recomputes the
   score; it only shows what Phases 6 and 7 computed.

## Example Result

A sample resume (Python, SQL, Pandas, NumPy, Machine Learning, Git,
Docker) checked against a sample JD (Python, SQL, Machine Learning,
Docker, FastAPI, TensorFlow):

```
Resume–JD Match Result
Match Score: 48.6% (Medium)
Matched Skills: Python, SQL, Machine Learning, Pandas, TensorFlow, Docker, Git
Missing Skills: FastAPI
Tip: In missing skills ko seekhne se match badhega.
```

Boundary cases, verified by tests: a resume identical to the JD
scores 1.0 (High); a resume with no shared words scores 0.0 (Low).

## Technologies

Python 3.12, PyMuPDF, Scikit-learn, Pandas, NumPy, Streamlit.
Nothing else, nothing paid. NLTK and spaCy were deliberately not
installed.

## Project Structure

```
resume-jd-matcher/
├── README.md, requirements.txt, .gitignore, DEPLOYMENT.md
├── .venv/                     # virtual environment (not committed)
├── data/
│   └── skills.json            # editable skill dictionary (26 skills)
├── src/
│   ├── pdf_extract.py         # Phase 2: PDF text extraction
│   ├── jd_input.py            # Phase 3: JD cleaning + validation
│   ├── preprocessing.py       # Phase 4: clean / tokenize / stopwords
│   ├── vectorizer.py          # Phase 5: TF-IDF
│   ├── similarity.py          # Phase 6: cosine similarity
│   ├── skill_extraction.py    # Phase 7: matched / missing skills
│   └── results.py             # Phase 8: results display
├── app/
│   └── app.py                 # Phase 9: Streamlit app
└── tests/                     # Phase 10: 8 test files, 71 cases
```

## Installation

```bash
# create a virtual environment (once)
python3 -m venv .venv

# activate it
source .venv/bin/activate        # Linux / Mac
# .venv\Scripts\activate        # Windows

# install the libraries
pip install -r requirements.txt
```

## How to Run

```bash
# run all tests (project root)
.venv/bin/python tests/test_match_pipeline.py
.venv/bin/python tests/test_results.py
.venv/bin/python tests/test_skill_extraction.py
.venv/bin/python tests/test_similarity.py
.venv/bin/python tests/test_vectorizer.py
.venv/bin/python tests/test_preprocessing.py
.venv/bin/python tests/test_pdf_extract.py
.venv/bin/python tests/test_jd_input.py

# run the Streamlit app
.venv/bin/streamlit run app/app.py
```

In the app: upload a resume PDF, paste the job description, click
**Check Match**. The result shows the score (percent + level),
matched skills, missing skills, and a tip. Errors are shown as
friendly messages, not tracebacks: no file uploaded, empty JD,
corrupt PDF, or a scanned PDF with no extractable text.

## Testing

71 test cases pass across 8 test files (plain asserts, no pytest
needed):

| Test file | Cases | What it covers |
|---|---|---|
| test_pdf_extract.py | 5 | valid PDF (bytes/path), blank PDF, corrupt/empty input |
| test_jd_input.py | 8 | valid JD, empty/whitespace/short JD, long JD (~5000 chars), non-string |
| test_preprocessing.py | 15 | lowercasing, URL/email removal, C++/C#/Node.js kept, stopwords, skill words kept |
| test_vectorizer.py | 6 | matrix shape, "c++" as one term, IDF behaviour, empty document |
| test_similarity.py | 10 | identical → 1.0, different → 0.0, empty inputs → 0.0, level bands |
| test_skill_extraction.py | 9 | case-insensitive match, Java vs JavaScript boundary, multi-word skills, missing/matched |
| test_results.py | 7 | score preserved exactly, counts, summary line, empty skill lists |
| test_match_pipeline.py | 11 | full end-to-end via run_match: valid pipeline, consistency, error cases |

## Limitations

1. **Scanned/image PDFs are not supported** — if a resume has no
   extractable text, the app says so and suggests using a text-based
   PDF. OCR (Tesseract) is a possible future addition.
2. **The score is text similarity, not a hiring signal.** A high
   score means the words overlap; it says nothing about experience,
   quality, or whether the person will get the job.
3. **Bag of words, no meaning.** TF-IDF does not understand synonyms
   or context — "ML" and "Machine Learning" are different terms unless
   both are in the skill dictionary.
4. **Fixed skill dictionary.** Only the 26 skills in
   `data/skills.json` are recognised; add more there if needed.
5. **English only.** Preprocessing and stopwords assume English text.

## Privacy

Uploaded resumes are processed in memory and never saved to disk, so
nothing a user uploads can end up in the repository. `*.pdf` is
blocked in `.gitignore` for the same reason.

## Deployment

Streamlit Community Cloud (free) — full steps in `DEPLOYMENT.md`.
Deployment link: https://resume-j-yurhnfhj5vgigsbg8pszue.streamlit.app/
