# Gravotech Python (Unofficial)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-green?logo=github)

**Version: 1.0.0**

---

## Description

Gravotech Python (Unofficial) is a Python package designed to communicate with Gravotech engraving machines using the TL07 protocol.

The goal of this library is to simplify integration, standardize exchanges, and automate communication with Gravotech machines, while hiding the complexity of low-level TCP/IP protocols.

This project is not affiliated with Gravotech and is provided as a community-driven, open-source solution.

---

## Who is this package for?

This package is intended for:

* Industrial software developers

* Automation engineers

* Manufacturing / methods engineering teams

Anyone who needs to integrate a Gravotech engraving machine into a larger software or industrial system (MES, ERP, production line, automation cell, etc.).

---

## Problems this package solves

Before using this package, Gravotech integrations often suffer from:

* Low-level TCP/IP exchanges that are difficult to manage

* Very limited abstraction over the TL07 protocol

* Custom, machine-specific scripts

* Code that is hard to read, hard to test, and hard to maintain

* Tight coupling between business logic and communication logic

This package provides:

* A clean, high-level Python API

* Thread-safe communication

* A clear separation between transport, commands, and business logic

* Testable and maintainable code

* A reusable foundation for industrial projects

---

## Installation

Install the package directly from PyPI:

```bash
    pip install gravotech-tl07
```

## Quick example

```python
from gravotech.client import Gravotech
from gravotech.actions.actions import LDMode

with Gravotech("192.168.0.211", 55555) as gravotech:
    # Load a marking file
    gravotech.Actions.ld("example.t2l", 1, LDMode.NORMAL)

    # Check machine status
    status = gravotech.Actions.st()
    print("Machine status:", status)

    # Start marking
    result = gravotech.Actions.go()
    print("Marking result:", result)
```

## Concrete use cases

### 1. Automated production line
* Integrate a Gravotech engraver into an automated production line to:

* Load marking files dynamically

* Set serial numbers or batch information using variables

* Trigger marking cycles programmatically

* Monitor machine state and errors

### 2. MES / ERP integration

* Use this package to connect a Gravotech machine to a Manufacturing Execution System:

* Automatic file selection based on production orders

* Traceability through engraved serial numbers

* Centralized error handling and monitoring

### 3. R&D and prototyping

* Quickly prototype engraving workflows:

* Simulate marking sequences

* Test TL07 commands without manual interaction

* Build proof-of-concept integrations

### 4. Maintenance and tooling

* Create internal tools to:

* List, upload, or delete files on the machine

* Diagnose machine status remotely

* Standardize engraving procedures across sites

## Project status

### Active development

* Core TL07 commands implemented

* Thread-safe TCP/IP communication

* Unit-tested architecture

* Continuous Integration in place

### Future improvements may include:

* Extended error handling

* Higher-level workflows

* Async support

* Additional documentation and examples

## Support & Contact

This project is provided as-is, without official support from Gravotech.

However:

* Bug reports and feature requests are welcome via GitHub Issues

* Contributions (PRs, tests, documentation) are encouraged

* The codebase is designed to be readable, testable, and extensible

If you need custom integration, industrial support, or project-specific adaptations, you are encouraged to fork the project or build on top of it

## Disclaimer

This is an unofficial project.
Gravotech®, TL07®, and related trademarks are the property of their respective owners.