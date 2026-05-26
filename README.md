# ISS Proximity Tracker & DevOps Pipeline

[![CI/CD Build and Test Pipeline](https://github.com/LiamBaker42/Devops-Space-Api/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/LiamBaker42/Devops-Space-Api/actions/workflows/ci-cd.yml)

A containerized microservice that tracks the live location of the International Space Station (ISS) in real-time and calculates its geodesic distance from any given UK postcode, served via a clean web interface.

The core objective of this project was to implement a professional, production-ready **GitOps CI/CD pipeline** utilizing modern cloud-engineering practices.

---

## Tech Stack & Architecture

* **Backend Framework:** FastAPI (Python 3.11) - Selected for native asynchronous support and automated OpenAPI documentation.
* **Frontend:** HTML5 / CSS3 via Jinja2 templates for real-time server-side rendering.
* **Containerization:** Docker (Python-slim base image optimized for low resource overhead).
* **CI/CD Automation:** GitHub Actions (Automated unit testing & build verification).
* **Third-Party APIs:** Open-Notify ISS API & Postcodes.io API.

### Technical Architecture Workflow
1. **Developer Push:** Code is pushed to GitHub.
2. **Continuous Integration (GitHub Actions):** A temporary Linux virtual machine spins up, installs dependencies, and executes `pytest` unit tests.
3. **Container Verification:** The workflow executes a mock Docker build step to ensure the environment configuration remains unbroken.

---

## How to Run the App Locally (Using Docker)

To run this application without needing Python installed on your local host system, ensure you have **Docker Desktop** running and execute the following commands in your terminal:

```bash
# 1. Clone the repository
git clone [https://github.com/YOUR_USERNAME/devops-space-api.git](https://github.com/YOUR_USERNAME/devops-space-api.git)
cd devops-space-api

# 2. Build the container image
docker build -t iss-tracker-image .

# 3. Spin up the containerized application
docker run -d -p 8000:8000 --name iss-tracker-container iss-tracker-image
