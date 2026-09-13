# AVIP 2026 — CyberSecurity Internship Tasks

Arithmatrix Virtual Internship Program (AVIP) 2026 — B.Y.T.E CyberSecurity Track

This repository contains completed tasks for the CyberSecurity internship
track. Each task lives in its own folder with its own code, README,
documentation, and sample outputs.

> ⚠️ **GitHub naming note:** Per the AVIP SOPs, each task should be pushed as
> its own **public repository** named `CS_<TaskNumber>_<TaskTitle>_byte`
> (e.g. `CS_1_CaesarCipher_byte`). This project folder is organized as one
> subfolder per task so you can push each one individually — see
> **"Splitting into separate GitHub repos"** below.

## Tasks Completed

| # | Task | Folder | Status |
|---|---|---|---|
| 1 | Caesar Cipher (Text Encryption/Decryption) | `CS_1_CaesarCipher_byte/` | ✅ Complete |
| 2 | Password Strength Checker | `CS_2_PasswordStrengthChecker_byte/` | ✅ Complete |
| 3 | Ethical Keylogger Simulation (Own System Only) | `CS_3_KeyloggerSimulation_byte/` | ✅ Complete |
| 4 | Port Scanner (Local/Authorized Targets Only) | `CS_4_PortScanner_byte/` | ✅ Complete |
| 5 | OTP Generator & Verifier | `CS_5_OTPGeneratorVerifier_byte/` | ✅ Complete |
| 6 | Steganography (Hide/Extract Text in Image) | `CS_6_Steganography_byte/` | ✅ Complete |

Remember: **you only need 2 tasks for a Completion Certificate and 3 for a
LoR** — pick whichever subset satisfies your Offer Letter requirement, or
submit all six.

## Requirements
Each folder that needs external packages has its own `requirements.txt`.
Overall, across all tasks you'll need:
```bash
pip install pynput cryptography Pillow
```
(Tasks 1, 2, 4, and 5 use only the Python standard library.)

## Splitting Into Separate GitHub Repos
The SOPs ask for one public repo per task, named
`DomainShortHand_TaskNumber_TaskTitle_byte`. From inside each task folder:

```bash
cd CS_1_CaesarCipher_byte
git init
git add .
git commit -m "feat: initial implementation of Caesar cipher tool"
git branch -M main
git remote add origin https://github.com/<your-username>/CS_1_CaesarCipher_byte.git
git push -u origin main
```
Repeat for each task folder, updating the repo name to match
(`CS_2_PasswordStrengthChecker_byte`, `CS_3_KeyloggerSimulation_byte`, etc.).
Make sure each repository's visibility is set to **Public** on GitHub.

## Deployment
Tasks 1, 2, and 5 are pure CLI/logic tools — you can optionally wrap any of
them in a tiny Flask/FastAPI app and deploy to **Render** if you want a live
demo URL (the SOPs' 3-step deploy guide: push to GitHub → connect Render or
Vercel → deploy). Tasks 3 and 4 are local-system tools by design (a
keylogger and a port scanner are meant to run against local machines, not be
exposed as public web services) — for those, a recorded terminal demo/GIF in
the README is the appropriate "deliverable," and that's already included as
`*.txt` transcripts in each folder.

## Ethics Reminder
Tasks 3 (Keylogger Simulation) and 4 (Port Scanner) touch on techniques that
are only legal and appropriate to use against **systems you own or have
explicit written authorization to test**. Each of those folders has its own
detailed ethics/legal notice — read it before running or sharing that code.
