# Task 1 — Caesar Cipher (Text Encryption/Decryption)

AVIP 2026 — CyberSecurity Track — Task 1

## Overview
A command-line tool that encrypts and decrypts text using the classic Caesar
cipher. It supports any integer shift value and preserves all non-alphabet
characters (spaces, digits, punctuation) unchanged.

## Features
- Configurable shift/key (positive or negative integers, auto-wrapped mod 26)
- Preserves case (uppercase stays uppercase, lowercase stays lowercase)
- Preserves non-alphabetic characters exactly as typed
- CLI mode and interactive mode

## Usage

### Command-line mode
```bash
python caesar_cipher.py encrypt "Hello, World!" 3
# Output: Khoor, Zruog!

python caesar_cipher.py decrypt "Khoor, Zruog!" 3
# Output: Hello, World!
```

### Interactive mode
```bash
python caesar_cipher.py --interactive
```
You will be prompted for mode, text, and shift value.

## Example Input/Output

| Input Text | Shift | Mode | Output |
|---|---|---|---|
| `Hello, World! 123` | 3 | encrypt | `Khoor, Zruog! 123` |
| `Khoor, Zruog! 123` | 3 | decrypt | `Hello, World! 123` |
| `Attack at Dawn` | 13 | encrypt | `Nggnpx ng Qnja` |

See `sample_transcript.txt` for a recorded execution and `sample_run.txt` for
raw CLI output.

## Files
- `caesar_cipher.py` — main implementation
- `sample_transcript.txt` — recorded demo transcript
- `sample_run.txt` — raw CLI run output

## Notes
This is a classical/historical cipher for educational purposes only — it is
**not cryptographically secure** and should never be used to protect real
sensitive data (it can be broken by brute force in 25 tries, or by frequency
analysis).
