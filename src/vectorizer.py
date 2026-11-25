"""Phase 5: TF-IDF vectorization — text ko numbers me badalna.

Plain words me:
- Bag of Words (BoW): har document ko uske words ki list samjho — kaunsa
  word kitni baar aaya, bas ye ginna.
- Vocabulary: saare documents me aane wale alag-alag words ki list.
  Ye vector ki columns banti hain.
- TF (Term Frequency): ek word ek document me kitni baar aaya.
- IDF (Inverse Document Frequency): jo word har document me aata hai
  (jaise "developer"), wo match karne me kam kaam ka hota hai; jo word
  sirf ek document me aata hai (jaise "tensorflow"), wo zyada khaas
  hota hai. IDF aam words ko halka aur rare words ko bhaari karta hai.
- TF-IDF = TF x IDF. Sirf count (BoW) use karne se "the", "and" jaise
  aam words ka score badh jata; TF-IDF unhe dabata hai aur meaningful
  words ko upar lata hai. Isliye match ke liye TF-IDF behtar hai.

Phase 4 ka preprocess_text yahan preprocessor hai, aur Phase 4 ka
tokenize hi tokenizer hai — taaki "c++", "c#" aur "node.js" ek hi
term rahein (sklearn ka default token pattern inhe tod deta).
"""

from sklearn.feature_extraction.text import TfidfVectorizer

from src.preprocessing import preprocess_text, tokenize


def build_tfidf_vectorizer():
    """TF-IDF vectorizer banao (abhi fit nahi — sirf settings).

    lowercase=False kyunki preprocess_text pehle hi lowercase kar
    deta hai. norm="l2" har document vector ki length 1 karta hai,
    taaki lambe aur chhote document barabar compare ho sakein.
    """
    return TfidfVectorizer(
        preprocessor=preprocess_text,
        tokenizer=tokenize,
        token_pattern=None,  # custom tokenizer hai, default pattern nahi chahiye
        lowercase=False,
        norm="l2",
        use_idf=True,
        smooth_idf=True,
    )


def fit_vectorizer(texts):
    """Texts ki list (jaise [resume_text, jd_text]) pe TF-IDF fit karo.

    Returns: (fitted vectorizer, TF-IDF matrix) — matrix ki har row ek
    document hai, har column ek vocabulary word hai.
    """
    if not texts:
        raise ValueError("Texts ki list khaali hai, fit karne ko kuch nahi.")
    vectorizer = build_tfidf_vectorizer()
    matrix = vectorizer.fit_transform(texts)
    return vectorizer, matrix


def get_vocabulary(vectorizer):
    """Fitted vectorizer ki vocabulary, sorted list me."""
    return sorted(vectorizer.get_feature_names_out().tolist())
