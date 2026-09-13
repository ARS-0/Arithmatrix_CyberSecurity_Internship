"""
Steganography: Hide/Extract Text in Image (LSB method)
AVIP 2026 — CyberSecurity Task 6

Method: Least Significant Bit (LSB) substitution.
  - The message is converted to bits and a 32-bit length header is prepended.
  - Each bit replaces the least-significant bit of one pixel color channel
    (R, G, B — alpha untouched), which is visually imperceptible.

Supported formats: PNG (lossless — required; JPEG's compression destroys
LSB data, so JPEG is NOT supported for output).

Capacity: 3 bits per pixel (R, G, B channels) minus 32 bits for the length
header. E.g. a 100x100 image has 100*100*3 - 32 = 29,968 usable bits =
~3,746 bytes (~3,746 ASCII characters).
"""

import argparse
from PIL import Image


def _text_to_bits(text: str) -> str:
    data = text.encode("utf-8")
    length_header = format(len(data), "032b")  # 32-bit length prefix (bytes)
    bit_string = "".join(format(byte, "08b") for byte in data)
    return length_header + bit_string


def _bits_to_text(bits: str) -> str:
    byte_chunks = [bits[i:i + 8] for i in range(0, len(bits), 8)]
    byte_values = bytes(int(b, 2) for b in byte_chunks)
    return byte_values.decode("utf-8", errors="replace")


def capacity_bits(img: Image.Image) -> int:
    width, height = img.size
    return width * height * 3  # R, G, B channels


def embed_text(cover_path: str, message: str, output_path: str):
    img = Image.open(cover_path)
    img = img.convert("RGB")
    pixels = img.load()
    width, height = img.size

    bits = _text_to_bits(message)
    total_capacity = capacity_bits(img)
    if len(bits) > total_capacity:
        max_chars = (total_capacity - 32) // 8
        raise ValueError(
            f"Message too long for this image. Capacity ~{max_chars} characters, "
            f"message is {len(message)} characters."
        )

    bit_index = 0
    for y in range(height):
        for x in range(width):
            if bit_index >= len(bits):
                break
            r, g, b = pixels[x, y]
            channels = [r, g, b]
            for c in range(3):
                if bit_index < len(bits):
                    channels[c] = (channels[c] & ~1) | int(bits[bit_index])
                    bit_index += 1
            pixels[x, y] = tuple(channels)
        if bit_index >= len(bits):
            break

    img.save(output_path, "PNG")
    print(f"[+] Message embedded ({len(message)} chars / {len(bits)} bits used "
          f"of {total_capacity} available). Saved to: {output_path}")


def extract_text(stego_path: str) -> str:
    img = Image.open(stego_path)
    img = img.convert("RGB")
    pixels = img.load()
    width, height = img.size

    # First extract the 32-bit length header
    header_bits = []
    bit_index = 0
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            for c in (r, g, b):
                if bit_index < 32:
                    header_bits.append(str(c & 1))
                    bit_index += 1
            if bit_index >= 32:
                break
        if bit_index >= 32:
            break

    message_length_bytes = int("".join(header_bits), 2)
    total_bits_needed = 32 + message_length_bytes * 8

    all_bits = []
    bit_index = 0
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            for c in (r, g, b):
                if bit_index < total_bits_needed:
                    all_bits.append(str(c & 1))
                    bit_index += 1
            if bit_index >= total_bits_needed:
                break
        if bit_index >= total_bits_needed:
            break

    message_bits = "".join(all_bits[32:])
    return _bits_to_text(message_bits)


def main():
    parser = argparse.ArgumentParser(description="LSB Steganography — embed/extract text in PNG images")
    sub = parser.add_subparsers(dest="command", required=True)

    embed = sub.add_parser("embed", help="Hide text inside an image")
    embed.add_argument("cover_image", help="Path to cover image (any format Pillow can read)")
    embed.add_argument("message", help="Text message to hide")
    embed.add_argument("output_image", help="Output path for stego image (will be saved as PNG)")

    extract = sub.add_parser("extract", help="Extract hidden text from a stego image")
    extract.add_argument("stego_image", help="Path to stego PNG image")

    args = parser.parse_args()

    if args.command == "embed":
        embed_text(args.cover_image, args.message, args.output_image)
    elif args.command == "extract":
        message = extract_text(args.stego_image)
        print(f"[+] Extracted message: {message}")


if __name__ == "__main__":
    main()
