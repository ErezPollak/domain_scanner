import pytest
import socket
import ssl
from unittest.mock import MagicMock, patch

# Importing tools directly from domain_tools to test the underlying business logic
from domain_scanner.tools.domain_tools import (
    dns_lookup,
    discover_subdomains,
    fetch_website,
    SECURITY_HEADERS,
    security_headers,
    extract_metadata,
    detect_tech_stack,
    analyze_ssl_certificate,
    crawl_website,
    analyze_robots,
    analyze_sitemap,
    measure_performance,
    scan_ports
)

@pytest.fixture
def mock_requests_get(mocker):
    return mocker.patch('domain_scanner.tools.domain_tools.requests.get')

@pytest.fixture
def mock_socket_gethostbyname(mocker):
    return mocker.patch('domain_scanner.tools.domain_tools.socket.gethostbyname')

# --- dns_lookup ---
def test_dns_lookup_success(mock_socket_gethostbyname):
    mock_socket_gethostbyname.return_value = "1.2.3.4"
    result = dns_lookup.func("example.com")
    assert result == "example.com -> 1.2.3.4"
    mock_socket_gethostbyname.assert_called_once_with("example.com")

def test_dns_lookup_failure(mock_socket_gethostbyname):
    mock_socket_gethostbyname.side_effect = Exception("Not found")
    result = dns_lookup.func("invalid.domain")
    assert result == "Not found"

# --- discover_subdomains ---
def test_discover_subdomains_success(mock_socket_gethostbyname):
    def side_effect(host):
        if host == "www.example.com":
            return "1.1.1.1"
        raise Exception("Not found")

    mock_socket_gethostbyname.side_effect = side_effect
    
    subdomains = ["www", "api"]
    result = discover_subdomains.func("example.com", subdomains)
    
    assert result == "www.example.com"

def test_discover_subdomains_none_found(mock_socket_gethostbyname):
    mock_socket_gethostbyname.side_effect = Exception("Not found")
    
    subdomains = ["www", "api"]
    result = discover_subdomains.func("example.com", subdomains)
    
    assert result == "No common subdomains discovered"

# --- fetch_website ---
def test_fetch_website_success(mock_requests_get):
    mock_response = MagicMock()
    mock_response.text = "<html><body>Home</body></html>"
    mock_requests_get.return_value = mock_response
    
    result = fetch_website.func("example.com")
    assert result == "<html><body>Home</body></html>"
    mock_requests_get.assert_called_once_with("https://example.com", timeout=10)

# --- security_headers ---
def test_security_headers(mock_requests_get):
    mock_response = MagicMock()
    mock_response.headers = {
        "Content-Security-Policy": "default-src 'self'",
        "X-Content-Type-Options": "nosniff"
    }
    mock_requests_get.return_value = mock_response
    
    result = security_headers.func("example.com")
    assert "Content-Security-Policy" in result
    assert "nosniff" in result
    assert "Missing" in result

# --- extract_metadata ---
def test_extract_metadata(mock_requests_get):
    mock_response = MagicMock()
    mock_response.text = '''
    <html>
      <head>
        <title>Test Page</title>
        <meta name="description" content="A test page description">
      </head>
      <body>
        <h1>Heading 1</h1>
        <h2>Heading 2</h2>
      </body>
    </html>
    '''
    mock_requests_get.return_value = mock_response
    
    result = extract_metadata.func("example.com")
    assert "Title: Test Page" in result
    assert "A test page description" in result
    assert "['Heading 1', 'Heading 2']" in result

# --- detect_tech_stack ---
@patch('domain_scanner.tools.domain_tools.wappalyzer.analyze')
def test_detect_tech_stack(mock_analyze):
    mock_analyze.return_value = {"React", "Node.js"}
    result = detect_tech_stack.func("example.com")
    assert "React" in result
    assert "Node.js" in result

# --- analyze_ssl_certificate ---
@patch('domain_scanner.tools.domain_tools.ssl.create_default_context')
@patch('domain_scanner.tools.domain_tools.socket.socket')
def test_analyze_ssl_certificate(mock_socket, mock_create_context):
    mock_ssl_sock = MagicMock()
    mock_ssl_sock.getpeercert.return_value = {
        "issuer": [[["commonName", "Test Issuer"]]],
        "subject": [[["commonName", "example.com"]]],
        "notBefore": "Jan 1 00:00:00 2024 GMT",
        "notAfter": "Jan 1 00:00:00 2025 GMT",
    }
    
    mock_ctx = MagicMock()
    mock_ctx.wrap_socket.return_value.__enter__.return_value = mock_ssl_sock
    mock_create_context.return_value = mock_ctx
    
    result = analyze_ssl_certificate.func("example.com")
    assert "Test Issuer" in result
    assert "example.com" in result
    assert "Jan 1 00:00:00 2025 GMT" in result

# --- analyze_robots ---
def test_analyze_robots(mock_requests_get):
    mock_response = MagicMock()
    mock_response.text = "User-agent: *\nDisallow: /admin"
    mock_requests_get.return_value = mock_response
    
    result = analyze_robots.func("example.com")
    assert result == "User-agent: *\nDisallow: /admin"
    mock_requests_get.assert_called_once_with("https://example.com/robots.txt", timeout=10)

# --- analyze_sitemap ---
def test_analyze_sitemap(mock_requests_get):
    mock_response = MagicMock()
    mock_response.text = "<urlset><url><loc>https://example.com</loc></url></urlset>"
    mock_requests_get.return_value = mock_response
    
    result = analyze_sitemap.func("example.com")
    assert result == "<urlset><url><loc>https://example.com</loc></url></urlset>"

# --- measure_performance ---
@patch('domain_scanner.tools.domain_tools.time.time')
def test_measure_performance(mock_time, mock_requests_get):
    # simulate latency of 1.5 seconds
    mock_time.side_effect = [10.0, 11.5]
    
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b'abcdef' # len=6
    mock_requests_get.return_value = mock_response
    
    result = measure_performance.func("example.com")
    assert "Status Code: 200" in result
    assert "Response Time: 1.500 seconds" in result
    assert "Content Length: 6" in result

# --- scan_ports ---
@patch('domain_scanner.tools.domain_tools.socket.socket')
def test_scan_ports(mock_socket):
    mock_sock_instance = MagicMock()
    # Mock connect_ex to return 0 for port 80 (success) and 1 for port 443 (fail)
    mock_sock_instance.connect_ex.side_effect = lambda x: 0 if x[1] == 80 else 1
    mock_socket.return_value = mock_sock_instance
    
    result = scan_ports.func("example.com", [80, 443])
    assert result == "80"
    
@patch('domain_scanner.tools.domain_tools.socket.socket')
def test_scan_ports_none(mock_socket):
    mock_sock_instance = MagicMock()
    # Mock connect_ex to return 1 (fail) for all
    mock_sock_instance.connect_ex.return_value = 1
    mock_socket.return_value = mock_sock_instance
    
    result = scan_ports.func("example.com", [80, 443])
    assert result == "No open ports discovered"

# --- crawl_website ---
@patch('domain_scanner.tools.domain_tools.ThreadPoolExecutor')
def test_crawl_website(mock_executor, mock_requests_get):
    mock_response = MagicMock()
    mock_response.text = '<a href="/about">About</a><a href="https://external.com">External</a>'
    mock_requests_get.return_value = mock_response
    
    # Mocking ThreadPoolExecutor map
    mock_ex_instance = MagicMock()
    mock_ex_instance.__enter__.return_value = mock_ex_instance
    mock_ex_instance.map.return_value = ["mock_page"] 
    mock_executor.return_value = mock_ex_instance
    
    result = crawl_website.func("example.com")
    assert "https://example.com/about" in result
    assert "Pages fetched:\n            1" in result # because mock map returns 1 item
    assert "external.com" not in result

