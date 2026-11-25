# Internship Report — Resume–Job Description Matching System

> Ye file report ka content hai (Markdown me), asli implementation
> aur asli test results ke basis pe likha gaya hai. Apne college ke
> format me convert karte time headings aur personal details bhar
> lena. Personal details (naam, roll no.) placeholders me hain —
> apne hisaab se bhar do.

---

## 1. Title Page (bharne ke liye)

- **Project Title:** Resume–Job Description Matching System
- **Name:** [Your Name]
- **Roll No.:** [Your Roll No.]
- **Course:** B.Tech, Computer Science and Engineering
- **Institute:** [Your Institute Name]
- **Internship Domain:** Artificial Intelligence & Machine Learning
  (Natural Language Processing)

---

## 2. Abstract

This project builds a Natural Language Processing system that compares
a resume (PDF) with a job description (text) and reports how well the
two match. It uses TF-IDF vectorization and cosine similarity to
produce a match score from 0 to 1, and a skill dictionary to report
which skills match and which skills the job asks for but the resume
does not have. The system is an educational prototype, not an
automated hiring or rejection system: the score measures text
similarity only, not the probability of getting a job or a
candidate's quality. The complete pipeline — PDF text extraction,
job-description validation, preprocessing, TF-IDF, cosine similarity,
skill extraction and results display — was built as small, testable
Python modules and wrapped in a Streamlit web application. All 71
test cases across 8 test files pass, including end-to-end tests of
the full pipeline. Boundary behaviour is verified: a resume identical
to the job description scores 1.0 (High), and a resume with no shared
words scores 0.0 (Low).

## 3. Introduction

When a person applies for a job, the first question is simple: does
my resume match what the job description asks for? Reading a long job
description and comparing it line by line with a resume is slow, and
it is easy to miss a skill the employer asked for. This project
automates that comparison with basic NLP: it turns both documents
into numbers, measures how close they are, and lists the skills that
match and the skills that are missing — so the user knows exactly
what to learn next. The whole system is built with free, open-source
tools and runs on a normal laptop.

## 4. Problem Statement

Given a resume in PDF format and a job description as text, compute
(1) a match score between 0 and 1, (2) the list of skills present in
both documents, and (3) the list of skills the job description asks
for but the resume does not have — and present all three through a
simple web interface that a non-technical user can operate.

## 5. Objectives

1. Extract text from a resume PDF reliably, and handle corrupt,
   empty and scanned PDFs with clear errors.
2. Clean and validate the job description input.
3. Preprocess both texts (lowercasing, cleaning, tokenization,
   stopword removal) while keeping technical terms like `C++`,
   `C#` and `Node.js` intact.
4. Convert both texts to TF-IDF vectors and compare them with cosine
   similarity to get a match score.
5. Extract skills from both texts using an editable skill dictionary
   and report matched and missing skills.
6. Display the score and the skill lists in one clean summary.
7. Build a Streamlit application around the pipeline.
8. Test every module and the full end-to-end pipeline, and prepare
   the project for free deployment.

## 6. System Overview / How It Works

The pipeline has 7 steps. Each step exists for one reason:

1. **PDF text extraction** — a resume arrives as a PDF, not as plain
   text, so the text must first be pulled out (PyMuPDF). Scanned
   image PDFs have no text to extract, so they are reported honestly
   instead of silently returning nothing.
2. **JD cleaning and validation** — a job description pasted by a user
   can be empty, too short, or full of extra whitespace. Cleaning and
   validation keep garbage input from producing a meaningless score.
3. **Preprocessing** — raw text contains URLs, emails, capital
   letters and filler words that add noise to the comparison. Cleaning
   and stopword removal leave the meaningful words behind. Technical
   terms (`C++`, `C#`, `Node.js`) are protected so they are not
   broken into pieces.
4. **TF-IDF vectorization** — to compare two texts mathematically,
   both must become vectors of numbers. TF-IDF gives a high weight
   to rare, meaningful words (like `tensorflow`) and a low weight to
   words that appear everywhere (like `developer`).
5. **Cosine similarity** — the angle between the two vectors is the
   match score: 1.0 means the texts point in the same direction
   (identical), 0.0 means they share no words at all.
6. **Skill extraction** — the score alone says *how much* the texts
   match; skills say *which* skills match and which are missing.
   That is the useful part for the user, because it tells them what
   to learn next.
7. **Results display** — score, matched skills, missing skills and a
   tip line in one summary. Display only shows what the earlier
   steps computed; it never changes the score.

Workflow: Resume PDF → Text Extraction → Preprocessing → TF-IDF →
Cosine Similarity → Skill Extraction → Results Display → Streamlit App.
The job description joins the same pipeline at the preprocessing
step.

**Tools:** Python 3.12, PyMuPDF, Scikit-learn, Pandas, NumPy,
Streamlit. NLTK and spaCy were deliberately not installed: sklearn's
built-in English stop words plus regex tokenization were enough for
this prototype, and adding heavy libraries without a real need would
only slow down setup.

## 7. Dataset

This project has **no fixed dataset**. The input is whatever the user
supplies at run time: their own resume PDF and a job description
text. That is stated honestly here because there is no training data
to describe — the system does not learn from a dataset, it compares
the two documents the user gives it. The only fixed data in the
project is the skill dictionary, `data/skills.json`: 26 skills
(Python, SQL, Machine Learning, Deep Learning, Pandas, NumPy,
Scikit-learn, TensorFlow, PyTorch, NLP, Docker, Git, FastAPI, Data
Analysis, Statistics, C++, C#, Java, JavaScript, HTML, CSS, React,
Node.js, Flask, MongoDB, AWS). The user can add or remove skills in
that file without changing any code.

## 8. Methodology

Each phase was built as a small, independent module with its own
tests, and the modules were connected one by one so that a failure in
any step is easy to trace:

- Text is processed in memory only. An uploaded resume is never
  written to disk, and `*.pdf` is blocked in `.gitignore`, so no
  user's resume can ever end up in the repository.
- The same preprocessing is used everywhere (the TF-IDF vectorizer
  calls the Phase 4 functions), so the resume and the job
  description are always compared on equal terms.
- Skill matching uses word-boundary regex (lookaround), not a plain
  substring check, so `Java` never matches inside `JavaScript`, and
  `C++` still matches correctly (a plain word boundary does not work
  on `+`, which is not a word character).
- The score is computed once (Phase 6) and only displayed afterwards
  (Phase 8) — it is never recomputed or adjusted.

## 9. Implementation

**Phase 2 — PDF extraction (`src/pdf_extract.py`).**
`extract_text_from_pdf` accepts a file path or raw bytes and returns
the text of all pages joined together. Corrupt, empty or encrypted
PDFs raise a `ValueError`; a blank or scanned PDF returns an empty
string, and `has_extractable_text` reports that there is nothing to
work with. Uploads are never written to disk.

**Phase 3 — JD input (`src/jd_input.py`).**
`clean_job_description` strips extra whitespace; `validate_job_
description` rejects empty input and job descriptions shorter than
50 characters after cleaning, and accepts long descriptions (a
~5000-character JD was tested) without truncation.

**Phase 4 — Preprocessing (`src/preprocessing.py`).**
`clean_text` lowercases, removes URLs and emails, and keeps `+`,
`#` and dots between letters so `C++`, `C#` and `Node.js` survive.
`tokenize` splits text with regex (no NLTK download). `remove_
stopwords` uses sklearn's `ENGLISH_STOP_WORDS` (318 words); skill
words are never stopwords. `preprocess_text` chains the three steps.
Lemmatization was deliberately not implemented: TF-IDF works fine
without it for this prototype, and adding NLTK/spaCy would be a
heavy download for no real gain.

**Phase 5 — TF-IDF (`src/vectorizer.py`).**
`build_tfidf_vectorizer` creates a sklearn `TfidfVectorizer` that
uses Phase 4's `preprocess_text` as preprocessor and `tokenize` as
tokenizer, so tokenization is identical in both places and `c++`
stays one term. `lowercase=False` (preprocessing already lowercases),
L2 norm, `use_idf=True`, `smooth_idf=True`. `fit_vectorizer` fits
on a list of texts (typically [resume, JD]) and returns the fitted
vectorizer and the TF-IDF matrix.

**Phase 6 — Cosine similarity (`src/similarity.py`).**
`cosine_similarity_score` compares two TF-IDF vectors with sklearn's
`cosine_similarity`, clipped to [0, 1] against floating-point error.
`match_score` returns `{"score", "score_percent", "level"}` with
levels Low (< 0.3), Medium (0.3–0.6) and High (> 0.6). Empty resume
or empty JD gives a score of 0.0. The module documents clearly that
the score is text similarity only — not job probability or candidate
quality.

**Phase 7 — Skill extraction (`src/skill_extraction.py`,
`data/skills.json`).**
`load_skills` reads the 26-skill JSON list. `extract_skills` finds
which skills appear in a text (case-insensitive, word-boundary
matching, multi-word skills like "Machine Learning" matched as one
skill). `find_missing_skills` returns skills the JD asks for but the
resume lacks; `find_matched_skills` returns the overlap.

**Phase 8 — Results display (`src/results.py`).**
`format_results` joins the Phase 6 score with the Phase 7 skill
lists into one dictionary with counts and a one-line summary (for
example, "Match 42.0% (Medium) — 3 skills matched, 2 missing.").
`display_results` returns a clean multi-line text block with the
score, matched skills, missing skills and a tip line. Nothing is
recomputed here.

**Phase 9 — Streamlit app (`app/app.py`).**
The user uploads a resume PDF, pastes the job description and clicks
"Check Match". All logic lives in `run_match(resume_bytes, jd_text)`,
which returns the Phase 8 result dictionary, so the pipeline is
testable without Streamlit. Errors are shown with `st.error` (no
file, empty JD, corrupt PDF, scanned PDF) — no tracebacks are shown
to the user. Run with `.venv/bin/streamlit run app/app.py`.

## 10. Evaluation

There is no accuracy percentage to report, because this system does
not predict a label — it measures similarity. Evaluation here means:
does every part behave as specified, and do the boundary cases give
the right answers? All tests are plain asserts, run with the project
virtual environment. **71 test cases pass across 8 test files.**

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

Boundary scores, verified by tests:

| Case | Score | Level |
|---|---|---|
| Resume identical to the JD | 1.0 | High |
| Resume with no shared words | 0.0 | Low |
| Sample end-to-end (resume: Python, SQL, Pandas, NumPy, ML, Git, Docker; JD: Python, SQL, ML, Docker, FastAPI, TensorFlow) | 0.486 (48.6%) | Medium |

Two more verified end-to-end runs: 54.2% (Medium), 4 skills matched,
2 missing (TensorFlow, FastAPI); and 40.3% (Medium), matched
Python/SQL, missing Docker/FastAPI. The app was also smoke-tested
live: `streamlit run` returns HTTP 200 with no errors.

## 11. Results and Analysis

- The pipeline works end to end: a real PDF and a real JD go in,
  and a score plus matched/missing skills come out, with every step
  covered by tests.
- The boundary cases behave as the maths says they should: identical
  texts score 1.0, texts with no shared words score 0.0, and partial
  overlap lands in between (0.486 in the sample run).
- The most useful output is not the score but the skill lists. A
  score of 48.6% alone says little; "7 skills matched, 1 missing
  (FastAPI)" tells the user exactly what to learn next.
- The score is honest about what it is: TF-IDF cosine similarity.
  It rewards shared words and punishes extra, unrelated words, which
  is why a resume with many extra skills can score lower than
  expected even when the important skills match — the sample run
  (0.486) shows this. The level bands (Low/Medium/High) make the
  number readable, but they are rough guides, not grades.

## 12. Screenshots

Live app: https://resume-j-yurhnfhj5vgigsbg8pszue.streamlit.app/ (deployed
25 Nov 2026 on Streamlit Community Cloud).

Add here after deployment: (1) Streamlit app home page, (2) a resume
PDF uploaded with a JD pasted, (3) the result showing the match
score, matched skills and missing skills. Take them from the live
deployed app, not from local mockups.

## 13. Limitations

1. **Scanned/image PDFs are not supported.** If a resume has no
   extractable text, the app says so and suggests a text-based PDF.
   OCR (Tesseract) is a possible future addition.
2. **The score is text similarity, not a hiring signal.** A high
   score means the words overlap; it says nothing about experience,
   quality, or whether the person will get the job. This system must
   never be used to reject candidates automatically.
3. **Bag of words, no meaning.** TF-IDF does not understand synonyms
   or context — "ML" and "Machine Learning" are different terms
   unless both are in the skill dictionary.
4. **Fixed skill dictionary.** Only the 26 skills in
   `data/skills.json` are recognised; add more there if needed.
5. **English only.** Preprocessing and stopwords assume English text.

## 14. Conclusion

The project successfully built an end-to-end resume–job description
matching system: a resume PDF and a job description go in, and a
match score plus matched and missing skills come out, through a
working Streamlit application. Every module is small, tested, and
honest about its limits — 71 test cases pass, boundary behaviour is
verified, and the score is clearly labelled as text similarity, not
a hiring decision. The system is understandable, testable, and
reproducible on a normal laptop with free tools.

## 15. Future Scope

1. OCR with Tesseract, so scanned/image resumes work too.
2. Semantic embeddings (e.g. sentence transformers) so synonyms and
   related skills count as matches, instead of exact words only.
3. A larger skill dictionary with automatic detection of skills not
   yet in the list.
4. Support for more resume formats (DOCX, plain text).
5. Deployment is done — the app is live at
   https://resume-j-yurhnfhj5vgigsbg8pszue.streamlit.app/ on
   Streamlit Community Cloud (screenshots to be added to this
   report from the live app).
