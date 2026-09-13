# Task 3 — Ethical Keylogger Simulation (Own System Only)

AVIP 2026 — CyberSecurity Track — Task 3

## ⚠️ Ethical Usage, Consent & Legal Compliance — READ FIRST

This project is a **local-only, educational** demonstration of how keystroke
capture and secure logging work. It is **not** designed, intended, or
distributed for surveilling anyone else's device.

- ✅ Run this **only** on a device you personally own, or one where you have
  explicit, documented consent from the owner.
- ✅ Fill in and keep `consent_declaration.txt` with your submission — this
  is a signed statement confirming testing was done ethically.
- ✅ Captured data is written **only** to your local disk, and only in
  **encrypted** form (Fernet/AES via the `cryptography` library).
- ✅ Use `--purge` to permanently delete the log and encryption key once
  you're done demonstrating.
- 🚫 Do not deploy this on shared, work, school, or any other person's
  device without their explicit knowledge and written consent.
- 🚫 In most jurisdictions, capturing another person's keystrokes without
  consent is illegal (wiretapping / computer-misuse statutes) — this
  project must never be used that way.

The program itself asks for an explicit "yes/no" confirmation before every
capture session as a safeguard.

## How It Works
1. `pynput` listens for key-press events on the local machine only.
2. Captured text is buffered, timestamped, and encrypted with a locally
   generated Fernet (AES-128) key before being written to disk.
3. The encryption key is stored in `secret.key` — treat it like a password.
4. `--decrypt` reads the log back and decrypts it for review.
5. `--purge` deletes both the log and the key.

## Usage
```bash
pip install pynput cryptography

# Capture keystrokes on THIS machine for 30 seconds (asks for consent confirmation)
python keylogger_sim.py --capture 30

# Decrypt and view the captured log
python keylogger_sim.py --decrypt

# Permanently delete the log + encryption key
python keylogger_sim.py --purge
```

## Files
- `keylogger_sim.py` — main implementation (capture, encrypt, decrypt, purge)
- `consent_declaration.txt` — **signed** declaration template (fill in before submitting)
- `keystrokes.log.enc.sample` — sanitized sample encrypted log (demo data only, not real captured keystrokes)
- `secret.key.sample` — sample key used to produce the sample log above (for demo/reproducibility only — never share a real key)

## Sample Demonstration Output
```
[+] Capturing keystrokes for 30 seconds on THIS machine only.
[+] Press Ctrl+C to stop early.
[+] Capture stopped after 30s. Encrypted log saved to keystrokes.log.enc

Decrypted entries:
[2026-09-08T11:46:33] hello world [SPACE]
[2026-09-08T11:46:33] this is a sanitized demo entry
```
(Full sanitized sample available in `keystrokes.log.enc.sample`, decryptable
with `secret.key.sample`.)
