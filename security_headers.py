#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# AMARU - Security Headers Validator
# Author: Cristopher Provoste
# Version: 2026

import requests
import sys
from colorama import init, Fore, Style
init(autoreset=True)

# ==================== CONFIG ====================
WEB_HEADERS = [
    "Strict-Transport-Security",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Content-Security-Policy",
    "X-Permitted-Cross-Domain-Policies",
    "Referrer-Policy",
    "Clear-Site-Data",
    "Cross-Origin-Embedder-Policy",
    "Cross-Origin-Opener-Policy",
    "Cross-Origin-Resource-Policy",
    "Cache-Control",
    "X-DNS-Prefetch-Control",
    "Permissions-Policy"
]

API_HEADERS = [
    "Cache-Control",
    "Content-Security-Policy",
    "Content-Type",
    "Strict-Transport-Security",
    "X-Content-Type-Options",
    "X-Frame-Options"
]

DEPRECATED_HEADERS = [
    "Feature-Policy",
    "Expect-CT",
    "Public-Key-Pins",
    "X-XSS-Protection",
    "Pragma"
]

# ==================== BANNER ====================
def print_banner():
    banner = f"""
{Fore.YELLOW}╔──────────────────────────────────────────────────────────╗
{Fore.YELLOW}║{Fore.WHITE}{Style.BRIGHT}                    █████╗ ███╗   ███╗ █████╗ ██████╗ ██╗   ██╗{Style.RESET_ALL}{Fore.YELLOW}                  ║
{Fore.YELLOW}║{Fore.WHITE}{Style.BRIGHT}                   ██╔══██╗████╗ ████║██╔══██╗██╔══██╗██║   ██║{Style.RESET_ALL}{Fore.YELLOW}                   ║
{Fore.YELLOW}║{Fore.WHITE}{Style.BRIGHT}                   ███████║██╔████╔██║███████║██████╔╝██║   ██║{Style.RESET_ALL}{Fore.YELLOW}                   ║
{Fore.YELLOW}║{Fore.WHITE}{Style.BRIGHT}                   ██╔══██║██║╚██╔╝██║██╔══██║██╔══██╗██║   ██║{Style.RESET_ALL}{Fore.YELLOW}                   ║
{Fore.YELLOW}║{Fore.WHITE}{Style.BRIGHT}                   ██║  ██║██║ ╚═╝ ██║██║  ██║██║  ██║╚██████╔╝{Style.RESET_ALL}{Fore.YELLOW}                   ║
{Fore.YELLOW}║{Fore.WHITE}{Style.BRIGHT}                   ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ {Style.RESET_ALL}{Fore.YELLOW}                   ║
{Fore.YELLOW}╚──────────────────────────────────────────────────────────╝
                     {Fore.CYAN}{Style.BRIGHT}Security Headers Validator{Style.RESET_ALL}
    """
    print(banner)

# ==================== MAIN ====================
def main():
    print_banner()

    print(f"{Fore.CYAN}[?] What are you scanning today?")
    print("    1) Web Frontend")
    print("    2) API Endpoint")
    choice = input(f"{Fore.YELLOW}[>] Choose (1 or 2): {Style.RESET_ALL}").strip()

    if choice == "1":
        mode = "web"
        expected_headers = WEB_HEADERS
        print(f"{Fore.GREEN}[+] Selected: Web Frontend")
    elif choice == "2":
        mode = "api"
        expected_headers = API_HEADERS
        print(f"{Fore.GREEN}[+] Selected: API Endpoint")
    else:
        print(f"{Fore.RED}[-] Invalid choice. Exiting.")
        sys.exit(1)

    target = input(f"{Fore.YELLOW}[>] Enter target URL (e.g. https://example.com): {Style.RESET_ALL}").strip()
    if not target.startswith("http"):
        target = "https://" + target

    token = input(f"{Fore.YELLOW}[?] Auth Token (Bearer/JWT/etc) - optional, press Enter to skip: {Style.RESET_ALL}").strip()

    headers = {}
    if token:
        headers["Authorization"] = token
        print(f"{Fore.GREEN}[+] Using authenticated request")

    try:
        print(f"\n{Fore.CYAN}[*] Sending request to {target} ...")
        response = requests.get(target, headers=headers, verify=False, timeout=10, allow_redirects=True)
        print(f"{Fore.GREEN}[+] Response: {response.status_code} {response.reason}\n")

        received_headers = {k.lower(): v for k, v in response.headers.items()}
        missing = []
        present = []

        print(f"{Fore.MAGENTA}{Style.BRIGHT}=== SECURITY HEADERS CHECK ({mode.upper()}) ===\n")

        for header in expected_headers:
            h_lower = header.lower()
            if h_lower in received_headers:
                print(f"{Fore.GREEN}[+] {header:35} → {received_headers[h_lower]}")
                present.append(header)
            else:
                print(f"{Fore.RED}[-] {header:35} → MISSING")
                missing.append(header)

        print(f"\n{Fore.MAGENTA}{Style.BRIGHT}=== DEPRECATED HEADERS ===")
        deprecated_found = False
        for header in DEPRECATED_HEADERS:
            h_lower = header.lower()
            if h_lower in received_headers:
                print(f"{Fore.YELLOW}[!] {header:35} → {received_headers[h_lower]} (DEPRECATED)")
                deprecated_found = True
        if not deprecated_found:
            print(f"{Fore.GREEN}[+] No deprecated headers found")

        print(f"\n{Fore.CYAN}{Style.BRIGHT}=== SUMMARY ===")
        print(f"{Fore.GREEN}Present : {len(present)} / {len(expected_headers)}")
        print(f"{Fore.RED}Missing : {len(missing)}")
        if missing:
            print(f"{Fore.RED}Missing headers: {', '.join(missing)}")

        print(f"\n{Fore.CYAN}{Style.BRIGHT}=== REFERENCES ===")
        if mode == "web":
            print(f"Web: https://owasp.org/www-project-secure-headers/")
        else:
            print(f"API: https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html")

        print(f"\n{Fore.YELLOW}{Style.BRIGHT}=== NOTES ===")
        print(f"• CSP frame-ancestors directive obsoletes X-Frame-Options")
        print(f"• Clear-Site-Data is recommended on logout/session expiry")

    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}[-] Request failed: {e}")
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[-] Aborted by user.")
    
    print(f"\n{Fore.MAGENTA}{Style.BRIGHT}Scan complete. Stay dangerous. — AMARU\n")

if __name__ == "__main__":
    try:
        import requests
    except ImportError:
        print("Installing requests...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "colorama"])
        import requests
    
    try:
        from colorama import init
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "colorama"])
    
    main()