# Task 6 — Steganography: Hide/Extract Text in Image

AVIP 2026 — CyberSecurity Track — Task 6

## Overview
A Least-Significant-Bit (LSB) steganography tool that hides a text message
inside an image by modifying the least-significant bit of each RGB color
channel — changes that are visually imperceptible to the human eye.

## How It Works
1. The message is UTF-8 encoded and prefixed with a 32-bit length header.
2. Each bit of (header + message) replaces the least-significant bit of one
   R/G/B channel value, pixel by pixel.
3. To extract, the tool reads the same bits back out: first the 32-bit
   header (to know how many bytes follow), then the message bits, which are
   reassembled into the original text.

## Supported Formats & Capacity
- **Output must be PNG** (lossless). JPEG compression would destroy the
  hidden LSB data, so JPEG output is not supported.
- **Capacity:** 3 bits per pixel (R, G, B). A `W x H` image can hold up to
  `(W × H × 3 − 32) / 8` bytes of text. E.g. a 200×200 image holds ~14,993
  characters.

## Usage
```bash
# Hide a message inside cover_image.png, save result as stego_image.png
python stego_tool.py embed cover_image.png "This is a secret message" stego_image.png

# Extract the hidden message from a stego image
python stego_tool.py extract stego_image.png
```

## Demonstration
```
$ python stego_tool.py embed cover_image.png "This is a secret message for AVIP 2026 Task 6 demo." stego_image.png
[+] Message embedded (51 chars / 440 bits used of 120000 available). Saved to: stego_image.png

$ python stego_tool.py extract stego_image.png
[+] Extracted message: This is a secret message for AVIP 2026 Task 6 demo.
```
Extracted text matches the original exactly — see `extraction_proof.txt`.

## Files
- `stego_tool.py` — main implementation (embed/extract)
- `cover_image.png` — example cover image (before hiding data)
- `stego_image.png` — example stego image (after hiding data — visually identical to the cover)
- `extraction_proof.txt` — captured output proving correct extraction

## Notes
LSB steganography hides data from casual visual inspection but is **not
encryption** — it can be detected by statistical steganalysis tools. For
real confidentiality, encrypt the message (e.g. with the AES/Fernet approach
used in Task 3) before embedding it.
