# Gravotech API

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-green?logo=github)

**Version: 1.0.0**

---

## 📌 Overview

This project provides a simple and reliable way to communicate with **Gravotech laser engraving machines** from your code.  
It solves the common challenge of integrating industrial engraving equipment into software workflows by offering a clean, thread-safe interface over TCP/IP — with an optional REST API layer for easy integration.

Designed for **any user or developer working with a Gravotech engraver**, this tool bridges the gap between your application logic and the machine’s native M-Command protocol.

---

## ✨ Features

- 🔌 **TCP/IP communication** with Gravotech engravers (port `55555`)
- 🧵 **Thread-safe** socket handling for concurrent use
- 🌐 **RESTful API** to send commands and monitor status via HTTP
- 🛠️ Support for core M-Commands (`ST`, `LD`, `GO`, `LS`, etc.)
- 🐳 Fully **Dockerized** for easy deployment and isolation
- 🧪 Built-in simulation mode for development (no physical machine required)

---

## ⚙️ Prerequisites

Before using this API, ensure you have:

- A **Gravotech laser engraver** connected to your network
- Your computer and the engraver on the **same local network**
- **Docker** and **Docker Compose** installed and accessible
- Network access to the engraver’s IP address (default port: `55555`)

---

## 🚀 Installation & Usage

### 1. Configure your environment

Create a `.env` file at the root of the project:

```env
GRAVOTECH_IP=192.168.1.100
GRAVOTECH_PORT=55555
API_HOST=0.0.0.0
API_PORT=8000
```
Replace GRAVOTECH_IP with your actual engraver's IP address.

### 2. Build the Docker image
```bash
  make build-api
```

### 3. Run the API
```bash
  make run-api
```
The REST API will be available at http://127.0.0.1:3001.

💡 Tip: During development, you can use the built-in fake Gravotech server to test without a physical machine.
```bash
    make build-server
    make run-server
```

## 📬 Support & Contact

This project is maintained by a single developer.
If you have questions, encounter issues, or need assistance, please contact me by email.

    📩 Maintainer: Saad RAFIQUL
    ✉️ Email: saad.rafiqul1@gmail.com

## 📄 License

Proprietary – All rights reserved.
For internal or authorized use only.

