===================
Class PacketManager
===================

 * :ref:`packet_init`
 * :ref:`packet_update_configuration`
 * :ref:`initiate_send_packets`
 * :ref:`send_packets_job`
 * :ref:`check_packets_to_send`
 * :ref:`store_packet_in_memory`
 * :ref:`remove_all_packets_from_memory`

.. _packet_init:

__init__(scheduler)
-------------------
The scheduler is implemented so jobs can be created. The logger is initialised. The configuration is loaded.

.. literalinclude:: ../../../datalogger/packet_manager.py
   :pyobject: PacketManager.__init__

.. _packet_update_configuration:

update_configuration()
-----------------------
The checksum, packet_send_interval and minimum_packets to send are loaded from the configuration. 
This method is loaded when the PacketManager is initialised and a new configuration is loaded (see :ref:`load_online_configuration_and_initiate_sending_data`).

.. literalinclude:: ../../../datalogger/packet_manager.py
   :pyobject: PacketManager.update_configuration

.. _update_time:

update_time()
-----------------------
If ntp time is not yet synced (``self.packets_synced``), the time is checked online with the ntplib. In ``self.time_offset`` the time difference is stored and the timestamps of all the already logged packets are updated.

.. literalinclude:: ../../../datalogger/packet_manager.py
   :pyobject: PacketManager.update_time

.. _initiate_send_packets:

initiate_send_packets(connection)
---------------------------------
The :class:`~connection_manager.ConnectionManager` instance is implemented and the configuration is updated. A single scheduled job of :ref:`send_packets_job` is started.

.. literalinclude:: ../../../datalogger/packet_manager.py
   :pyobject: PacketManager.initiate_send_packets

.. _send_packets_job:

send_packets_job()
------------------
Checks if the minimum of packets that needs to be sent is reached. If it is reached the packets will be sent, otherwise a single scheduled job of :ref:`check_packets_to_send` is started. When :ref:`send_packets` function returns the number of sent packets ``nr_of_sent_packets``, the first ``nr_of_sent_packets`` are removed from ``self.packets``.

.. literalinclude:: ../../../datalogger/packet_manager.py
   :pyobject: PacketManager.send_packets_job
   :start-after: RETRY_SEND_PACKETS_INTERVAL."""

.. _check_packets_to_send:

check_packets_to_send()
-----------------------
This job is started when the ``self.packet_send_interval`` is reached for the :ref:`send_packets_job`, but there are not enough packets to send. It will check with a smaller time interval, ``RETRY_SEND_PACKETS_INTERVAL``, if there are enough packets to send.

.. literalinclude:: ../../../datalogger/packet_manager.py
   :pyobject: PacketManager.check_packets_to_send

.. _store_packet_in_memory:

store_packet_in_memory(type, values)
------------------------------------

The timer type and the values are passed to this method and stored together with the current UNIX UTC time ``timestamp`` and the configuration checksum in a packet. That packet is appended to the self.packets list.
If the time is synced (``self.packets_synced``) in :ref:`update_time`, the ``self.time_offset`` is added to the timestamp. 

.. literalinclude:: ../../../datalogger/packet_manager.py
   :pyobject: PacketManager.store_packet_in_memory

.. _remove_all_packets_from_memory:

remove_all_packets_from_memory()
--------------------------------
If a new configuration is loaded from the internet in :ref:`load_online_configuration_and_initiate_sending_data`, the packets that were stored from the old configuration are all removed.

.. literalinclude:: ../../../datalogger/packet_manager.py
   :pyobject: PacketManager.remove_all_packets_from_memory


