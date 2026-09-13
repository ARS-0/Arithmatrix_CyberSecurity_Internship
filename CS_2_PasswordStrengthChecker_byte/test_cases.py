"""
Test cases for password_checker.py
Run with: python test_cases.py
"""

from password_checker import check_password_strength

TEST_CASES = [
    ("password", "Weak"),          # common password
    ("123456", "Weak"),            # common + too short
    ("aaaaaaaa", "Weak"),          # repeated chars
    ("Passw0rd", "Moderate"),      # decent mix, short-ish
    ("Tr0ub4dor", "Moderate"),
    ("C0rrect-Horse-Battery", "Strong"),
    ("MyS3cur3P@ssw0rd!", "Strong"),
    ("Xk9#mL2$vQ7pR", "Strong"),
]


def run_tests():
    passed = 0
    for pwd, expected in TEST_CASES:
        result = check_password_strength(pwd)
        status = "PASS" if result["category"] == expected else "FAIL"
        if status == "PASS":
            passed += 1
        print(f"[{status}] '{pwd}' -> got={result['category']} expected={expected} "
              f"(score={result['score']}/{result['max_score']})")

    print(f"\n{passed}/{len(TEST_CASES)} test cases passed.")


if __name__ == "__main__":
    run_tests()
