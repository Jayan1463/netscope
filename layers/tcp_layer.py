import socket
import time


def tcp_handshake(host: str, port: int = 80, timeout: float = 3.0):
    """
    Measure TCP connection setup time.

    Returns:
        {
            status: "ok" | "error",
            connect_time_ms: float
        }
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)

        start = time.time()
        sock.connect((host, port))
        end = time.time()

        sock.close()

        return {
            "status": "ok",
            "connect_time_ms": (end - start) * 1000
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }
