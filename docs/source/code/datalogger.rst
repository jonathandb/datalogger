
================
Class DataLogger
================

 * :ref:`data_init`
 * :ref:`load_online_configuration_and_initiate_sending_data`
 * :ref:`wait_for_connection_to_load_configuration`
 * :ref:`try_to_connect_to_internet`
 * :ref:`try_to_load_online_configuration`
 * :ref:`set_up_led_manager_calls`

.. _data_init:

__init__()
----------
In the intialisation method of the :class:`~datalogger.DataLogger` class, the code is encapsulated in an try-except block to catch possible errors that arise. If an error arises, before ending the datalogger the logs are sent to the server.

::

  try:
    ...
  
  except Exception as e:
    self.logger.error(e)
    self.log_send_store_handler.send_logs_job()
    raise


In the try-except block, following systems are intitialised:

 * :class:`~log_handlers_and_filters.LogSendStoreHandler`
 * :class:`~configuration_manager.ConfigurationManager`
 * :class:`~apscheduler.scheduler.Scheduler`  
 * :class:`~packet_manager.PacketManager`
 * :class:`~connection_manager.ConnectionManager`  


.. literalinclude:: ../../../datalogger/datalogger.py
   :pyobject: DataLogger.__init__
   :start-after: try:
   :end-before: # try to connect

Next, if there is a connection to the server, the online configuration is compared to the local one on the basis of a checksum. This happens in :ref:`load_online_configuration_and_initiate_sending_data`. After that the time is synchronised in :ref:`update_time` and the :class:`packet_manager` starts sending packets to the server in :ref:`initiate_send_packets`.
If there is no connection to the server a job is started that, as soon as the connection to the server is back, checks and optionally updates the configuration. 

.. literalinclude:: ../../../datalogger/datalogger.py
   :pyobject: DataLogger.__init__
   :start-after: self.connection)
   :end-before: # initiate sensor timers

After that, the :class:`~read_sensor_scheduler.ReadSensorScheduler` is started and the led manager is initialised. A message is showed to make clear that the initialisation is complete. 

.. literalinclude:: ../../../datalogger/datalogger.py
   :pyobject: DataLogger.__init__
   :start-after: self.wait_for_connection_to_load_configuration()
   :end-before: except Exception as e:

.. _load_online_configuration_and_initiate_sending_data:

load_online_configuration_and_initiate_sending_data()
-----------------------------------------------------
First the online configuration checksum is requested and compared to the local configuration. If it is different, the online configuration is downloaded, validated and saved locally. After that all stored packets are removed from memory since they are incompatible with the new configuration. 

The systems that use configuration paramaters are updated. The configuration update of the ReadSensorScheduler is in a try-except block because it is possible that it is not yet initialised. 

.. literalinclude:: ../../../datalogger/datalogger.py
   :pyobject: DataLogger.load_online_configuration_and_initiate_sending_data
   :end-before: try:  # try to remove job

A job is created in the method that loads itself periodically. The time interval between the job is defined in the configuration as parameter *timeintervaltocheckonlineconfig*.

The last step in the method is to initiate the start of sending packets.


.. literalinclude:: ../../../datalogger/datalogger.py
   :pyobject: DataLogger.load_online_configuration_and_initiate_sending_data
   :start-after: self.logger.warning('Problem updating configuration')

.. _wait_for_connection_to_load_configuration:

wait_for_connection_to_load_configuration()
-------------------------------------------
This method is started when there is no internet connection.
If there is no internet connection, it starts a job that periodically checks if there is a connection with internet. If there is an internet connection it checks if there is connection with the server. If it isn't, it starts a job that periodically checks if there is a connection with the server. 

.. literalinclude:: ../../../datalogger/datalogger.py
   :pyobject: DataLogger.wait_for_connection_to_load_configuration

.. _try_to_connect_to_internet:

try_to_connect_to_internet()
----------------------------
This method is started as a job, and checks if there is connection with the internet and the server. 

If there is connection with the internet:

 * It stops itself as a job.
 * It checks the connection with the server:
   
   * If there is connection with the server it runs :ref:`load_online_configuration_and_initiate_sending_data`.
   * If there is no connection with the server it starts :ref:`try_to_load_online_configuration` as a job.

.. literalinclude:: ../../../datalogger/datalogger.py
   :pyobject: DataLogger.try_to_connect_to_internet

.. _try_to_load_online_configuration:

try_to_load_online_configuration()
----------------------------------
It there is connection with the server :ref:`load_online_configuration_and_initiate_sending_data` is run and it stops itself as a job.

.. literalinclude:: ../../../datalogger/datalogger.py
   :pyobject: DataLogger.try_to_load_online_configuration

.. _set_up_led_manager_calls:

set_up_led_manager_calls()
--------------------------
For each system that needs to manipulate the state of leds a LedCall is being instantiated and implemented in it.

.. literalinclude:: ../../../datalogger/datalogger.py
   :pyobject: DataLogger.set_up_led_manager_calls

