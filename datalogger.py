from configuration_manager import ConfigurationManager
#from read_sensor_scheduler import ReadSensorScheduler
from read_random_scheduler import ReadSensorScheduler
from time import sleep
import configuration
import logging
import logging.handlers
from log_handlers_and_filters import LogSendStoreHandler, JobInfoFilter
from apscheduler.scheduler import Scheduler
from connection_manager import ConnectionManager
from packet_manager import PacketManager
import pdb
from led_manager import LedManager, Led, LedState, PinName, LedCall
import os

LOG_LOCATION = '/var/log/datalogger/'
CONFIG_LOCATION = os.path.join(os.path.expanduser('~'), '.config/datalogger.ini')
CHECK_CONNECTION_INTERVAL = 60

class DataLogger:
    def __init__(self):

        try:
            #initiate logger
            self.logger = logging.getLogger()

            self.logger.setLevel(logging.DEBUG)

            self.log_send_store_handler = LogSendStoreHandler(LOG_LOCATION)

            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
            self.log_send_store_handler.setFormatter(formatter)

            memory_handler = logging.handlers.MemoryHandler(1)
            memory_handler.setTarget(self.log_send_store_handler)
            self.logger.addHandler(memory_handler)

            self.logger.info('Initialising system...')
            #load local configuration
            self.conf_man = ConfigurationManager(CONFIG_LOCATION)
            self.log_send_store_handler.update_configuration()

            self.scheduler = Scheduler()
            self.scheduler.start()
            job_info_filter = JobInfoFilter()
            logging.getLogger('apscheduler.scheduler').addFilter(job_info_filter)
            logging.getLogger('apscheduler.threadpool').addFilter(job_info_filter)
            self.packet_manager = PacketManager(self.scheduler)

            #initiate network connection
            self.connection = ConnectionManager()

            #add scheduler and connection to log handler
            self.log_send_store_handler.update_configuration(self.scheduler, self.connection)

            #try to connect
            connected = self.connection.check_internet_connection() and self.connection.check_server_connection()
            if connected:

                self.load_online_configuration_and_initiate_sending_data()
                self.packet_manager.initiate_send_packets(self.connection)
            else:
                '''
                if there is no connection:
                    keep check for a connection
                    temporarily use offline timer and modbus slave configuration
                '''

                self.wait_for_connection_to_load_configuration()

            #initiate sensor timers
            self.read_sensor_scheduler = ReadSensorScheduler(self.scheduler,
                                                             self.packet_manager)
            self.led_manager = LedManager(self.scheduler)
            self.led_manager.update_led(PinName.powered, LedState.on)
            self.set_up_led_manager_calls()

            #sleep 1 second to intialise led of log handler
            sleep(1)
            self.logger.info('Initialisation complete')

            while True:
                sleep(10)
                self.logger.debug('Alive and kicking')
                self.scheduler.print_jobs()

        except Exception as e:
            self.logger.error(e)
            self.log_send_store_handler.send_logs_job()
            raise

    def set_up_led_manager_calls(self):
        sensor_led_call = LedCall(self.led_manager, PinName.readingsensor)
        connected_led_call = LedCall(self.led_manager, PinName.connected)
        logging_led_call = LedCall(self.led_manager, PinName.logging)

        self.read_sensor_scheduler.set_led_call(sensor_led_call)
        self.connection.set_led_call(connected_led_call)
        self.log_send_store_handler.set_led_call(logging_led_call)

    def load_online_configuration_and_initiate_sending_data(self):
        #check online configuration
        try:
            online_checksum = self.connection.get_checksum()
            self.logger.info("Checking online configuration..")
            if self.conf_man.is_configuration_online_different(online_checksum):
                self.logger.info("Online configuration is new, updating configuration..")
                #online configuration is different
                online_configuration = self.connection.get_configuration()
                self.conf_man.validate_json_configuration(online_configuration)
                self.conf_man.save_online_configuration_local(online_checksum,
                                                             online_configuration)
                self.packet_manager.remove_all_packets_from_memory()

                #update systems that make use of the configuration
                self.log_send_store_handler.update_configuration(self.scheduler, self.connection)
                self.connection.update_configuration()
                try:
                    self.read_sensor_scheduler.update_configuration()
                except:
                    pass
                self.packet_manager.update_configuration()
        except:
            self.logger.warning('Problem updating configuration')
            raise
        try:
            self.scheduler.unschedule_func(self.load_online_configuration_and_initiate_sending_data)
        except:
            pass

        #periodically check changes in configuration
        self.scheduler.add_interval_job(self.load_online_configuration_and_initiate_sending_data,
                                        seconds=configuration.get_time_interval_to_check_online_config())

        self.packet_manager.initiate_send_packets(self.connection)

    def wait_for_connection_to_load_configuration(self):
        if not self.connection.is_connected():
            #no internet connection, start job to check connection
            self.scheduler.add_interval_job(self.try_to_connect_to_internet,
                                            seconds=CHECK_CONNECTION_INTERVAL)
        else:
            if not self.connection.check_server_connection():
                #no connection with server, start job to check connection
                self.scheduler.add_interval_job(self.try_to_load_online_configuration,
                                                seconds=CHECK_CONNECTION_INTERVAL)

    def try_to_connect_to_internet(self):
        if self.connection.check_internet_connection():
            self.scheduler.unschedule_func(self.try_to_connect_to_internet)

            if not self.connection.check_server_connection():
                    #no connection with server, start job to check connection
                    self.scheduler.add_interval_job(self.try_to_load_online_configuration,
                                                    seconds=CHECK_CONNECTION_INTERVAL)
            else:
                self.load_online_configuration_and_initiate_sending_data()

    def try_to_load_online_configuration(self):
        if self.connection.check_server_connection():
            self.load_online_configuration_and_initiate_sending_data()

            self.scheduler.unschedule_func(self.try_to_load_online_configuration)



dl = DataLogger()


