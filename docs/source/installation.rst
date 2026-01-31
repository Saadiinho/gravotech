Installation
============

This section explains how to install and configure the **Gravotech Python (Unofficial)** package.

---

📦 **Install from PyPI**
------------------------

The recommended way to install the package is via pip:

.. code-block:: bash

   pip install gravotech-tl07

To verify that the installation was successful, you can run:

.. code-block:: bash

   python -c "import gravotech; print('Gravotech installed successfully')"

---

🐍 **Python Requirements**
--------------------------

This package requires:

- Python **3.8 or newer**
- pip 21+ (recommended)

You can check your Python version with:

.. code-block:: bash

   python --version

---

🛠️ **Install for Development**
-------------------------------

If you want to contribute to the project or modify the code, you can clone the repository
and install it in editable mode:

.. code-block:: bash

   git clone https://github.com/your-org/gravotech-tl07.git
   cd gravotech-tl07
   pip install -e .

If you are using **Poetry**, you can instead run:

.. code-block:: bash

   poetry install

---

🐳 **Docker (Optional)**
------------------------

If your project runs inside Docker, you can add the package to your `requirements.txt`:

.. code-block:: text

   gravotech-tl07

Or install it directly in your Dockerfile:

.. code-block:: dockerfile

   RUN pip install gravotech-tl07

---

⚠️ **Network Requirements**
---------------------------

Ensure that:

- Your Gravotech machine is reachable on the network.
- The correct IP address and port are used (default Gravotech port is usually **55555**).
- No firewall is blocking the connection.

---

🧪 **Testing the Installation**
--------------------------------

You can test a basic connection like this:

.. code-block:: python

   from gravotech.client import Gravotech

   gravotech = Gravotech("192.168.0.211", 55555)
   gravotech.connect()
   print("Connected successfully!")
   gravotech.Streamer.close()
