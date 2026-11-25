"""Phase 4: NLP preprocessing — resume aur JD ka text saaf karna.

TF-IDF (Phase 5) ko saaf, chhote, meaningful words chahiye. Isliye har
text is chain se guzarta hai: clean -> tokenize -> stopwords hatao.

Lemmatization is phase me NAHI hai: is prototype ke liye TF-IDF bina
lemmatization ke theek kaam karta hai, aur NLTK/spaCy daalna ek bhaari
download hota. Agar baad me asli zaroorat padi to tab add karenge.
"""

import re

from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

# URL aur email hatane ke patterns
_URL_RE = re.compile(r"https?://\S+|www\.\S+")
_EMAIL_RE = re.compile(r"\S+@\S+")

# Token: akshar/number, saath me + ya # (C++, C#), aur beech me dot (Node.js)
_TOKEN_RE = re.compile(r"[a-z0-9+#]+(?:\.[a-z0-9+#]+)*")


def clean_text(text):
    """Text saaf karo: lowercase, URL/email hatao, punctuation hatao.

    Bachake rakho: `+` aur `#` (C++, C# skill names me hote hain) aur
    dot jab wo do aksharon ke beech me ho (Node.js). Baaki punctuation
    ko space se badlo, extra whitespace ek single space me milao.
    """
    if not isinstance(text, str):
        raise ValueError("Text ek string hona chahiye.")
    text = text.lower()
    text = _URL_RE.sub(" ", text)
    text = _EMAIL_RE.sub(" ", text)
    # Dot sirf tab rakho jab uske dono taraf akshar/number ho (node.js);
    # warna wo sentence ka full-stop hai, hata do.
    text = re.sub(r"(?<!\w)\.|\.(?!\w)", " ", text)
    text = re.sub(r"[^a-z0-9+#.\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokenize(text):
    """Saaf kiye hue text ko word tokens me todo (plain `re`, NLTK nahi).

    Token me kam se kam ek akshar ya number hona chahiye — akele `+`
    ya `#` jaisi bachi hui cheezein token nahi banti.
    """
    if not isinstance(text, str):
        raise ValueError("Text ek string hona chahiye.")
    tokens = _TOKEN_RE.findall(text.lower())
    return [t for t in tokens if re.search(r"[a-z0-9]", t)]


def remove_stopwords(tokens):
    """English stopwords hatao (sklearn ki built-in list, NLTK nahi).

    Rule: skill jaisi cheezein kabhi stopword nahi hoti — sklearn ki
    list me 'python', 'tensorflow', 'pandas', 'c++' jaise words hain hi
    nahi. Phase 7 ka skill dictionary iska aakhiri guard hoga: skill
    extraction dictionary se hota hai, stopword list se nahi.
    """
    return [t for t in tokens if t not in ENGLISH_STOP_WORDS]


def preprocess_text(text):
    """Main function: clean -> tokenize -> stopwords hatao -> ek string.

    Khaali ya sirf whitespace wala input "" return karta hai.
    """
    cleaned = clean_text(text)
    if not cleaned:
        return ""
    tokens = tokenize(cleaned)
    tokens = remove_stopwords(tokens)
    return " ".join(tokens)
