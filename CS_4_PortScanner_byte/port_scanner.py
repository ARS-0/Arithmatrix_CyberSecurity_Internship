"""
Port Scanner — Local / Authorized Targets Only
AVIP 2026 — CyberSecurity Task 4

⚠️ LEGAL & ETHICAL NOTICE ⚠️
Scanning ports on systems you do not own or do not have explicit written
authorization to test is illegal in most jurisdictions (e.g., under the
U.S. Computer Fraud and Abuse Act, UK Computer Misuse Act, and similar laws
elsewhere) and may violate your ISP's or organization's acceptable-use
policy, even if scans appear "harmless."

This tool is configured to scan ONLY localhost / loopback addresses and
private (RFC1918) IP ranges by default. To target anything else, you must
pass `--i-have-authorization`, confirming you have explicit written
permission from the target's owner to test it. All testing performed while
building this project was done exclusively against localhost (127.0.0.1).

Usage:
    python port_scanner.py 127.0.0.1 --ports 1-1024
    python port_scanner.py 127.0.0.1 --ports 22,80,443,8080
    python port_scanner.py 192.168.1.10 --ports 1-100 --i-have-authorization
"""

import argparse
import csv
import ipaddress
import json
import socket
import sys
import datetime


COMMON_SERVICES = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
    80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS",
    3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL", 8080: "HTTP-Alt",
}


def parse_ports(port_spec: str):
    ports = set()
    for part in port_spec.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-")
            ports.update(range(int(start), int(end) + 1))
        else:
            ports.add(int(part))
    return sorted(ports)


def is_authorized_target(host: str, force: bool) -> bool:
    """Only allow loopback / private IP ranges unless explicitly authorized."""
    if force:
        return True
    try:
        # Resolve hostname to IP for the check
        ip = ipaddress.ip_address(socket.gethostbyname(host))
        return ip.is_loopback or ip.is_private
    except (socket.gaierror, ValueError):
        return False


def scan_port(host: str, port: int, timeout: float = 0.5) -> str:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        result = sock.connect_ex((host, port))
        return "open" if result == 0 else "closed"
    except socket.timeout:
        return "filtered"
    except OSError:
        return "filtered"
    finally:
        sock.close()


def run_scan(host: str, ports: list, timeout: float = 0.5) -> list:
    results = []
    for port in ports:
        status = scan_port(host, port, timeout)
        results.append({
            "host": host,
            "port": port,
            "status": status,
            "service_guess": COMMON_SERVICES.get(port, "unknown"),
            "timestamp": datetime.datetime.now().isoformat(),
        })
    return results


def write_csv(results, filename):
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["host", "port", "status", "service_guess", "timestamp"])
        writer.writeheader()
        writer.writerows(results)


def write_json(results, filename, scan_params):
    with open(filename, "w") as f:
        json.dump({"scan_parameters": scan_params, "results": results}, f, indent=2)


def main():
    parser = argparse.ArgumentParser(description="Authorized-target port scanner")
    parser.add_argument("host", help="Target IP/hostname (default: loopback/private only)")
    parser.add_argument("--ports", default="1-1024", help="Port range or comma list, e.g. 1-1024 or 22,80,443")
    parser.add_argument("--timeout", type=float, default=0.5, help="Per-port timeout in seconds")
    parser.add_argument("--output", default="scan_results", help="Output filename prefix")
    parser.add_argument("--i-have-authorization", action="store_true",
                         help="Confirm you have explicit written authorization to scan this target")
    args = parser.parse_args()

    if not is_authorized_target(args.host, args.i_have_authorization):
        print("[!] Refusing to scan: target is not localhost/private, and "
              "--i-have-authorization was not provided.")
        print("[!] Only scan systems you own or have explicit written permission to test.")
        sys.exit(1)

    ports = parse_ports(args.ports)
    print(f"[+] Scanning {args.host} — {len(ports)} port(s) — timeout={args.timeout}s")

    scan_params = {
        "host": args.host,
        "ports": args.ports,
        "timeout": args.timeout,
        "scan_time": datetime.datetime.now().isoformat(),
    }

    results = run_scan(args.host, ports, args.timeout)

    open_ports = [r for r in results if r["status"] == "open"]
    print(f"[+] Scan complete. {len(open_ports)} open port(s) found:")
    for r in open_ports:
        print(f"    {r['port']}/tcp  open  ({r['service_guess']})")

    write_csv(results, f"{args.output}.csv")
    write_json(results, f"{args.output}.json", scan_params)
    print(f"[+] Full results written to {args.output}.csv and {args.output}.json")


if __name__ == "__main__":
    main()
