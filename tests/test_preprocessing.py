"""Phase 4 tests — preprocessing ke har rule ka ek case.

Run: cd ~/workspace/resume-jd-matcher && .venv/bin/python tests/test_preprocessing.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.preprocessing import (
    clean_text,
    preprocess_text,
    remove_stopwords,
    tokenize,
)

passed = 0
failed = 0


def check(name, actual, expected):
    global passed, failed
    if actual == expected:
        passed += 1
        print(f"Case {name}: PASS")
    else:
        failed += 1
        print(f"Case {name}: FAIL — mila {actual!r}, chahiye tha {expected!r}")


def check_raises(name, fn):
    global passed, failed
    try:
        fn()
    except ValueError:
        passed += 1
        print(f"Case {name}: PASS")
    else:
        failed += 1
        print(f"Case {name}: FAIL — ValueError nahi aaya")


# 1. Lowercasing
check("1 (lowercasing)", preprocess_text("Python Developer"),
      "python developer")

# 2. URL hat jaye
result = preprocess_text("Visit https://example.com/careers for Python jobs")
check("2 (URL removed)", result, "visit python jobs")
assert "example" not in result and "http" not in result

# 3. Email hat jaye
result = preprocess_text("Contact me at john.doe@gmail.com for Python work")
check("3 (email removed)", result, "contact python work")
assert "gmail" not in result

# 4. C++ bache
check("4 (C++ kept)", "c++" in preprocess_text("I know C++ and Python").split(), True)

# 5. C# bache
check("5 (C# kept)", "c#" in preprocess_text("Experience in C# and .NET").split(), True)

# 6. Stopwords hatein
check("6 (stopwords removed)", preprocess_text("the and with Python"), "python")

# 7. Skill words bachein
check("7 (skill words kept)", preprocess_text("Python TensorFlow pandas"),
      "python tensorflow pandas")

# 8. Bikhri whitespace ek ho jaye
check("8 (whitespace collapsed)", preprocess_text("  Python\n\n\t  SQL   "),
      "python sql")

# 9. Khaali input -> khaali output
check("9 (empty string)", preprocess_text(""), "")
check("9b (whitespace only)", preprocess_text("   \n\t  "), "")

# 10. Non-string input -> ValueError
check_raises("10 (clean_text non-string)", lambda: clean_text(123))
check_raises("10b (preprocess non-string)", lambda: preprocess_text(None))

# 11. tokenize: stopwords rehte hain (hatana alag step hai), C++ token banta hai
check("11 (tokenize)", tokenize("Python and C++"), ["python", "and", "c++"])

# 12. remove_stopwords: sirf stopwords hatein, skills bachte hain
check("12 (remove_stopwords)",
      remove_stopwords(["the", "python", "and", "sql"]), ["python", "sql"])

# 13. Node.js me dot bachta hai
check("13 (Node.js kept)", "node.js" in preprocess_text("Worked on Node.js apps").split(), True)

print(f"\n{passed}/{passed + failed} cases PASS")
if failed:
    raise SystemExit(1)
