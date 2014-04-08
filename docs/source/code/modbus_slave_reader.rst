=======================
Class ModbusSlaveReader
=======================

 * :ref:`modbus_init`
 * :ref:`read_register_value`
 * :ref:`check_connection`

.. _modbus_init:

__init__(serial_socket)
-----------------------
The logger is initialised. A :class:`~pymodbus.client.sync.ModbusSerialClient` instance is created with the passed parameter ``serial_socket`` as used serial port. A log filter ``modbus_client_filter`` is made to avoid too much log messages from :class:`~pymodbus.client.sync.ModbusSerialClient`. 

.. literalinclude:: ../../../datalogger/modbus_slave_reader.py
   :pyobject: ModbusSlaveReader.__init__

.. _read_register_value:

read_register_value(slave, register)
------------------------------------
A value is read from the modbus slave its register.

.. literalinclude:: ../../../datalogger/modbus_slave_reader.py
   :pyobject: ModbusSlaveReader.read_register_value


.. _check_connection:

check_connection()
------------------
This function is used in :ref:`check_modbus_connection` to make sure the connection with a modbus slave exists.

.. literalinclude:: ../../../datalogger/modbus_slave_reader.py
   :pyobject: ModbusSlaveReader.check_connection


