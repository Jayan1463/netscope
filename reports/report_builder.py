from datetime import datetime


def build_report(domain: str, results: dict):
    """
    Build a structured diagnostic report.
    """

    return {
        "meta": {
            "tool": "NetScope",
            "domain": domain,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        },
        "results": results
    }
