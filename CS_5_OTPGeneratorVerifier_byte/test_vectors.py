"""
Test vectors for otp_tool.py
Includes an RFC 6238 published test vector plus correct/incorrect handling demos.
Run with: python test_vectors.py
"""

from otp_tool import generate_totp, verify_totp, _hotp
import base64

# RFC 6238 Appendix B test vector (SHA1, 8-digit truncated to 6 digits here
# since our implementation is fixed at 6 digits — we verify the HOTP core
# against RFC 4226's own 6-digit test vectors instead, which is the
# algorithm TOTP is built on).

# RFC 4226 Appendix D test vectors (secret = "12345678901234567890" in ASCII)
RFC4226_SECRET_B32 = base64.b32encode(b"12345678901234567890").decode()
RFC4226_EXPECTED = [
    "755224", "287082", "359152", "969429", "338314",
    "254676", "287922", "162583", "399871", "520489",
]


def test_hotp_rfc4226():
    print("=== RFC 4226 HOTP core test vectors ===")
    passed = 0
    for counter, expected in enumerate(RFC4226_EXPECTED):
        actual = _hotp(RFC4226_SECRET_B32, counter)
        status = "PASS" if actual == expected else "FAIL"
        if status == "PASS":
            passed += 1
        print(f"[{status}] counter={counter} expected={expected} actual={actual}")
    print(f"{passed}/{len(RFC4226_EXPECTED)} HOTP vectors passed.\n")


def test_totp_generate_and_verify():
    print("=== TOTP generate -> verify round trip ===")
    secret = base64.b32encode(b"my-demo-secret-key!!").decode()
    otp = generate_totp(secret)
    print(f"Generated OTP: {otp}")

    correct = verify_totp(secret, otp)
    print(f"[PASS] Correct OTP accepted: {correct}" if correct else "[FAIL] Correct OTP rejected")

    wrong_otp = "000000" if otp != "000000" else "111111"
    incorrect = verify_totp(secret, wrong_otp)
    print(f"[PASS] Incorrect OTP rejected: {not incorrect}" if not incorrect else "[FAIL] Incorrect OTP accepted")
    print()


if __name__ == "__main__":
    test_hotp_rfc4226()
    test_totp_generate_and_verify()
