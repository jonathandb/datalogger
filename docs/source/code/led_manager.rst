
Class LedManager
================

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
The logger is initialised and the scheduler is implemented.
Each pin that the :class:`~led_manager.PinName` IntEnum contains is added to the self.leds list as a :class:`~led_manager.Led` object.

.. literalinclude:: ../../../datalogger/led_manager.py
   :pyobject: LedManager.__init__
   :url:

.. _update_led:

update_led(pin_name, ledstate)
------------------------------
This method is passed as a reference in the LedCall class. That way systems can call this method when they have implemented an LedCall object. See the :class:`~datalogger.DataLogger` method :ref:`set_up_led_manager_calls` to see the implementation.

Each time this method is called the gpio pin that is linked to a led in self.leds will be:

  * enabled if it isn't already done
  * checked if the state differs from the current state it will be changed

.. literalinclude:: ../../../datalogger/led_manager.py
   :pyobject: LedManager.update_led
   :url:

.. _enable_output:

enable_output(pin_nr)
---------------------
Tries to activate the gpio pin.
If the activation is successfull, the pin is set as output.

.. literalinclude:: ../../../datalogger/led_manager.py
   :pyobject: LedManager.enable_output
   :url:

.. _activate:

activate(pin_nr)
----------------
An attempt is done to activate the gpio pin by setting writing the pin_nr to 
the /sys/class/gpio/export socket. After that the socket location is stored in the self.pindirs list.

.. literalinclude:: ../../../datalogger/led_manager.py
   :pyobject: LedManager.activate
   :url:

.. _set_as_output:

set_as_output(pin_nr)
---------------------
An attempt is done to set the activated gpio pin as an output.

.. literalinclude:: ../../../datalogger/led_manager.py
   :pyobject: LedManager.set_as_output
   :url:

.. _turn_on:

turn_on(pin_nr)
---------------

.. literalinclude:: ../../../datalogger/led_manager.py
   :pyobject: LedManager.turn_on
   :url:

.. _turn_off:

turn_off(pin_nr)
----------------

.. literalinclude:: ../../../datalogger/led_manager.py
   :pyobject: LedManager.turn_off
   :url:
   
.. _flash:

flash(pin_nr, msecs)
--------------------

.. literalinclude:: ../../../datalogger/led_manager.py
   :pyobject: LedManager.flash
   :url:


