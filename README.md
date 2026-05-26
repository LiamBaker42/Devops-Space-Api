# 🛰️ ISS Live Reactive Tracker & DevOps Pipeline

[![CI/CD Build and Test Pipeline](https://github.com/LiamBaker42/Devops-Space-Api/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/LiamBaker42/Devops-Space-Api/actions/workflows/ci-cd.yml)

A fully responsive, containerized web application that tracks the live orbital path of the International Space Station (ISS) via asynchronous client-side polling, rendering real-time vector trails and calculating proximity adjustments from any targeted UK postcode.

The core objective of this project was to master **containerization (Docker)**, **automation pipeline engineering (CI/CD via GitHub Actions)**, and **responsive system integration**.

---

## 🛠️ Tech Stack & Architecture

* **Backend Engine:** FastAPI (Python 3.11) - Leveraged as an asynchronous network proxy to mitigate browser CORS and Mixed Content policies.
* **Frontend UI:** HTML5 / CSS3 Grid & Flexbox (Server-side rendering via Jinja2) engineered with fluid media queries for total cross-platform responsiveness (Mobile/Desktop).
* **Mapping Framework:** Leaflet.js - Utilizing client-side JavaScript to stream asynchronous `fetch` telemetry without full-page reloads.
* **Containerization:** Docker (Python-slim base image optimized for lightweight execution overhead).
* **CI/CD Automation:** GitHub Actions (Automated unit testing & environment build verification).

### 🔄 Architectural Pipeline & Proxy Workflow
1. **Developer Push:** Code changes trigger the GitHub Actions workflow runner.
2. **Continuous Integration (CI):** An ephemeral Linux virtual environment provisions, executes unit tests via `pytest`, and runs a container validation check.
3. **Secure API Proxying:** To defeat browser-level blocks on mixed HTTP/HTTPS requests, the browser queries the internal `/api/iss-now` endpoint. The FastAPI backend securely forwards this request to the upstream satellite stream and passes it back cleanly to the map layer.

---

## 🚀 How to Run the App Locally (Using Docker)

To run this application instantly without needing a local Python environment, ensure **Docker Desktop** is running and execute these commands in your terminal:

```bash
# 1. Clone the repository
git clone [https://github.com/LiamBaker42/Devops-Space-Api.git](https://github.com/LiamBaker42/Devops-Space-Api.git)
cd Devops-Space-Api

# 2. Build the decoupled container image
docker build -t iss-tracker-image .

# 3. Spin up the containerized web app mapped to local host port 8000
docker run -d -p 8000:8000 --name iss-tracker-container iss-tracker-image
