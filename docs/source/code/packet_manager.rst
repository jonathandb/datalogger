===================
Class PacketManager
===================

 * :ref:`packet_init`
 * :ref:`update_configuration`
 * :ref:`initiate_send_packets`


.. _packet_init:

__init__(scheduler)
-------------------
The scheduler is implemented so jobs can be created. The logger is initialised. The configuration is loaded.

.. literalinclude:: ../../../datalogger/packet_manager.py
   :pyobject: PacketManager.__init__

.. _update_configuration:

update_configuration()
-----------------------
The checksum, packet_send_interval and minimum_packets to send are loaded from the configuration. 
This method is loaded when the PacketManager is initialised and a new configuration is loaded (see :ref:`load_online_configuration_and_initiate_sending_data`).

.. literalinclude:: ../../../datalogger/packet_manager.py
   :pyobject: PacketManager.update_configuration

.. _initiate_send_packets:

initiate_send_packets(connection)
---------------------------------
The :class:`~connection_manager:ConnectionManager` instance is implemented and the configuration is updated

.. literalinclude:: ../../../datalogger/packet_manager.py
   :pyobject: PacketManager.initiate_send_packets

