Gravotech Python (Unofficial)
=============================

Gravotech Python is an unofficial, open-source Python library that enables communication
with Gravotech engraving machines using the TL07 protocol over TCP/IP.

This package provides a high-level, Pythonic interface for interacting with Gravotech
machines, abstracting away low-level socket communication while preserving access to
core TL07 commands when needed.

It is designed for industrial environments where reliability, testability, and maintainability
are essential.

.. note::

   This project is not affiliated with, endorsed by, or supported by Gravotech.
   Gravotech®, TL07®, and related trademarks remain the property of their respective owners.

---

🚀 **Project Goals**
--------------------

This library aims to:

- Simplify integration with Gravotech TL07-based machines
- Provide a clean, high-level Python API for machine control
- Encapsulate low-level TCP/IP communication details
- Offer thread-safe communication mechanisms
- Enable automated engraving workflows
- Improve testability and maintainability of industrial codebases

---

🎯 **Who is this for?**
-----------------------

This package is primarily intended for:

- Industrial software developers
- Automation engineers
- Manufacturing and methods engineering teams
- System integrators working with MES/ERP systems
- R&D teams prototyping engraving workflows

---

🔧 **What problems does this solve?**
-------------------------------------

Traditional Gravotech integrations often suffer from:

- Complex, low-level TCP/IP communication
- Limited abstraction over the TL07 protocol
- Machine-specific, hard-to-maintain scripts
- Tight coupling between business logic and machine control
- Lack of automated testing

This library addresses these issues by providing:

- A structured, object-oriented interface
- Clear separation between transport and business logic
- Built-in thread safety
- A test-friendly architecture
- A reusable foundation for industrial projects

---

📦 **Getting Started**
----------------------

If you are new to this library, we recommend following this reading path:

1. **Installation** — Install the package and set up your environment.
2. **Usage Guide** — Learn the basic concepts and workflow.

---

📖 **Documentation**
--------------------

.. toctree::
   :maxdepth: 2
   :caption: Documentation

   installation
   usage

---

🧠 **Core Architecture**
------------------------

The library is structured around three main components:

- **Gravotech Client (`Gravotech`)**
  - Main entry point for users
  - Manages connection lifecycle
  - Provides access to all actions

- **IPStreamer**
  - Handles low-level TCP/IP communication
  - Ensures thread-safe messaging
  - Implements automatic retries and timeouts

- **GraveuseAction**
    - High-level interface for TL07 commands
    - Encapsulates machine instructions such as:
        - Loading files (`LD`)
        - Starting marking (`GO`)
        - Reading machine status (`ST`)
        - Managing files (`LS`, `RM`, `PF`)
        - Handling variables (`VG`, `VS`)

---

🧪 **Quality & Testing**
------------------------

This project includes:

- Comprehensive unit tests using pytest
- Mock-based testing for hardware-independent validation
- Continuous Integration via GitHub Actions
- Code formatting enforced with Black
- Security analysis using Bandit

---

📈 **Project Status**
---------------------

**Active Development**

Current features include:

- Core TL07 command support
- Robust TCP/IP communication layer
- Thread-safe design
- Context manager support (`with Gravotech(...)`)
- Fully unit-tested architecture

Planned improvements:

- More advanced error handling
- Higher-level workflow abstractions
- Async support
- Expanded documentation and examples

---

📬 **Support & Contributions**
------------------------------

This project is community-driven.

You are encouraged to:

- Open issues for bugs or feature requests
- Submit pull requests with improvements
- Contribute tests, documentation, or examples

For custom industrial integrations, you may fork the project or extend it according
to your needs.

---

⚠️ **Disclaimer**
------------------

This is an unofficial project.
Gravotech®, TL07®, and related trademarks are the property of their respective owners.
