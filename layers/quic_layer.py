import subprocess
import time


def quic_request(domain: str):
    """
    Measure HTTP/3 (QUIC) request time using curl.
    """

    # Check if curl supports HTTP/3
    version = subprocess.run(
        ["curl", "-V"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if "HTTP3" not in version.stdout:
        return {
            "status": "unsupported",
            "reason": "curl built without HTTP/3 support"
        }

    try:
        start = time.time()

        process = subprocess.run(
            [
                "curl",
                "--http3",
                "-s",
                "-o",
                "/dev/null",
                "-w",
                "%{http_code}",
                f"https://{domain}"
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10
        )

        total_time = (time.time() - start) * 1000

        if process.returncode != 0:
            raise Exception(process.stderr.strip())

        return {
            "status": "ok",
            "http_code": process.stdout.strip(),
            "total_time_ms": total_time
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }
