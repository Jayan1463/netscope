import ssl
import socket
import datetime


def inspect_tls(domain: str, port: int = 443, timeout: float = 3.0):
    """
    Inspect TLS certificate of a server.

    Returns:
        {
            status: "ok" | "error",
            subject: str,
            issuer: str,
            not_before: str,
            not_after: str,
            expired: bool
        }
    """
    try:
        context = ssl.create_default_context()

        with socket.create_connection((domain, port), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()

        not_before = datetime.datetime.strptime(
            cert["notBefore"], "%b %d %H:%M:%S %Y %Z"
        )
        not_after = datetime.datetime.strptime(
            cert["notAfter"], "%b %d %H:%M:%S %Y %Z"
        )

        now = datetime.datetime.utcnow()

        subject = dict(x[0] for x in cert["subject"])
        issuer = dict(x[0] for x in cert["issuer"])

        return {
            "status": "ok",
            "subject": subject.get("commonName", "Unknown"),
            "issuer": issuer.get("commonName", "Unknown"),
            "not_before": not_before.strftime("%Y-%m-%d"),
            "not_after": not_after.strftime("%Y-%m-%d"),
            "expired": now > not_after
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }
