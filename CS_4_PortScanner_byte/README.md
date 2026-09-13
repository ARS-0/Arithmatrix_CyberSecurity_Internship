# Task 4 — Port Scanner (Local / Authorized Targets Only)

AVIP 2026 — CyberSecurity Track — Task 4

## ⚠️ Legal & Ethics Notice

Port scanning a system without the owner's explicit permission is illegal in
most jurisdictions (e.g. the U.S. Computer Fraud and Abuse Act, UK Computer
Misuse Act, and equivalent laws elsewhere), even when the scan itself causes
no damage.

This tool **only scans loopback (`127.0.0.1`) and private/RFC1918 IP ranges
by default**. Any other target is blocked unless you pass
`--i-have-authorization`, an explicit flag confirming you hold written
permission to test that host. **All testing for this submission was
performed exclusively against `127.0.0.1` (localhost).**

## Features
- Configurable host + port range (`22`, `1-1024`, `22,80,443`, etc.)
- TCP connect-scan reporting `open` / `closed` / `filtered`
- Structured output in both CSV and JSON, including timestamp and scan
  parameters
- Built-in guard rail restricting scans to authorized targets

## Usage
```bash
# Scan common ports on localhost
python port_scanner.py 127.0.0.1 --ports 1-1024

# Scan specific ports
python port_scanner.py 127.0.0.1 --ports 22,80,443,8080

# Scanning anything outside localhost/private ranges requires this flag,
# and you must actually have authorization to do so:
python port_scanner.py 192.168.1.10 --ports 1-100 --i-have-authorization
```

## Example Output
```
[+] Scanning 127.0.0.1 — 10 port(s) — timeout=0.5s
[+] Scan complete. 1 open port(s) found:
    8000/tcp  open  (unknown)
[+] Full results written to sample_scan_results.csv and sample_scan_results.json
```
(Port 8000 was open in this demo because a local `python -m http.server 8000`
instance was running on localhost during the test.)

## Files
- `port_scanner.py` — main implementation
- `sample_scan_results.csv` / `sample_scan_results.json` — sample structured output
- `scan_run_screenshot.txt` — captured terminal run

## Notes
This is a basic TCP-connect scanner suitable for learning fundamentals. It is
intentionally simple (no SYN-stealth scanning, no OS fingerprinting) — tools
like `nmap` are far more capable and should be used for real authorized
security testing.
