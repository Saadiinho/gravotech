Utilisation
===========

Exemple simple d’utilisation :

.. code-block:: python

   from gravotech import Gravotech, LDMode

   with Gravotech("192.168.0.211", 55555) as g:
       g.Actions.ld("TEST.T2L", 1, LDMode.NORMAL)
       status = g.Actions.go()
       print("Statut final :", status)
