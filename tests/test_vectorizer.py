"""Phase 5 tests — TF-IDF vectorization ke har rule ka ek case.

Run: cd ~/workspace/resume-jd-matcher && .venv/bin/python tests/test_vectorizer.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.vectorizer import (
    build_tfidf_vectorizer,
    fit_vectorizer,
    get_vocabulary,
)

passed = 0
failed = 0


def check(name, condition):
    global passed, failed
    if condition:
        passed += 1
        print(f"PASS: {name}")
    else:
        failed += 1
        print(f"FAIL: {name}")


RESUME = "Python developer with experience in C++ and SQL. Machine learning with pandas and TensorFlow."
JD = "We need a Python developer skilled in machine learning, SQL and Docker."

# Case 1: do texts fit karo — matrix shape (2, n), n > 0
vectorizer, matrix = fit_vectorizer([RESUME, JD])
check("Case 1 (fit: matrix shape (2, n), n > 0)",
      matrix.shape[0] == 2 and matrix.shape[1] > 0)

# Case 2: "c++" vocabulary me ek hi term hai, "c" alag term nahi
vocab = get_vocabulary(vectorizer)
check('Case 2 ("c++" ek term hai, "c" alag nahi)',
      "c++" in vocab and "c" not in vocab)

# Case 3: dono docs me aane wale word ki IDF kam, ek doc wale ki zyada
idf = dict(zip(vectorizer.get_feature_names_out(), vectorizer.idf_))
check("Case 3 (IDF: 'python' dono me < 'tensorflow' ek me)",
      idf["python"] < idf["tensorflow"])

# Case 4: khaali-string document fit ko crash nahi karta, row all-zero hoti hai
_, matrix_empty = fit_vectorizer(["", RESUME])
check("Case 4 (khaali doc: no crash, pehli row all-zero)",
      matrix_empty.shape[0] == 2 and matrix_empty[0].nnz == 0)

# Case 5: word jahan zyada baar aaya, wahan uska TF-IDF weight zyada
vec_rep, matrix_rep = fit_vectorizer(["python python python sql", "python sql"])
col = vec_rep.vocabulary_["python"]
check("Case 5 (repeat word: 'python' ka weight doc1 > doc2)",
      matrix_rep[0, col] > matrix_rep[1, col])

# Case 6: vocabulary sorted list hoti hai
check("Case 6 (get_vocabulary sorted list deta hai)",
      vocab == sorted(vocab) and isinstance(vocab, list))

print(f"\nSab {passed}/{passed + failed} cases PASS" if failed == 0
      else f"\n{failed} FAIL, {passed} PASS")
