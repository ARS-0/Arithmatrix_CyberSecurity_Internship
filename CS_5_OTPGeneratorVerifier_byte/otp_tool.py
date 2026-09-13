"""
OTP Generator & Verifier (TOTP — Time-based One-Time Password)
AVIP 2026 — CyberSecurity Task 5

Implements RFC 6238 TOTP from scratch (HMAC-SHA1) so it has no external
dependency beyond Python's standard library.

Algorithm parameters (documented / configurable):
    - Secret: base32-encoded shared secret
    - Time step (T): 30 seconds
    - Digits: 6
    - Validity window: current step +/- 1 step (i.e. accepts an OTP up to
      ~30s old or ~30s "early" to tolerate clock drift) — configurable via
      VALIDITY_WINDOW below.
"""

import argparse
import base64
import hashlib
import hmac
import struct
import time
import secrets

TIME_STEP = 30          # seconds per OTP validity period
OTP_DIGITS = 6
VALIDITY_WINDOW = 1     # accept +/- N time steps to tolerate clock drift


def generate_secret() -> str:
    """Generate a random base32 secret suitable for TOTP."""
    random_bytes = secrets.token_bytes(20)
    return base64.b32encode(random_bytes).decode("utf-8")


def _hotp(secret_b32: str, counter: int, digits: int = OTP_DIGITS) -> str:
    """RFC 4226 HOTP core, used as the building block for TOTP."""
    key = base64.b32decode(secret_b32.upper() + "=" * ((8 - len(secret_b32) % 8) % 8))
    counter_bytes = struct.pack(">Q", counter)
    hmac_hash = hmac.new(key, counter_bytes, hashlib.sha1).digest()

    offset = hmac_hash[-1] & 0x0F
    truncated = hmac_hash[offset:offset + 4]
    code_int = struct.unpack(">I", truncated)[0] & 0x7FFFFFFF
    code = code_int % (10 ** digits)
    return str(code).zfill(digits)


def generate_totp(secret_b32: str, timestamp: float = None) -> str:
    """RFC 6238 TOTP: HOTP where the counter is derived from elapsed time."""
    if timestamp is None:
        timestamp = time.time()
    counter = int(timestamp // TIME_STEP)
    return _hotp(secret_b32, counter)


def verify_totp(secret_b32: str, submitted_otp: str, timestamp: float = None) -> bool:
    """Verify an OTP allowing +/- VALIDITY_WINDOW time steps of drift."""
    if timestamp is None:
        timestamp = time.time()
    current_counter = int(timestamp // TIME_STEP)

    for offset in range(-VALIDITY_WINDOW, VALIDITY_WINDOW + 1):
        candidate = _hotp(secret_b32, current_counter + offset)
        if hmac.compare_digest(candidate, submitted_otp):
            return True
    return False


def seconds_remaining(timestamp: float = None) -> int:
    if timestamp is None:
        timestamp = time.time()
    return TIME_STEP - int(timestamp % TIME_STEP)


def main():
    parser = argparse.ArgumentParser(description="TOTP OTP Generator & Verifier")
    sub = parser.add_subparsers(dest="command", required=True)

    gen = sub.add_parser("generate", help="Generate a new secret + current OTP")
    gen.add_argument("--secret", help="Existing base32 secret (generates a new one if omitted)")

    ver = sub.add_parser("verify", help="Verify a submitted OTP against a secret")
    ver.add_argument("secret", help="Base32 secret")
    ver.add_argument("otp", help="OTP code to verify")

    args = parser.parse_args()

    if args.command == "generate":
        secret = args.secret or generate_secret()
        otp = generate_totp(secret)
        print(f"Secret:  {secret}")
        print(f"OTP:     {otp}")
        print(f"Valid for another {seconds_remaining()}s (step size = {TIME_STEP}s)")

    elif args.command == "verify":
        result = verify_totp(args.secret, args.otp)
        print("VALID ✓" if result else "INVALID ✗")


if __name__ == "__main__":
    main()
