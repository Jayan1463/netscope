import socket
import ssl
import time


def http_request(domain: str, path: str = "/", port: int = 443):
    """
    Perform a raw HTTPS GET request and measure timings.
    """

    timings = {}
    start_total = time.time()

    # DNS
    start = time.time()
    ip = socket.gethostbyname(domain)
    timings["dns"] = (time.time() - start) * 1000

    # TCP
    start = time.time()
    sock = socket.create_connection((ip, port))
    timings["tcp"] = (time.time() - start) * 1000

    # TLS
    context = ssl.create_default_context()
    start = time.time()
    ssock = context.wrap_socket(sock, server_hostname=domain)
    timings["tls"] = (time.time() - start) * 1000

    # HTTP Request
    request = f"GET {path} HTTP/1.1\r\nHost: {domain}\r\nConnection: close\r\n\r\n"
    start = time.time()
    ssock.sendall(request.encode())
    timings["request"] = (time.time() - start) * 1000

    # HTTP Response
    start = time.time()
    response = ssock.recv(4096)
    timings["response"] = (time.time() - start) * 1000

    ssock.close()

    timings["total"] = (time.time() - start_total) * 1000

    status_line = response.decode(errors="ignore").splitlines()[0]

    return {
        "status": "ok",
        "ip": ip,
        "status_line": status_line,
        "timings": timings
    }
