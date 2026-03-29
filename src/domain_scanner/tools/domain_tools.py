import socket
import ssl
import time
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from crewai.tools import tool
import wappalyzer


# ------------------------------------------------
# DNS LOOKUP
# ------------------------------------------------


@tool("DNS Lookup")
def dns_lookup(domain: str) -> str:
    """
    Resolve a domain name to its IP address.

    TOOL INPUT FORMAT:
    {"domain": "example.com"}

    RULES:
    - Pass ONLY the domain name.
    - Do NOT include http:// or https://.
    - Do NOT include explanations or extra fields.

    Example:
    {"domain": "example.com"}

    Returns:
    A string mapping the domain to its IP address.
    Example:
    example.com -> 93.184.216.34
    """
    try:
        ip = socket.gethostbyname(domain)
        return f"{domain} -> {ip}"
    except Exception as e:
        return f"TOOL_ERROR: {str(e)}"


# ------------------------------------------------
# SUBDOMAIN DISCOVERY
# ------------------------------------------------


@tool("Subdomain Discovery")
def discover_subdomains(domain: str, subdomains: list[str]) -> str:
    """
    Discover common subdomains for a given domain.

    TOOL INPUT FORMAT:
    {
        "domain": "example.com",
        "subdomains": ["www", "api", "mail"]
    }

    PARAMETER INSTRUCTIONS:
    - The "subdomains" parameter must be a list of common subdomain prefixes.
    - Generate 50–100 likely subdomains used in modern infrastructure.

    Include categories such as:
    - Web: www, blog, site
    - APIs: api, gateway
    - Infrastructure: cdn, assets, static
    - Authentication: auth, oauth, login
    - Email: mail, smtp, imap
    - Dev environments: dev, test, staging
    - Admin panels: admin, dashboard, console
    - Monitoring: status, metrics, grafana

    RULES:
    - Provide only the base domain.
    - Do NOT include protocols like https://.
    - Subdomains must be prefixes only (no full hostnames).

    Example:
    {
        "domain": "example.com",
        "subdomains": ["www", "api", "dev", "mail"]
    }

    Returns:
    A newline-separated list of discovered subdomains.
    """

    found = []

    for sub in subdomains:
        host = f"{sub}.{domain}"

        try:
            socket.gethostbyname(host)
            found.append(host)
        except Exception:
            pass

    if not found:
        return "No common subdomains discovered"

    return "\n".join(found)


# ------------------------------------------------
# FETCH WEBSITE
# ------------------------------------------------


@tool("Fetch Website HTML")
def fetch_website(domain: str) -> str:
    """
    Fetch the raw HTML of the website homepage.

    TOOL INPUT FORMAT:
    {"domain": "example.com"}

    RULES:
    - Only pass the domain.
    - Do NOT include https://.
    - Do NOT include reasoning text.

    Example:
    {"domain": "example.com"}

    Returns:
    The first 5000 characters of the homepage HTML.
    """
    try:
        r = requests.get(f"https://{domain}", timeout=10)
        return r.text[:5000]
    except Exception as e:
        return f"TOOL_ERROR: {str(e)}"


# ------------------------------------------------
# SECURITY HEADERS
# ------------------------------------------------

SECURITY_HEADERS = [
    "Content-Security-Policy",
    "Strict-Transport-Security",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
]


@tool("Security Headers Scan")
def security_headers(domain: str) -> str:
    """
    Analyze HTTP security headers of a website.

    TOOL INPUT FORMAT:
    {"domain": "example.com"}

    RULES:
    - Provide only the domain.
    - Do NOT include https://.
    - Do NOT include any extra text.

    Example:
    {"domain": "example.com"}

    Returns:
    A dictionary showing which security headers are present or missing.
    """
    try:
        r = requests.get(f"https://{domain}", timeout=10)

        results = {}
        for h in SECURITY_HEADERS:
            results[h] = r.headers.get(h, "Missing")

        return str(results)

    except Exception as e:
        return f"TOOL_ERROR: {str(e)}"


# ------------------------------------------------
# METADATA EXTRACTION
# ------------------------------------------------


@tool("Extract Metadata")
def extract_metadata(domain: str) -> str:
    """
    Extract SEO and structural metadata from a website.

    TOOL INPUT FORMAT:
    {"domain": "example.com"}

    RULES:
    - Only pass the domain.
    - Do NOT include protocol prefixes.
    - No additional fields allowed.

    Example:
    {"domain": "example.com"}

    Returns:
    - Page title
    - Meta description
    - First 10 headings (H1-H3)
    """
    try:
        r = requests.get(f"https://{domain}", timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        title = soup.title.string if soup.title else "None"

        description = ""
        meta = soup.find("meta", attrs={"name": "description"})
        if meta:
            description = meta.get("content")

        headings = [h.text.strip() for h in soup.find_all(["h1", "h2", "h3"])][:10]

        return f"""
            Title: {title}

            Description:
            {description}

            Headings:
            {headings}
            """

    except Exception as e:
        return f"TOOL_ERROR: {str(e)}"


# ------------------------------------------------
# TECH STACK DETECTION
# ------------------------------------------------


@tool("Detect Tech Stack")
def detect_tech_stack(domain: str) -> str:
    """
    Detect technologies used by the website.

    TOOL INPUT FORMAT:
    {"domain": "example.com"}

    RULES:
    - Provide only the domain name.
    - Do NOT include https://.
    - Do NOT include additional fields.

    Example:
    {"domain": "example.com"}

    Returns:
    A list of detected technologies (frameworks, CMS, etc).
    """
    try:
        url = f"https://{domain}"

        tech = wappalyzer.analyze(url)

        return f"Technologies: {list(tech)}"

    except Exception as e:
        return f"TOOL_ERROR: {str(e)}"


# ------------------------------------------------
# SSL CERTIFICATE ANALYSIS
# ------------------------------------------------


@tool("SSL Certificate Analysis")
def analyze_ssl_certificate(domain: str) -> str:
    """
    Retrieve SSL/TLS certificate details for a domain.

    TOOL INPUT FORMAT:
    {"domain": "example.com"}

    RULES:
    - Pass only the domain.
    - Do NOT include protocols.
    - No extra text or fields.

    Example:
    {"domain": "example.com"}

    Returns:
    Certificate subject, issuer, and validity period.
    """
    try:
        ctx = ssl.create_default_context()

        with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
            s.settimeout(5)
            s.connect((domain, 443))
            cert = s.getpeercert()

        issuer = dict(x[0] for x in cert["issuer"])
        subject = dict(x[0] for x in cert["subject"])

        return f"""
            Subject: {subject}
            Issuer: {issuer}
            Valid From: {cert['notBefore']}
            Valid Until: {cert['notAfter']}
            """

    except Exception as e:
        return f"TOOL_ERROR: {str(e)}"


# ------------------------------------------------
# PARALLEL WEBSITE CRAWLER
# ------------------------------------------------


def fetch_page(url):
    try:
        r = requests.get(url, timeout=10)
        return r.text
    except Exception:
        return ""


@tool("Parallel Website Crawler")
def crawl_website(domain: str) -> str:
    """
    Crawl the homepage and discover internal links.

    TOOL INPUT FORMAT:
    {"domain": "example.com"}

    RULES:
    - Provide only the domain.
    - Do NOT include https://.
    - No extra text.

    Example:
    {"domain": "example.com"}

    Returns:
    - List of discovered internal pages
    - Number of pages fetched
    """
    try:
        base = f"https://{domain}"

        r = requests.get(base, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        links = set()

        for a in soup.find_all("a", href=True):
            url = urljoin(base, a["href"])
            parsed = urlparse(url)

            if parsed.netloc == domain:
                links.add(url)

        links = list(links)[:20]

        with ThreadPoolExecutor(max_workers=5) as ex:
            pages = list(ex.map(fetch_page, links))

        return f"""
            Discovered pages:
            {links}

            Pages fetched:
            {len(pages)}
            """

    except Exception as e:
        return f"TOOL_ERROR: {str(e)}"


# ------------------------------------------------
# ROBOTS.TXT ANALYSIS
# ------------------------------------------------


@tool("Robots.txt Analyzer")
def analyze_robots(domain: str) -> str:
    """
    Retrieve and analyze the robots.txt file.

    TOOL INPUT FORMAT:
    {"domain": "example.com"}

    RULES:
    - Only pass the domain.
    - No protocol prefixes.

    Example:
    {"domain": "example.com"}

    Returns:
    The first 2000 characters of robots.txt.
    """
    try:
        url = f"https://{domain}/robots.txt"

        r = requests.get(url, timeout=10)

        return r.text[:2000]

    except Exception as e:
        return f"TOOL_ERROR: {str(e)}"


# ------------------------------------------------
# SITEMAP ANALYSIS
# ------------------------------------------------


@tool("Sitemap Analyzer")
def analyze_sitemap(domain: str) -> str:
    """
    Retrieve the sitemap.xml of a website.

    TOOL INPUT FORMAT:
    {"domain": "example.com"}

    RULES:
    - Provide only the domain.
    - Do NOT include https://.

    Example:
    {"domain": "example.com"}

    Returns:
    The first 2000 characters of sitemap.xml.
    """
    try:
        url = f"https://{domain}/sitemap.xml"

        r = requests.get(url, timeout=10)

        return r.text[:2000]

    except Exception as e:
        return f"TOOL_ERROR: {str(e)}"


# ------------------------------------------------
# PERFORMANCE TEST
# ------------------------------------------------


@tool("Performance Measurement")
def measure_performance(domain: str) -> str:
    """
    Measure website response performance.

    TOOL INPUT FORMAT:
    {"domain": "example.com"}

    RULES:
    - Only pass the domain.
    - Do NOT include protocols.

    Example:
    {"domain": "example.com"}

    Returns:
    - HTTP status code
    - Response time
    - Content length
    """
    try:
        url = f"https://{domain}"

        start = time.time()
        r = requests.get(url, timeout=10)
        end = time.time()

        latency = end - start

        return f"""
                Status Code: {r.status_code}
                Response Time: {latency:.3f} seconds
                Content Length: {len(r.content)}
                """

    except Exception as e:
        return f"TOOL_ERROR: {str(e)}"


# ------------------------------------------------
# PORTS SCAN
# ------------------------------------------------


@tool("Port Scanner")
def scan_ports(host: str, ports: list[int]) -> str:
    """
    Scan common ports on a target host.

    TOOL INPUT FORMAT:
    {
        "host": "example.com",
        "ports": [80, 443, 22]
    }

    PARAMETER INSTRUCTIONS:
    - The "ports" parameter must be a list of common TCP ports.
    - Generate 50–100 commonly used ports in modern infrastructure.

    Include categories such as:
    - Web: 80, 443, 8080, 8443
    - Remote access: 22 (SSH), 3389 (RDP), 5900 (VNC)
    - File transfer: 20, 21 (FTP), 989, 990 (FTPS)
    - Email: 25 (SMTP), 465, 587, 110 (POP3), 995, 143 (IMAP), 993
    - Databases: 3306 (MySQL), 5432 (PostgreSQL), 1433 (MSSQL), 27017 (MongoDB), 6379 (Redis)
    - Dev services: 3000, 5000, 5173, 8000
    - Infrastructure: 53 (DNS), 123 (NTP), 161 (SNMP)
    - Message brokers: 5672 (RabbitMQ), 9092 (Kafka)
    - Monitoring: 9090 (Prometheus), 3000 (Grafana)

    RULES:
    - Provide only port numbers.
    - Do NOT include protocols.
    - Ports must be integers.

    Example:
    {
        "host": "example.com",
        "ports": [22, 80, 443, 3306]
    }

    Returns:
    A newline-separated list of open ports.
    """

    open_ports = []

    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)

            result = sock.connect_ex((host, port))
            if result == 0:
                open_ports.append(port)

            sock.close()

        except Exception:
            pass

    if not open_ports:
        return "No open ports discovered"

    return "\n".join(str(p) for p in open_ports)
