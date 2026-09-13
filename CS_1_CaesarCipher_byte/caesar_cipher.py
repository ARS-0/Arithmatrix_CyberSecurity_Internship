"""
Caesar Cipher — Text Encryption/Decryption
AVIP 2026 — CyberSecurity Task 1

Usage:
    python caesar_cipher.py encrypt "Hello, World!" 3
    python caesar_cipher.py decrypt "Khoor, Zruog!" 3
    python caesar_cipher.py --interactive
"""

import argparse
import sys


def shift_char(ch: str, shift: int) -> str:
    """Shift a single alphabetic character by `shift` positions.
    Non-alphabet characters (spaces, punctuation, digits) are returned unchanged.
    """
    if ch.isalpha():
        base = ord('A') if ch.isupper() else ord('a')
        return chr((ord(ch) - base + shift) % 26 + base)
    return ch


def caesar_encrypt(plaintext: str, shift: int) -> str:
    shift = shift % 26
    return ''.join(shift_char(c, shift) for c in plaintext)


def caesar_decrypt(ciphertext: str, shift: int) -> str:
    shift = shift % 26
    return ''.join(shift_char(c, -shift) for c in ciphertext)


def run_interactive():
    print("=== Caesar Cipher (Interactive Mode) ===")
    mode = input("Mode (encrypt/decrypt): ").strip().lower()
    text = input("Enter text: ")
    shift = int(input("Enter shift/key (integer): ").strip())

    if mode == "encrypt":
        result = caesar_encrypt(text, shift)
    elif mode == "decrypt":
        result = caesar_decrypt(text, shift)
    else:
        print("Invalid mode. Choose 'encrypt' or 'decrypt'.")
        sys.exit(1)

    print(f"\nResult: {result}")
    return result


def main():
    parser = argparse.ArgumentParser(description="Caesar Cipher Encryption/Decryption Tool")
    parser.add_argument("mode", nargs="?", choices=["encrypt", "decrypt"], help="Operation mode")
    parser.add_argument("text", nargs="?", help="Text to process")
    parser.add_argument("shift", nargs="?", type=int, help="Shift/key value (integer)")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")

    args = parser.parse_args()

    if args.interactive or not (args.mode and args.text is not None and args.shift is not None):
        run_interactive()
        return

    if args.mode == "encrypt":
        print(caesar_encrypt(args.text, args.shift))
    else:
        print(caesar_decrypt(args.text, args.shift))


if __name__ == "__main__":
    main()
