import plotly.graph_objects as go


# ======================================================
# DNS — Latency Gauge Bar
# ======================================================
def latency_bar(title: str, latency_ms: float):
    """
    Clean, semantic latency bar (observability style).
    """

    if latency_ms < 100:
        color = "#2ecc71"   # green
    elif latency_ms < 300:
        color = "#f1c40f"   # yellow
    else:
        color = "#e74c3c"   # red

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=[latency_ms],
            y=["DNS Resolution"],
            orientation="h",
            marker=dict(color=color),
            text=[f"{latency_ms:.2f} ms"],
            textposition="inside",
            insidetextanchor="middle",
        )
    )

    fig.update_layout(
        title=dict(text=title, x=0.02, font=dict(size=18)),
        xaxis=dict(
            title="Milliseconds",
            showgrid=False,
            zeroline=False,
        ),
        yaxis=dict(showticklabels=False),
        height=180,
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e6e6e6"),
    )

    return fig


# ======================================================
# IP — Ping Sparkline
# ======================================================
def ping_line(latencies):
    """
    Sparkline-style ping latency over packets.
    """
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            y=latencies,
            mode="lines+markers",
            line=dict(color="#58a6ff", width=2),
            marker=dict(size=6),
            name="Ping Latency",
        )
    )

    fig.update_layout(
        title="Ping Latency Over Time",
        xaxis_title="Packet Index",
        yaxis_title="Milliseconds",
        height=260,
        margin=dict(l=40, r=20, t=50, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e6e6e6"),
    )

    return fig


# ======================================================
# Traceroute — Hop Latency Curve
# ======================================================
def traceroute_chart(hops):
    """
    Hop-by-hop traceroute latency curve.
    """
    x = [hop["hop"] for hop in hops]
    y = [hop["latency"] for hop in hops]
    labels = [f'{hop["host"]} ({hop["ip"]})' for hop in hops]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="lines+markers",
            line=dict(color="#f78166", width=2),
            marker=dict(size=8),
            text=labels,
            hovertemplate="%{text}<br>Latency: %{y} ms",
            name="Hop Latency",
        )
    )

    fig.update_layout(
        title="Traceroute — Hop-by-Hop Latency",
        xaxis_title="Hop Number",
        yaxis_title="Latency (ms)",
        height=320,
        margin=dict(l=50, r=20, t=50, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e6e6e6"),
    )

    return fig


# ======================================================
# TCP — Handshake Timeline
# ======================================================
def tcp_handshake_timeline(connect_time_ms: float):
    """
    Visual timeline of TCP three-way handshake.
    """
    steps = ["SYN", "SYN-ACK", "ACK"]
    times = [0, connect_time_ms * 0.6, connect_time_ms]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=times,
            y=steps,
            mode="lines+markers",
            line=dict(color="#a371f7", width=3),
            marker=dict(size=10),
            name="TCP Handshake",
        )
    )

    fig.update_layout(
        title="TCP Three-Way Handshake Timeline",
        xaxis_title="Time (ms)",
        yaxis_title="Step",
        height=260,
        margin=dict(l=50, r=20, t=50, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e6e6e6"),
    )

    return fig


# ======================================================
# TLS — Status Card
# ======================================================
def tls_status_card(expired: bool):
    """
    TLS certificate validity indicator.
    """
    status = "EXPIRED" if expired else "VALID"
    color = "#e74c3c" if expired else "#2ecc71"

    fig = go.Figure(
        go.Indicator(
            mode="number",
            value=1,
            title={"text": f"TLS Certificate: {status}"},
            number={"font": {"color": color, "size": 48}},
        )
    )

    fig.update_layout(
        height=180,
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e6e6e6"),
    )

    return fig


# ======================================================
# HTTP — Waterfall Breakdown
# ======================================================
def http_waterfall_chart(timings: dict):
    """
    Horizontal waterfall of HTTP request phases.
    """
    phases = list(timings.keys())
    values = list(timings.values())

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=values,
            y=phases,
            orientation="h",
            marker=dict(color="#79c0ff"),
            text=[f"{v:.1f} ms" for v in values],
            textposition="inside",
        )
    )

    fig.update_layout(
        title="HTTP Request Waterfall",
        xaxis_title="Milliseconds",
        yaxis_title="Phase",
        height=320,
        margin=dict(l=120, r=20, t=50, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e6e6e6"),
    )

    return fig


# ======================================================
# QUIC vs TCP — Comparison
# ======================================================
def quic_vs_tcp_chart(tcp_time_ms: float, quic_time_ms: float):
    """
    Side-by-side protocol comparison.
    """
    protocols = ["TCP (HTTP/1.1)", "QUIC (HTTP/3)"]
    values = [tcp_time_ms, quic_time_ms]
    colors = ["#f78166", "#2ecc71"]

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=protocols,
            y=values,
            marker=dict(color=colors),
            text=[f"{v:.1f} ms" for v in values],
            textposition="auto",
        )
    )

    fig.update_layout(
        title="QUIC vs TCP — Total Request Time",
        yaxis_title="Milliseconds",
        height=300,
        margin=dict(l=40, r=20, t=50, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e6e6e6"),
    )

    return fig

def request_time_breakdown(timings: dict):
    """
    Stacked bar showing where time was spent across layers.
    timings example:
    {
        "DNS": 120,
        "TCP": 40,
        "TLS": 60,
        "HTTP": 280
    }
    """
    labels = list(timings.keys())
    values = list(timings.values())

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=values,
            y=["Total Request Time"],
            orientation="h",
            marker=dict(
                color=["#2ecc71", "#a371f7", "#f1c40f", "#79c0ff"]
            ),
            text=[f"{v:.0f} ms" for v in values],
            textposition="inside"
        )
    )

    fig.update_layout(
        title="Where Time Was Spent (End-to-End)",
        xaxis_title="Milliseconds",
        yaxis=dict(showticklabels=False),
        height=220,
        margin=dict(l=40, r=20, t=50, b=30),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e6e6e6")
    )

    return fig
