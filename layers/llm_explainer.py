import subprocess
import json

def explain_with_llm(report_data: dict):
    prompt = f"""
You are a senior distributed systems engineer.

Explain the following diagnostics:
1. What was slow or failed
2. Why it happened
3. What to check next

Diagnostics:
{json.dumps(report_data, indent=2)}

Be concise and technical.
"""

    try:
        result = subprocess.run(
            ["ollama", "run", "llama3"],
            input=prompt.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30
        )

        if result.returncode != 0:
            raise RuntimeError(result.stderr.decode())

        return {
            "status": "ok",
            "text": result.stdout.decode()
        }

    except Exception:
        return {
            "status": "fallback",
            "text": fallback_explanation(report_data)
        }

def fallback_explanation(report_data):
    notes = []

    if "dns" in report_data:
        if report_data["dns"]["cache"]["status"] == "cache_miss":
            notes.append("DNS was slow due to a cache miss (recursive lookup).")

    if "tcp" in report_data and report_data["tcp"]["connect_time_ms"] > 150:
        notes.append("TCP handshake latency suggests network delay.")

    if "http" in report_data and report_data["http"]["timings"]["total"] > 300:
        notes.append("HTTP dominated total latency (backend slowness).")

    return "\n".join(f"- {n}" for n in notes) or "No major issues detected."
