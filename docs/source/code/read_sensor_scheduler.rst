=========================
Class ReadSensorScheduler
=========================

 * :ref:`led_init`
 * :ref:`update_led`
 * :ref:`update_led`
 * :ref:`enable_output`
 * :ref:`activate`
 * :ref:`set_as_output`
 * :ref:`turn_on`
 * :ref:`turn_off`
 * :ref:`flash`


.. _led_init:

__init__(scheduler)
-------------------
The logger is initialised. The :class:`~apscheduler:scheduler:Scheduler` and :class:`~packet_manager:PacketManager` are implemented. The configuration is loaded. 

.. literalinclude:: ../../../datalogger/read_sensor_scheduler.py
   :pyobject: ReadSensorScheduler.__init__

.. _update_configuration:

update_configuration()
----------------------
The timers are loaded from the configuration. :ref:`create_modbus_reader` is run. When the creation was successfull, the :ref:`check_modbus_connection` job is started which tries to connect with the modbus slaves. When this is successfull, the timers are created in :ref:`create_timers`. 
This method is loaded when the PacketManager is initialised and a new configuration is loaded (see :ref:`load_online_configuration_and_initiate_sending_data`).

.. literalinclude:: ../../../datalogger/read_sensor_scheduler.py
   :pyobject: ReadSensorScheduler.update_configuration

.. _create_modbus_reader:

create_modbus_reader()
----------------------
In this function a :class:`~modbus_slave_reader:ModbusSlaveReader` instance is made and an attempt is made to connected with the modbus slaves.

.. literalinclude:: ../../../datalogger/read_sensor_scheduler.py
   :pyobject: ReadSensorScheduler.create_modbus_reader

.. _add_timer:

add_timer(timer)
----------------
This method calculates what the time is when the timer goes off. Then a :ref:`read_sensor` job is created that  is run when the sensors of the timer needs to be read.

.. literalinclude:: ../../../datalogger/read_sensor_scheduler.py
   :pyobject: ReadSensorScheduler.add_timer

.. _create_timers:

create_timers()
---------------
All possible previous :ref:`read_sensor` jobs are deleted and all new timers are created with :ref:`add_timer`.

.. literalinclude:: ../../../datalogger/read_sensor_scheduler.py
   :pyobject: ReadSensorScheduler.create_timers

.. _check_modbus_connection:

check_modbus_connection()
-------------------------
This function checks the connection of the :class:`~modbus_slave_reader:ModbusSlaveReader` isntance. If the connection is successfull, it creates the timers.

.. literalinclude:: ../../../datalogger/read_sensor_scheduler.py
   :pyobject: ReadSensorScheduler.check_modbus_connection


.. _read_sensor:

read_sensor(timer)
------------------
This method is run when the timer goes off. It reads all the sensors that belongs to the timer and puts them in a list which is then stored in the :class:`~packet_manager:PacketManager` with the :ref:`store_packet_in_memory` method. A signal is given to the led_manager to flash the sensor led.

.. literalinclude:: ../../../datalogger/read_sensor_scheduler.py
   :pyobject: ReadSensorScheduler.read_sensor

.. _set_led_call:

set_led_call(led_call)
----------------------
This method implements the :class:`~led_manager:LedCall` isntance.

.. literalinclude:: ../../../datalogger/read_sensor_scheduler.py
   :pyobject: ReadSensorScheduler.set_led_call


