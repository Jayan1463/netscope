# 🌐 NetScope — Internet Observatory

**NetScope** is a systems-first Internet observability and experimentation tool that visualizes how the Internet actually works — layer by layer — from **DNS resolution** to **modern transport protocols like QUIC**.

Unlike typical networking tools or dashboards, NetScope is designed to **teach, observe, break, and explain** real Internet behavior using first-principles thinking.

---

## 🧠 Philosophy

> *“Don’t just use the Internet — observe it, stress it, and understand why it behaves the way it does.”*

NetScope focuses on:

* Systems thinking over surface-level metrics
* Explainability over raw data
* Real network behavior instead of mocks
* Learning through controlled failure

---

## ✨ Key Features

### 🔍 Layer-by-Layer Internet Visibility

* **DNS** — Name resolution latency and caching behavior
* **IP / Ping** — Reachability, packet latency trends
* **Traceroute** — Actual hop-by-hop routing paths
* **TCP** — Connection establishment timing
* **TLS** — Certificate trust and validity
* **HTTP** — End-to-end request waterfall
* **QUIC (HTTP/3)** — Modern protocol comparison vs TCP

---

### ⚙️ Failure Injection (Safe & Local)

Simulate real-world conditions without breaking your system:

* Slow DNS resolution
* Artificial TCP latency
* HTTP request failure simulation
* Observe cascading effects across layers

---

### 📊 Visual, Animated Observability

* Interactive Plotly charts
* Waterfall timelines
* Per-layer latency breakdowns
* Request-time attribution graph

---

### 🤖 AI-Assisted Explanation

NetScope can generate **human-readable explanations** of:

* Why a request was slow
* Which layer dominated latency
* How failures propagated
* What would improve performance

(Uses a local or pluggable LLM — no cloud lock-in.)

---

### 📦 Desktop App Support

* Packaged as a **macOS `.app`**
* No terminal required for end users
* Local execution only (privacy-safe)
* Optional `.dmg` installer

---

## 🧱 Architecture Overview

```
netscope/
│
├── app.py                # Main Streamlit application
├── launcher.py           # Desktop app launcher (PyInstaller)
│
├── layers/               # Internet layer implementations
│   ├── dns_layer.py
│   ├── ip_layer.py
│   ├── traceroute_layer.py
│   ├── tcp_layer.py
│   ├── tls_layer.py
│   ├── http_layer.py
│   ├── quic_layer.py
│   └── llm_explainer.py
│
├── visuals/
│   └── charts.py         # All Plotly visualizations
│
├── reports/
│   └── report_builder.py # JSON diagnostic export
│
└── README.md
```

Each layer is intentionally isolated to reinforce **clear responsibility boundaries**, mirroring real protocol stacks.

---

## 🚀 Getting Started (Development)

### 1️⃣ Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2️⃣ Install dependencies

```bash
pip install streamlit plotly requests dnspython
```

### 3️⃣ Run NetScope

```bash
streamlit run app.py
```

Open: `http://localhost:8501`

---

## 🖥️ Building macOS Desktop App

NetScope can be packaged as a native macOS app using **PyInstaller**.

### Build steps (stable method)

```bash
pip install pyinstaller
pyinstaller \
  --windowed \
  --name NetScope \
  --add-data "app.py:." \
  launcher.py
```

Output:

```
dist/NetScope.app
```

> ℹ️ Uses `onedir` mode for macOS stability.
> Streamlit hot-reload is intentionally disabled.

---

## 📤 Exporting Reports

NetScope can export a full diagnostic snapshot as JSON, including:

* Per-layer timing data
* Failure simulations applied
* Observed protocol behavior
* AI-generated explanation

Useful for:

* Case studies
* Debugging exercises
* Interview walkthroughs
* Teaching material

---

## 🎓 What This Project Demonstrates

This project showcases:

* Deep understanding of Internet protocols
* Systems-level reasoning
* Observability tooling design
* Failure modeling
* Clean modular architecture
* UI/UX for technical systems
* Desktop app packaging

It is **not** a CRUD app, dashboard clone, or framework demo.

---

## 🧩 Limitations (Intentional)

* QUIC availability depends on system HTTP/3 support
* TLS handshake timing is approximated
* No packet-level sniffing (focus is conceptual clarity)

These trade-offs are deliberate to keep the project **explainable and portable**.

---

## 🛣️ Future Extensions

* Packet-level simulation engine
* TCP retransmission visualization
* DNS cache poisoning scenarios
* Multi-request comparison mode
* Distributed system failure graphs

---

## 📜 License

This project is intended for **educational and research purposes**.
Local-only execution. No data collection.

---

## 🙌 Final Note

NetScope was built to answer one question:

> *“What is really happening when I type a URL and press Enter?”*

If you understand NetScope, you understand the Internet.

---

