Code explained
==============


================
class DataLogger
================

__init__ 
--------
In the intialisation function of the :class:`~datalogger.DataLogger` class, the code is encapsulated in an try-except block to catch possible errors that arise. If an error arises, before ending the datalogger the logs are sent to the server.

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

::
  
  # initiate logger
  self.logger = logging.getLogger()
  self.logger.setLevel(logging.DEBUG)
  self.log_send_store_handler = LogSendStoreHandler(LOG_LOCATION)
  formatter = logging.Formatter(
      '%(asctime)s - %(levelname)s - %(name)s - %(message)s')
  self.log_send_store_handler.setFormatter(formatter)
  self.logger.addHandler(self.log_send_store_handler)
  self.logger.info('Initialising system...')
  job_info_filter = JobInfoFilter()
  logging.getLogger('apscheduler.scheduler').addFilter(
      job_info_filter)
  logging.getLogger('apscheduler.threadpool').addFilter(
      job_info_filter)

  # load local configuration
  self.conf_man = ConfigurationManager(CONFIG_LOCATION)
  self.log_send_store_handler.update_configuration()

  self.scheduler = Scheduler()
  self.scheduler.start()

  self.packet_manager = PacketManager(self.scheduler)

  # initiate network connection
  self.connection = ConnectionManager()

  # add scheduler and connection to log handler
  self.log_send_store_handler.update_configuration(
      self.scheduler,
      self.connection)

Next, if there is a connection to the server, the online configuration is compared to the local one on the basis of a checksum.
If there is no connection to the server a job is started that, as soon as the connection to the server is back, checks and optionally updates the configuration. 

::

  # try to connect
  connected = self.connection.check_internet_connection(
      ) and self.connection.check_server_connection()
  if connected:
      self.load_online_configuration_and_initiate_sending_data()
      self.packet_manager.initiate_send_packets(self.connection)
  else:
      '''
      if there is no connection:
          keep checking for a connection
          temporarily use offline timer and modbus slave
          configuration
      '''
      self.wait_for_connection_to_load_configuration()

After that, the :class:`~read_sensor_scheduler.ReadSensorScheduler` is started and the led manager is initialised::

  # initiate sensor timers
  self.read_sensor_scheduler = ReadSensorScheduler(
      self.scheduler,
      self.packet_manager)
  self.led_manager = LedManager(self.scheduler)
  self.led_manager.update_led(PinName.powered, LedState.on)
  self.set_up_led_manager_calls()

