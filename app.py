import json
import streamlit as st

# ===================== Imports =====================
from layers.dns_layer import resolve_dns
from layers.ip_layer import tcp_latency
from layers.traceroute_layer import traceroute_host
from layers.tcp_layer import tcp_handshake
from layers.tls_layer import inspect_tls
from layers.http_layer import http_request
from layers.quic_layer import quic_request
from layers.llm_explainer import explain_with_llm
from reports.report_builder import build_report

from visuals.charts import (
    latency_bar,
    traceroute_chart,
    tcp_handshake_timeline,
    tls_status_card,
    http_waterfall_chart,
    quic_vs_tcp_chart,
    request_time_breakdown
)

# ===================== Page Config =====================
st.set_page_config(page_title="NetScope", layout="wide")

def show(fig):
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ===================== Progress Helpers =====================
def init_progress(total_steps):
    bar = st.progress(0)
    label = st.empty()
    return bar, label, total_steps, 0

def advance(bar, label, step, total, text):
    percent = int((step / total) * 100)
    bar.progress(percent)
    label.markdown(f"⏳ **{text}**")

# ===================== Header =====================
st.title("🌐 NetScope — Internet Observatory")
st.caption("Observe • Break • Explain (smooth, progressive execution)")

# ===================== Sidebar =====================
with st.sidebar:
    st.header("Layers")
    enable_dns = st.checkbox("DNS", True)
    enable_ip = st.checkbox("IP / Reachability (TCP)", True)
    enable_trace = st.checkbox("Traceroute", True)
    enable_tcp = st.checkbox("TCP", True)
    enable_tls = st.checkbox("TLS", True)
    enable_http = st.checkbox("HTTP", True)
    enable_quic = st.checkbox("QUIC", True)

    st.divider()
    st.header("Failure Simulation (Non-blocking)")
    slow_dns = st.checkbox("Simulate Slow DNS")
    slow_tcp = st.checkbox("Simulate Slow TCP")
    fail_http = st.checkbox("Simulate HTTP Failure")
    delay_ms = st.slider("Injected latency (ms)", 100, 2000, 800, 100)

# ===================== Input =====================
domain = st.text_input("Domain", "google.com")
run = st.button("Run Analysis", type="primary")

# ===================== Execution =====================
if run:
    report_data = {}
    summary = {}

    enabled_layers = sum([
        enable_dns,
        enable_ip,
        enable_trace,
        enable_tcp,
        enable_tls,
        enable_http,
        enable_quic
    ])

    progress_bar, progress_label, total, step = init_progress(enabled_layers)

    # ---------------- DNS ----------------
    if enable_dns:
        step += 1
        advance(progress_bar, progress_label, step, total, "Resolving DNS")

        st.subheader("🧭 DNS")
        with st.spinner("Resolving DNS..."):
            dns = resolve_dns(domain)

        if dns["status"] == "ok":
            if slow_dns:
                dns["latency"] += delay_ms
                dns["simulated"] = "slow_dns"

            report_data["dns"] = dns
            summary["DNS"] = dns["latency"]

            show(latency_bar("DNS Resolution", dns["latency"]))

            cache = dns.get("cache")
            if cache:
                st.info(f"Cache: {cache.get('status')} — {cache.get('reason')}")
            else:
                st.info("Cache: not inferred")
        else:
            st.error(dns["error"])

    # ---------------- IP (TCP Reachability) ----------------
    if enable_ip:
        step += 1
        advance(progress_bar, progress_label, step, total, "Measuring TCP reachability")

        st.subheader("📡 IP / Reachability (TCP)")
        with st.spinner("Checking TCP connectivity..."):
            ip = tcp_latency(domain)

        if ip["status"] == "reachable":
            report_data["ip"] = ip
            summary["IP"] = ip["latency_ms"]

            show(latency_bar(
                "TCP Reachability (Port 443)",
                ip["latency_ms"]
            ))

            st.info(
                f"Method: {ip['method']} • "
                f"Port: {ip['port']} • "
                f"Latency: {ip['latency_ms']} ms"
            )
        else:
            st.error(ip.get("error", "Host unreachable"))

    # ---------------- Traceroute ----------------
    if enable_trace:
        step += 1
        advance(progress_bar, progress_label, step, total, "Tracing network path")

        st.subheader("🛰️ Traceroute")
        with st.spinner("Tracing network path..."):
            trace = traceroute_host(domain)

        if trace["status"] == "ok":
            report_data["traceroute"] = trace
            show(traceroute_chart(trace["hops"]))
        else:
            st.warning("Traceroute blocked or incomplete (expected in cloud environments)")

    # ---------------- TCP ----------------
    if enable_tcp:
        step += 1
        advance(progress_bar, progress_label, step, total, "Establishing TCP connection")

        st.subheader("🔗 TCP")
        with st.spinner("Establishing TCP connection..."):
            tcp = tcp_handshake(domain, 80)

        if tcp["status"] == "ok":
            if slow_tcp:
                tcp["connect_time_ms"] += delay_ms
                tcp["simulated"] = "slow_tcp"

            report_data["tcp"] = tcp
            summary["TCP"] = tcp["connect_time_ms"]
            show(tcp_handshake_timeline(tcp["connect_time_ms"]))
        else:
            st.error(tcp["error"])

    # ---------------- TLS ----------------
    if enable_tls:
        step += 1
        advance(progress_bar, progress_label, step, total, "Inspecting TLS certificate")

        st.subheader("🔐 TLS")
        with st.spinner("Inspecting TLS certificate..."):
            tls = inspect_tls(domain)

        if tls["status"] == "ok":
            report_data["tls"] = tls
            show(tls_status_card(tls["expired"]))
        else:
            st.error(tls["error"])

    # ---------------- HTTP ----------------
    if enable_http:
        step += 1
        advance(progress_bar, progress_label, step, total, "Performing HTTP request")

        st.subheader("📄 HTTP")
        with st.spinner("Performing HTTP request..."):
            if fail_http:
                http = {"status": "failed"}
            else:
                http = http_request(domain)

        if http["status"] == "ok":
            report_data["http"] = http
            summary["HTTP"] = http["timings"]["total"]
            show(http_waterfall_chart(http["timings"]))
        else:
            st.error("HTTP request failed (simulated or real)")

    # ---------------- QUIC ----------------
    if enable_quic:
        step += 1
        advance(progress_bar, progress_label, step, total, "Testing QUIC / HTTP/3")

        st.subheader("⚡ QUIC vs TCP")
        with st.spinner("Attempting QUIC (HTTP/3)..."):
            quic = quic_request(domain)

        report_data["quic"] = quic

        if quic["status"] == "ok" and "http" in report_data:
            show(quic_vs_tcp_chart(
                report_data["http"]["timings"]["total"],
                quic["total_time_ms"]
            ))
        elif quic["status"] == "unsupported":
            st.info("QUIC unsupported (curl without HTTP/3)")
        else:
            st.warning("QUIC blocked or unavailable")

    # ---------------- COMPLETE ----------------
    progress_bar.progress(100)
    progress_label.markdown("✅ **Analysis complete**")

    # ---------------- SUMMARY ----------------
    if summary:
        st.divider()
        st.subheader("🧠 Request Summary")
        show(request_time_breakdown(summary))
        st.metric("Total Time", f"{sum(summary.values()):.0f} ms")

    # ---------------- LLM ----------------
    st.divider()
    st.subheader("🤖 AI Explanation")
    with st.spinner("Analyzing system behavior..."):
        explanation = explain_with_llm(report_data)
    st.markdown(explanation["text"])

    # ---------------- EXPORT ----------------
    st.divider()
    report = build_report(domain, report_data)
    st.download_button(
        "Download Report",
        json.dumps(report, indent=2),
        f"netscope_{domain}.json",
        "application/json"
    )

st.markdown("---\n🧠 **Professional observability UX achieved.**")
