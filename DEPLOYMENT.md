# Deployment — Streamlit Community Cloud (free)

Ye project Streamlit Community Cloud ke free plan pe deploy hota hai.
Deploy se pehle saara code GitHub repo me hona chahiye.

## Kya-kya chahiye

- GitHub account: **vijaymehta1**
- Repo ka naam: `resume-jd-matcher` (public)
- Repo me ye files honi chahiye (sab pehle se tracked hain):
  - `app/app.py` — main app file
  - `requirements.txt` — pinned versions
  - `data/skills.json` — skill dictionary; app ise runtime pe padhta
    hai, isliye ye file repo me tracked honi hi chahiye
  - `src/` ke saare modules — `pdf_extract.py`, `jd_input.py`,
    `preprocessing.py`, `vectorizer.py`, `similarity.py`,
    `skill_extraction.py`, `results.py`

## Steps

### 1. GitHub pe repo banao

github.com par jao → New repository → naam `resume-jd-matcher`
→ Public → Create. Koi README/license wahan se add mat karo
(khaali repo chahiye, warna push me conflict hoga).

### 2. Code push karo (project folder se)

```bash
cd ~/workspace/resume-jd-matcher
git remote add origin https://github.com/vijaymehta1/resume-jd-matcher.git
git branch -M main
git push -u origin main
```

GitHub username/password poochhega — apne account se login karo.
(Pehli baar Personal Access Token maang sakta hai; password ki jagah
token daalna hota hai. Token: GitHub → Settings → Developer settings
→ Personal access tokens → Generate.)

### 3. Streamlit Cloud pe deploy karo

1. https://share.streamlit.io kholo → GitHub se sign in karo.
2. **New app** → **Use existing repo** chuno.
3. Repository: `vijaymehta1/resume-jd-matcher`, Branch: `main`,
   Main file path: `app/app.py`.
4. **Deploy** dabao. Pehli baar 2-3 minute lagte hain (libraries
   install hoti hain).
5. Deploy hone ke baad ek public URL milega, jaise
   `https://resume-jd-matcher.streamlit.app`.

### 4. Deploy ke baad test karo

- App kholo, ek sample resume PDF upload karo aur ek job description
  paste karo, phir **Check Match** dabao.
- Ek valid match pe score (percent me) + matched skills + missing
  skills dikhne chahiye. Local check me ek sample resume + JD pe
  score **48.6% (Medium)** aaya tha, 7 matched skills aur 1 missing
  skill (FastAPI) — deployed app pe bhi aisa hi behaviour hona chahiye.
- Galat input pe (bina file ke, khaali JD, corrupt PDF) saaf error
  message dikhna chahiye, traceback nahi.
- Agar koi error aaye to Streamlit Cloud ke **Manage app → Logs**
  me dekho.

## Notes

- App ko chalane ke liye `data/skills.json` zaroori hai — isliye ye
  file repo me tracked hai, `.gitignore` me nahi.
- Uploaded resume kabhi disk pe save nahi hota — sirf memory me
  process hota hai, isliye privacy ka koi issue nahi.
- Free plan pe app sone (sleep) ho sakta hai jab koi use na kare —
  dobara kholne pe 30-60 second me jaag jata hai.
