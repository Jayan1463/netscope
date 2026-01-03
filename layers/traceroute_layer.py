import subprocess
import re

def traceroute_host(host, max_hops=15):
    try:
        process = subprocess.run(
            ["traceroute", "-m", str(max_hops), host],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if process.returncode != 0:
            raise Exception(process.stderr)

        hops = []

        for line in process.stdout.splitlines():
            match = re.match(r"\s*(\d+)\s+(.+?)\s+\(([\d\.]+)\)\s+([\d\.]+)\s+ms", line)
            if match:
                hop_num = int(match.group(1))
                host_name = match.group(2)
                ip = match.group(3)
                latency = float(match.group(4))

                hops.append({
                    "hop": hop_num,
                    "host": host_name,
                    "ip": ip,
                    "latency": latency
                })

        return {
            "status": "ok",
            "hops": hops
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }
