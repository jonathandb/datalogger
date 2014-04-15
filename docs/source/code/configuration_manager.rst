==========================
Class ConfigurationManager
==========================

 * :ref:`conf_init`
 * :ref:`load_local_configuration`
 * :ref:`is_online_configuration_different`
 * :ref:`validate_json_configuration`
 * :ref:`save_configuration_local`
 * :ref:`try_save_configuration_parameter`

.. _conf_init:

__init__()
----------
The logger is initialised. And the configuration location ``config_location`` is passed from the constructor. After that the local configuration is loaded in :ref:`load_local_configuration`

.. literalinclude:: ../../../datalogger/configuration_manager.py
   :pyobject: ConfigurationManager.__init__

.. _load_local_configuration:

load_local_configuration
------------------------
As the method title says, it loads the local configuration. The whole process of loading the configuration is put in a try-except block. In it, the :class:`~configparser.ConfigParser` object is initialised and the configuration location is set in it.. 
When the configuration or a configuration parameter is not found, it is cached in it. The configuration is stored in global variables in the :mod:`configuration` module.

.. literalinclude:: ../../../datalogger/configuration_manager.py
   :pyobject: ConfigurationManager.load_local_configuration


.. _is_online_configuration_different:

is_online_configuration_different
---------------------------------
Compares the passed variable online_checksum with the local checksum and returns True if they differ.

.. literalinclude:: ../../../datalogger/configuration_manager.py
   :pyobject: ConfigurationManager.is_online_configuration_different


.. _validate_json_configuration:

validate_json_configuration
---------------------------
This method is used to check if the downloaded configuration in json format is valid.

.. literalinclude:: ../../../datalogger/configuration_manager.py
   :pyobject: ConfigurationManager.validate_json_configuration


.. _save_configuration_local:

save_configuration_local
------------------------
In this method the passed configuration is stored locally. To make sure all configuration sections exist, an attempt is done to create them.  To store the parameters as optimal as possible, they are each loaded in a seperate try-except block in the method :ref:`try_save_configuration_parameter`.

When all the configuration parameters are stored in the :mod:`configuration` module, the physical storing of the configuration is done. First it is checked if the folder of the configuration exists. If not, it is created recursively with the ``os.makedirs(config_dirpath)`` method. After that, the configuration is stored in the folder.


.. literalinclude:: ../../../datalogger/configuration_manager.py
   :pyobject: ConfigurationManager.save_configuration_local


.. _try_save_configuration_parameter:

try_save_configuration_parameter
--------------------------------
An attempt is done to store the online configuration parameter in the :mod:`configuration` module. 

.. literalinclude:: ../../../datalogger/configuration_manager.py
   :pyobject: ConfigurationManager.try_save_configuration_parameter


