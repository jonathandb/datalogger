.. _requirements:
 
Minimum requirements
--------------------

If you want to run the datalogger without the need of writing code, you'll need hardware that is:

  * capable of running linux.
  * able to read sensors:

    * from modbus slaves via usb or ethernet. See also: :ref:`Connecting to modbus <hardware_modbus>` 
    * via I2C from a arduino compatible microcontroller.
  * able to connect to the internet periodically for communication with the server.

.. note:: It is possible to extend the software to read the data from elsewhere.
.. note:: Interesting hardware to log data are low cost, energy efficient ARM boards like the raspberry pi or the cubieboard. They use low power, have a serial connection, have gpio pins and are performant enough.

