import subprocess
import re


def ping_host(host: str, count: int = 5):
    """
    Ping a host and measure latency & packet loss.

    Returns:
        {
            status: "ok" | "error",
            latencies: [float],
            loss: int
        }
    """
    try:
        process = subprocess.run(
            ["ping", "-c", str(count), host],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if process.returncode != 0:
            raise Exception(process.stderr.strip())

        # Extract latency values (ms)
        latencies = [
            float(t)
            for t in re.findall(r"time=([\d.]+)", process.stdout)
        ]

        # Extract packet loss
        loss_match = re.search(r"(\d+)% packet loss", process.stdout)
        loss = int(loss_match.group(1)) if loss_match else 0

        return {
            "status": "ok",
            "latencies": latencies,
            "loss": loss
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }
