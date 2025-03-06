import requests
from rich import print
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

# Initialize console
console = Console()

# Display Large Banner for "AMARU"
banner_text = Text("\nA M A R U", style="bold color(214)")
sub_banner_text = Text("\nhttps://amaru.co.nz/", style="bold white")
third_line_text = Text("\nSecurity Headers Validator", style="bold white")

console.print(Panel.fit(banner_text.append(sub_banner_text).append(third_line_text), border_style="bold white"))

# Ask for URL
url = input("Enter the URL (e.g., https://example.com): ").strip()

# Security headers that should be present
required_headers = [
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
]

# Deprecated headers
deprecated_headers = [
    "Feature-Policy",
    "Expect-CT",
    "Public-Key-Pins",
    "X-XSS-Protection",
    "Pragma",
]

# Fetch headers
try:
    response = requests.get(url, timeout=5)
    headers = response.headers
except requests.RequestException as e:
    console.print(f"[bold red]Error:[/bold red] Could not fetch headers for {url}. Check the URL or your connection.")
    exit()

# Create table for security headers
security_table = Table(title="Security Headers Analysis", show_header=True, header_style="bold magenta")
security_table.add_column("Header", style="cyan", justify="left")
security_table.add_column("Status", style="bold", justify="center")

# Check security headers
for header in required_headers:
    if header in headers:
        security_table.add_row(header, "[green]Implemented[/green]")
    else:
        security_table.add_row(header, "[red]Not Implemented[/red]")

# Create table for deprecated headers
deprecated_table = Table(title="Deprecated Headers Check", show_header=True, header_style="bold magenta")
deprecated_table.add_column("Header", style="cyan", justify="left")
deprecated_table.add_column("Status", style="bold", justify="center")

# Check deprecated headers
for header in deprecated_headers:
    if header in headers:
        deprecated_table.add_row(header, "[red]Implemented (Deprecated!)[/red]")
    else:
        deprecated_table.add_row(header, "[green]Not Implemented[/green]")

# Print tables
console.print(security_table)
console.print(deprecated_table)

# Add final note
note_text = Text(
    "\nIt is worth noting that the Content-Security-Policy (CSP) frame-ancestors directive obsoletes the X-Frame-Options header.\n"
    "If a resource has both policies, the CSP frame-ancestors policy will be enforced, and the X-Frame-Options policy will be ignored.",
    style="bold yellow",
)
console.print(Panel.fit(note_text, border_style="bold blue"))
