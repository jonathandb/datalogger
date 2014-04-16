=======================
Class ConnectionManager
=======================

 * :ref:`connection_init`
 * :ref:`conn_update_configuration`
 * :ref:`is_connected`
 * :ref:`check_internet_connection`
 * :ref:`check_server_connection`
 * :ref:`get_configuration_checksum`
 * :ref:`get_configuration`
 * :ref:`send_packets`
 * :ref:`validate_response`
 * :ref:`log_response`
 * :ref:`send_logs`
 * :ref:`conn_update_led`
 * :ref:`conn_set_led_call`

.. _connection_init:

__init__()
----------
The default json_header is set that is used when sending json data. The logger is initialised and a log filter for the requests package is made to limit its packages. The variable self.connected is set to False. It gives the possibility to see if the last connection to the internet or server was successfull. The configuration is loaded. 

.. literalinclude:: ../../../datalogger/connection_manager.py
   :pyobject: ConnectionManager.__init__
   :url:

.. _conn_update_configuration:

update_configuration()
----------------------
The server url is loaded from the configuration.
This method is loaded when the ConnectionManager is initialised and a new configuration is loaded (see :ref:`load_online_configuration_and_initiate_sending_data`).

.. literalinclude:: ../../../datalogger/connection_manager.py
   :pyobject: ConnectionManager.update_configuration
   :url:

.. _is_connected:

is_connected()
--------------
Returns the self.connected variable.

.. literalinclude:: ../../../datalogger/connection_manager.py
   :pyobject: ConnectionManager.is_connected
   :url:

.. _check_internet_connection:

check_internet_connection()
---------------------------
Tries to connect with the internet. If connected it returns ``True``, else ``False``.

.. literalinclude:: ../../../datalogger/connection_manager.py
   :pyobject: ConnectionManager.check_internet_connection
   :url:

.. _check_server_connection:

check_server_connection()
-------------------------
Tries to connect with the server. If connected it returns ``True``, else ``False``.

.. literalinclude:: ../../../datalogger/connection_manager.py
   :pyobject: ConnectionManager.check_server_connection
   :url:

.. _get_configuration_checksum:

get_configuration_checksum()
----------------------------
Returns the configuration checksum of the server. If the http status code is not 200, a :class:`requests.ConnectionError()` is raised so that an log message is generated and the outer try-except block in :ref:`load_online_configuration_and_initiate_sending_data` can catch it.

.. literalinclude:: ../../../datalogger/connection_manager.py
   :pyobject: ConnectionManager.get_configuration_checksum
   :url:

.. _get_configuration:

get_configuration()
-------------------
Returns the configuration as a json object. Similar to :ref:`get_configuration_checksum`, if the http status code is not 200, a :class:`requests.ConnectionError()` is raised so that an log message is generated and the outer try-except block in :ref:`load_online_configuration_and_initiate_sending_data` can catch it.

.. literalinclude:: ../../../datalogger/connection_manager.py
   :pyobject: ConnectionManager.get_configuration
   :url:

.. _send_packets:

send_packets(packets)
---------------------
The number of packets that are being sent is stored in ``nr_of_sent_packets``. Because packets can grow larger during the post request ``requests.post(self.server_url + PACKETS_URL_SUFFIX, data=json.dumps(packets), headers=self.json_header)`` when there is a slow internet connection.  ``nr_of_sent_packets`` is returned so that the number of sent packets can be removed from the stored packets in :class:`~packet_manager.PacketManager` in the method :ref:`send_packets_job`.

.. literalinclude:: ../../../datalogger/connection_manager.py
   :pyobject: ConnectionManager.send_packets
   :url:

.. _validate_response:

validate_response(post)
-----------------------
This method checks if received json packet is valid. 

.. literalinclude:: ../../../datalogger/connection_manager.py
   :pyobject: ConnectionManager.validate_response
   :url:

.. _log_response:

log_response(post)
------------------
This method logs if the response was successful with the included message from the server.

.. literalinclude:: ../../../datalogger/connection_manager.py
   :pyobject: ConnectionManager.log_response
   :url:

.. _send_logs:

send_logs(logs)
---------------
The number of logs that are being sent is stored in ``nr_of_sent_logs``. Because the list of logs can grow larger during the post request ``requests.post(self.server_url + LOGS_URL_SUFFIX, data=json.dumps(logs), headers=self.json_header)`` when there is a slow internet connection.  ``nr_of_sent_logs`` is returned so that the number of sent logs can be removed from the stored logs in :class:`~log_handlers_and_filters.LogSendStoreHandler` in the method :ref:`send_logs_job`.

.. literalinclude:: ../../../datalogger/connection_manager.py
   :pyobject: ConnectionManager.send_logs
   :url:

.. _conn_update_led:

update_led()
------------
Every time there is a possibility that the connection status (``self.connected``) is changed, this method is called to update the led status.

.. literalinclude:: ../../../datalogger/connection_manager.py
   :pyobject: ConnectionManager.update_led
   :url:

.. _conn_set_led_call:

set_led_call(led_call)
----------------------
This method implements the :class:`~led_manager.LedCall` instance.
