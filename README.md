# 🌐 NetScope — Internet Observability Platform

**NetScope** is a cloud-native Internet observability tool that explains how real network requests traverse the Internet stack — **layer by layer** — from DNS resolution to application-level protocols.

Unlike traditional tools that treat the network as a black box, NetScope focuses on **explainability, systems behavior, and real-world cloud constraints**.

🔗 **Live Demo:** [https://netscope-0ev2.onrender.com](https://netscope-0ev2.onrender.com)

---

## 🚀 Why NetScope?

Most networking tools assume:

* ICMP (ping) is always available ❌
* Local machine privileges exist ❌
* Cloud environments behave like desktops ❌

NetScope was built **from first principles** to work in **real cloud environments**, where:

* ICMP is blocked
* Traceroute is restricted
* Raw sockets are unavailable

Instead of forcing these tools, NetScope redesigns reachability and latency measurement using **production-safe techniques** like TCP socket timing.

---

## 🧠 What NetScope Does

NetScope analyzes a request across the Internet stack:

### 🌐 DNS

* Domain resolution
* Resolver latency
* Cache inference (TTL behavior)

### 🔌 IP / Reachability (Cloud-Safe)

* TCP-based reachability (no ICMP)
* Connection latency measurement
* Packet-loss approximation

### 🛰️ Traceroute (Best-Effort)

* Hop-by-hop path visualization
* Graceful degradation when blocked

### 🔗 TCP

* Three-way handshake timing
* Connection establishment latency

### 🔐 TLS

* Certificate inspection
* Expiry and validation status

### 📄 HTTP

* Request/response timing breakdown
* Waterfall visualization

### ⚡ QUIC vs TCP

* HTTP/3 (QUIC) vs HTTP/1.1 performance comparison
* Automatic fallback if QUIC is unsupported

---

## 🧪 Failure Simulation (Educational Focus)

NetScope can **simulate failures** to demonstrate how systems degrade:

* Artificial DNS latency
* TCP connection delays
* HTTP request failures

This makes NetScope useful not just for observation, but for **systems learning and reliability thinking**.

---

## 🛠️ Tech Stack

* **Python**
* **Streamlit** (UI & orchestration)
* **Plotly** (visualizations)
* **Socket Programming**
* **TLS / SSL**
* **HTTP / QUIC**
* **Cloud Deployment (Render)**

---

## 🏗️ Architecture Overview

```
app.py
├── layers/
│   ├── dns_layer.py
│   ├── ip_layer.py        # TCP-based reachability
│   ├── traceroute_layer.py
│   ├── tcp_layer.py
│   ├── tls_layer.py
│   ├── http_layer.py
│   └── quic_layer.py
├── visuals/
│   └── charts.py
├── reports/
│   └── report_builder.py
```

Each layer:

* Executes independently
* Fails gracefully
* Explains *why* something worked or failed

---

## ☁️ Cloud-Native Design Decisions

* ❌ No ICMP dependency (ping blocked in cloud)
* ✅ TCP socket timing used instead
* ❌ No privileged system calls
* ✅ Fully deployable on managed platforms
* ✅ Safe for production environments

---

## 📦 Local Setup (Optional)

```bash
git clone https://github.com/Jayan1463/netscope.git
cd netscope
pip install -r requirements.txt
streamlit run app.py
```

---

## 🎯 Learning Outcomes

This project demonstrates:

* Systems-level thinking
* Real-world networking behavior
* Cloud deployment constraints
* Observability and reliability design
* Debugging across network layers

---

## 👤 Author

**Jayan**
B.E Computer Science Engineering
Focus: Systems, Networking, Cloud, Observability

---

## 📜 License

This project is for educational and demonstration purposes.

