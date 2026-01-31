Usage Guide
===========

This guide explains how to use the **Gravotech Python (Unofficial)** package in practice.



**Basic Connection**
--------------------

The main entry point of the library is the :class:`gravotech.client.Gravotech` class.

You can use it with a context manager:

.. code-block:: python

   from gravotech.client import Gravotech

   with Gravotech("192.168.0.211", 55555) as gravotech:
       print("Connected to Gravotech machine")

This automatically connects when entering the `with` block and closes the connection
when exiting it.

You can also manage the connection manually:

.. code-block:: python

   gravotech = Gravotech("192.168.0.211", 55555)
   gravotech.connect()

   # Do operations here

   gravotech.Streamer.close()



**Accessing Machine Actions**
-----------------------------

All high-level machine commands are available through:

.. code-block:: python

   gravotech.Actions

Example:

.. code-block:: python

   status = gravotech.Actions.st()
   print("Machine status:", status)



**Loading and Running a Marking File**
--------------------------------------

Typical workflow:

1. Load a file
2. Check status
3. Start marking

.. code-block:: python

   from gravotech.actions.actions import LDMode

   with Gravotech("192.168.0.211", 55555) as gravotech:
       gravotech.Actions.ld("example.t2l", 1, LDMode.NORMAL)

       status = gravotech.Actions.st()
       print("Status:", status)

       result = gravotech.Actions.go()
       print("Marking finished with:", result)



**Working with Variables**
--------------------------

You can set and get variables in the machine.

Set variable:

.. code-block:: python

   gravotech.Actions.vs(3, "SERIAL-12345")

Get variable:

.. code-block:: python

   value = gravotech.Actions.vg(3)
   print("Variable 3:", value)



**Managing Files on the Machine**
---------------------------------

List files:

.. code-block:: python

   files = gravotech.Actions.ls("*.t2l")
   print(files)

Upload a file:

.. code-block:: python

   data = b"0123456789ABCDEF"
   gravotech.Actions.pf("new_file.t2l", data)

Delete files:

.. code-block:: python

   gravotech.Actions.rm("old_file.t2l")



**Error Handling**
-------------------

If the machine returns an error (`ER ...`), a `ValueError` will be raised.

Example:

.. code-block:: python

   try:
       gravotech.Actions.ad()
   except ValueError as e:
       print("Machine error:", e)

For network errors, a `RuntimeError` may be raised.



**Thread Safety**
-----------------

The underlying `IPStreamer` uses a reentrant lock (`RLock`), which means:

- Multiple threads can safely call `gravotech.Actions.*` methods.
- Long operations like `GO` are automatically synchronized.



**Advanced Usage**
------------------

If you need direct access to low-level communication, you can use:

.. code-block:: python

   gravotech.Streamer.unsafe_write("ST")
   response = gravotech.Streamer.unsafe_read()

This is only recommended for advanced users.
