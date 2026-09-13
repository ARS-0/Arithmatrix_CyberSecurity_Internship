# Task 2 — Password Strength Checker

AVIP 2026 — CyberSecurity Track — Task 2

## Overview
A CLI tool that scores password strength against a documented rule set and
returns a category (Weak / Moderate / Strong) with a rationale for each rule.

## Rule Set (configurable in `password_checker.py`)
| Rule | Points |
|---|---|
| Length ≥ 8 chars | +1 |
| Length ≥ 12 chars (bonus) | +1 |
| Contains lowercase letter | +1 |
| Contains uppercase letter | +1 |
| Contains digit | +1 |
| Contains special character | +1 |
| Found in common-password blocklist | caps score at **Weak** |
| 3+ repeated consecutive characters | caps score at **Weak** |

**Category thresholds:** 0–2 → Weak, 3–4 → Moderate, 5–6 → Strong
Thresholds and the minimum/strong length values live in the `CONFIG` dict at
the top of `password_checker.py` and can be tuned per your own policy.

## Usage
```bash
python password_checker.py "MyS3cur3P@ssw0rd!"
# or run without an argument to be prompted interactively
python password_checker.py
```

## Test Cases
Run the included test suite:
```bash
python test_cases.py
```
See `test_run_output.txt` for a captured run (8/8 passing), covering:
- Common/dictionary passwords (`password`, `123456`) → Weak
- Repeated-character passwords (`aaaaaaaa`) → Weak
- Mixed-case + digit passwords → Moderate
- Long passphrases and high-entropy strings → Strong

## Files
- `password_checker.py` — main implementation + rule engine
- `test_cases.py` — automated test cases
- `test_run_output.txt` — sample test run output

## Notes
This tool checks composition/pattern rules only — it does not check passwords
against live breach databases. For production systems, pair this kind of
checker with a real breach-corpus check (e.g. Have I Been Pwned's k-anonymity
API) before relying on it fully.
