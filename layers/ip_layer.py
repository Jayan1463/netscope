import socket
import time


def tcp_latency(host: str, port: int = 443, timeout: float = 3.0):
    """
    Measure TCP reachability and latency using a socket connection.
    Cloud-safe replacement for ping.

    Returns:
        {
            status: "reachable" | "unreachable",
            latency_ms: float,
            method: "tcp_connect",
            port: int
        }
    """
    start = time.time()
    try:
        sock = socket.create_connection((host, port), timeout=timeout)
        sock.close()
        latency_ms = round((time.time() - start) * 1000, 2)

        return {
            "status": "reachable",
            "latency_ms": latency_ms,
            "method": "tcp_connect",
            "port": port
        }

    except Exception as e:
        return {
            "status": "unreachable",
            "error": str(e),
            "method": "tcp_connect",
            "port": port
        }
