"""
Password Strength Checker
AVIP 2026 — CyberSecurity Task 2

Rule set (documented, configurable via CONFIG below):
  1. Minimum length            (default 8, "strong" bonus at 12+)
  2. Contains lowercase letter
  3. Contains uppercase letter
  4. Contains digit
  5. Contains special character (from SPECIAL_CHARS)
  6. Not in a common/weak password blocklist
  7. No 3+ repeated consecutive characters (e.g. "aaa", "111")

Scoring:
  Each satisfied rule (2-5) = 1 point. Length bonus adds up to 2 points.
  Blocklist hit or repeated-char violation caps score at "Weak".

  Score 0-2  -> Weak
  Score 3-4  -> Moderate
  Score 5-6  -> Strong
"""

import re
import argparse

CONFIG = {
    "min_length": 8,
    "strong_length": 12,
}

SPECIAL_CHARS = r"""!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?~`"""

COMMON_PASSWORDS = {
    "password", "123456", "12345678", "qwerty", "abc123", "password1",
    "111111", "123123", "letmein", "iloveyou", "admin", "welcome",
    "monkey", "dragon", "football", "123456789", "changeme",
}


def has_repeated_chars(password: str, run_length: int = 3) -> bool:
    """Detect `run_length` or more identical characters in a row."""
    pattern = r"(.)\1{" + str(run_length - 1) + ",}"
    return bool(re.search(pattern, password))


def check_password_strength(password: str) -> dict:
    reasons = []
    score = 0

    length_ok = len(password) >= CONFIG["min_length"]
    if length_ok:
        score += 1
        reasons.append(f"✓ Meets minimum length of {CONFIG['min_length']}")
    else:
        reasons.append(f"✗ Too short (minimum {CONFIG['min_length']} characters)")

    if len(password) >= CONFIG["strong_length"]:
        score += 1
        reasons.append(f"✓ Bonus: length is {CONFIG['strong_length']}+ characters")

    has_lower = bool(re.search(r"[a-z]", password))
    has_upper = bool(re.search(r"[A-Z]", password))
    has_digit = bool(re.search(r"\d", password))
    has_special = bool(re.search(f"[{SPECIAL_CHARS}]", password))

    for ok, label in [
        (has_lower, "lowercase letter"),
        (has_upper, "uppercase letter"),
        (has_digit, "digit"),
        (has_special, "special character"),
    ]:
        if ok:
            score += 1
            reasons.append(f"✓ Contains a {label}")
        else:
            reasons.append(f"✗ Missing a {label}")

    is_common = password.lower() in COMMON_PASSWORDS
    if is_common:
        reasons.append("✗ Password found in common/weak password list")

    repeated = has_repeated_chars(password)
    if repeated:
        reasons.append("✗ Contains 3+ repeated consecutive characters")

    # Determine category
    if is_common or repeated or score <= 2:
        category = "Weak"
    elif score <= 4:
        category = "Moderate"
    else:
        category = "Strong"

    return {
        "password_length": len(password),
        "score": score,
        "max_score": 6,
        "category": category,
        "reasons": reasons,
    }


def print_report(password: str):
    result = check_password_strength(password)
    print(f"\nPassword: {'*' * len(password)}  (length={result['password_length']})")
    print(f"Score: {result['score']}/{result['max_score']}")
    print(f"Category: {result['category']}")
    print("Rationale:")
    for r in result["reasons"]:
        print(f"  {r}")
    return result


def main():
    parser = argparse.ArgumentParser(description="Password Strength Checker")
    parser.add_argument("password", nargs="?", help="Password to evaluate")
    args = parser.parse_args()

    if args.password:
        print_report(args.password)
    else:
        pwd = input("Enter password to check: ")
        print_report(pwd)


if __name__ == "__main__":
    main()
