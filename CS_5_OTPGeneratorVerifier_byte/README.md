# Task 5 — OTP Generator & Verifier

AVIP 2026 — CyberSecurity Track — Task 5

## Overview
A from-scratch implementation of **TOTP** (Time-based One-Time Password,
RFC 6238), built on top of **HOTP** (RFC 4226), using only Python's standard
library (`hmac`, `hashlib`, `struct`, `base64`).

## Algorithm / Validity Parameters
| Parameter | Value |
|---|---|
| Hash algorithm | HMAC-SHA1 |
| Time step (T) | 30 seconds |
| OTP length | 6 digits |
| Validity window | current step ± 1 step (~±30s clock drift tolerance) |

These are documented and configurable at the top of `otp_tool.py`
(`TIME_STEP`, `OTP_DIGITS`, `VALIDITY_WINDOW`).

## Usage
```bash
# Generate a brand-new secret and its current OTP
python otp_tool.py generate

# Generate an OTP for an existing secret
python otp_tool.py generate --secret IULZUO3QUL3OSVNWKL6K6ONMDYOFOBES

# Verify a submitted OTP against a secret
python otp_tool.py verify IULZUO3QUL3OSVNWKL6K6ONMDYOFOBES 384393
```

## Correctness — Validated Against the Official RFC 4226 Test Vectors
`test_vectors.py` checks the HOTP core against all 10 published RFC 4226
Appendix D test vectors (secret = ASCII "12345678901234567890"), plus a
generate→verify round trip demonstrating both correct-OTP acceptance and
incorrect-OTP rejection.

```
10/10 HOTP vectors passed.
Generated OTP: 223749
[PASS] Correct OTP accepted: True
[PASS] Incorrect OTP rejected: True
```
Full output in `test_run_output.txt`.

## Files
- `otp_tool.py` — TOTP/HOTP implementation, generate + verify CLI
- `test_vectors.py` — RFC 4226 conformance tests + correct/incorrect demo
- `test_run_output.txt` — captured test run
- `demo_generate.txt` — sample `generate` command output

## Notes
This is an educational, dependency-free TOTP implementation compatible with
the same algorithm used by Google Authenticator / Authy. For production
systems, prefer a maintained, audited library such as `pyotp`.
