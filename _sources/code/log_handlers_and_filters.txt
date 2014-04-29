=========================
Class LogSendStoreHandler
=========================

 * :ref:`logsendstore_init`
 * :ref:`log_update_configuration`
 * :ref:`emit`
 * :ref:`get_log_level_by_string`
 * :ref:`initiate_send_logs`
 * :ref:`initiate_store_logs`
 * :ref:`send_logs_job`
 * :ref:`store_logs_job`
 * :ref:`keep_logfile_in_max_limits`
 * :ref:`examine_logfolder`
 * :ref:`log_set_led_call`

.. _logsendstore_init:

__init__(log_location)
----------------------
The parent ``Handler`` class is initialised. The ``self.send_logs`` and ``self.file_logs`` lists are made if they don't exist yet. The passed parameter ``log_location`` is stored. The variable self.configured is set to False. The logger is initialised.  It gives the possibility to see if the last connection to the internet or server was successfull. The configuration is loaded. 

.. literalinclude:: ../../../datalogger/log_handlers_and_filters.py
   :pyobject: LogSendStoreHandler.__init__
   :url:

.. _log_update_configuration:

update_configuration(\*\*kwargs)
--------------------------------
Different needed parameters are loaded from the configuration. If ``scheduler`` is passed and the storage of logs is enabled in the configuration, then the logs store job is started in :ref:`initiate_store_logs`. If ``scheduler`` and ``connection`` are passed and the sending of logs to the server is enabled in the configuration, then the logs store job is started in :ref:`initiate_send_logs`.
This method is run in :ref:`data_init` when the :class:`~packet_manager.PacketManager` is initialised, the :class:`~apscheduler.scheduler.Scheduler` is loaded, the :class:`~connection_manager.ConnectionManager` is loaded and alsa when a new configuration is loaded in (see :ref:`load_online_configuration_and_initiate_sending_data`).

.. literalinclude:: ../../../datalogger/log_handlers_and_filters.py
   :pyobject: LogSendStoreHandler.update_configuration
   :url:

.. _emit:

emit(record)
------------
When a new log is created this method is called. The log is printed to the console and the :class:`~led_manager.LedManager` is called to flash a led. After configuration is complete, logs can be stored in ``self.send_logs`` and ``self.file_logs``.

.. literalinclude:: ../../../datalogger/log_handlers_and_filters.py
   :pyobject: LogSendStoreHandler.emit
   :url:


.. _get_log_level_by_string:

get_log_level_by_string(levelstring)
------------------------------------
This method converts the log level in string format to its numeric value.

.. literalinclude:: ../../../datalogger/log_handlers_and_filters.py
   :pyobject: LogSendStoreHandler.get_log_level_by_string
   :url:


.. _initiate_send_logs:

initiate_send_logs(connection, scheduler)
-----------------------------------------
The :class:`~connection_manager.ConnectionManager` instance is implemented. A single scheduled job of :ref:`send_logs_job` is started.

.. literalinclude:: ../../../datalogger/log_handlers_and_filters.py
   :pyobject: LogSendStoreHandler.initiate_send_logs
   :url:


.. _initiate_store_logs:

initiate_store_logs(scheduler, log_location)
--------------------------------------------
First it is checked if the log folder exists, if not it is created. A single scheduled job of :ref:`store_logs_job` is started.

.. literalinclude:: ../../../datalogger/log_handlers_and_filters.py
   :pyobject: LogSendStoreHandler.initiate_store_logs
   :url:


.. _send_logs_job:

send_logs_job()
---------------
This jobs sends the logs via the :class:`~connection_manager.ConnectionManager`. If sending of the logs is successfull, the logs that were sent are cleared.

.. literalinclude:: ../../../datalogger/log_handlers_and_filters.py
   :pyobject: LogSendStoreHandler.send_logs_job
   :url:

.. _store_logs_job:

store_logs_job()
----------------
After running :ref:`keep_logfile_in_max_limits` the logs are stored in ``self.abs_path_log``.

.. literalinclude:: ../../../datalogger/log_handlers_and_filters.py
   :pyobject: LogSendStoreHandler.store_logs_job
   :url:


.. _keep_logfile_in_max_limits:

keep_logfile_in_max_limits()
----------------------------
Organises the logfiles. If a logfile is to big, it is stored under another name and a new logfile is created. If there are too many logfiles, the oldest one is removed. The total max log size is set in the configuration. The individual log file size is set in global variable SINGLE_LOG_FILE_SIZE.

.. literalinclude:: ../../../datalogger/log_handlers_and_filters.py
   :pyobject: LogSendStoreHandler.keep_logfile_in_max_limits
   :url:


.. _examine_logfolder:

examine_logfolder()
-------------------
Is used in :ref:`keep_logfile_in_max_limits` to calculate the total log size, and the biggest log number.

.. literalinclude:: ../../../datalogger/log_handlers_and_filters.py
   :pyobject: LogSendStoreHandler.examine_logfolder
   :url:


.. _log_set_led_call:

set_led_call(led_call)
----------------------
This method implements the :class:`~led_manager.LedCall` instance.

.. literalinclude:: ../../../datalogger/log_handlers_and_filters.py
   :pyobject: LogSendStoreHandler.set_led_call
   :url:


