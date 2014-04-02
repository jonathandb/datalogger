import logging
import logging.handlers
import configuration
import os
from datetime import datetime
import time

SINGLE_LOG_FILE_SIZE = 500000


class LogSendStoreHandler(logging.Handler):

    """This handler decides what happens with the created logs messages.
    The logs can be sent to the server or/and stored locally.
    The sending and storing can done in configurable time intervals to
    limit wear of network connection and storage.
    """

    def __init__(self, log_location):
        logging.Handler.__init__(self)

        if not hasattr(self, 'send_logs'):
            self.send_logs = []

        if not hasattr(self, 'file_logs'):
            self.file_logs = []

        self.log_location = log_location
        self.configured = False
        self.logger = logging.getLogger()
        self.update_configuration()

    def update_configuration(self, *args, **kwargs):
        try:
            self.send_log_level = self.get_log_level_by_string(
                configuration.get_log_level_to_send_to_server())
            self.store_log_level = self.get_log_level_by_string(
                configuration.get_log_level_to_store_local())
            self.time_interval_to_send_log = configuration.get_time_interval_to_send_log(
                )
            self.time_interval_to_store_local = configuration.get_time_interval_to_store_local(
                )
            self.max_log_size = configuration.get_max_local_log_size()

            try:
                scheduler = kwargs.get('scheduler', None)
                connection = kwargs.get('connection', None)
                if configuration.is_store_logs_local():
                    self.initiate_store_logs(scheduler, self.log_location)
                if configuration.is_send_logs_to_server():
                    self.initiate_send_logs(connection, scheduler)
            except:
                pass

            self.configured = True
        except:
            self.configured = False
            self.logger.warning(
                'Failed to update configuration of {0}'.format(__name__))

    def emit(self, record):
        """Is called when a log is created.
        If logs needs to be sent or stored, they are stored in their
        corresponding lists.
        """
        try:
            print(self.format(record))

            try:
                self.led_call.flash()
            except:
                pass

            if self.configured:
                if record.levelno >= self.send_log_level:
                    timestamp = time.mktime(datetime.now().timetuple())
                    log = {'msg': record.msg,
                           'funcName': record.funcName,
                           'filename': record.filename,
                           'lineno': record.lineno,
                           'levelno': record.levelno,
                           'timeDate': timestamp}
                    self.send_logs.append(log)

                if record.levelno >= self.store_log_level:
                    msg = self.format(record)
                    self.file_logs.append(msg)

        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

    def get_log_level_by_string(self, levelstring):
        if levelstring == 'CRITICAL':
            return 50
        elif levelstring == 'ERROR':
            return 40
        elif levelstring == 'WARNING':
            return 30
        elif levelstring == 'INFO':
            return 20
        elif levelstring == 'DEBUG':
            return 10
        else:
            return 0

    def initiate_send_logs(self, connection, scheduler):
        self.connection = connection

        try:
            scheduler.unschedule_func(self.send_logs_job)
        except:
            pass

        scheduler.add_interval_job(self.send_logs_job,
                                   seconds=self.time_interval_to_send_log)

    def initiate_store_logs(self, scheduler, log_location):
        base_filename = "datalogger.log"

        try:
            # check if folder exists, if not: create one
            if not os.path.exists(log_location):
                os.mkdir(log_location)

            if os.path.isfile(log_location):
                i = 0
                while os.path.isfile(log_location + str(i)):
                    i += 1
                if not os.path.isfolder(log_location):
                    os.mkdir(log_location)
        except Exception as e:
            self.logger.warning('Unable to create log folder: {0}'.format(e))

        self.abs_path_log_folder = os.path.abspath(log_location)
        self.abs_path_log = os.path.abspath(
            os.path.join(
                log_location,
                base_filename))

        try:
            scheduler.unschedule_func(self.store_logs_job)
        except:
            pass

        scheduler.add_interval_job(self.store_logs_job,
                                   seconds=self.time_interval_to_store_local)

    def send_logs_job(self):
        """Is called on a time interval set in the configuration.
        If sending of the logs is successfull, the logs that needs to be sent
        are cleared.
        """
        if len(self.send_logs) > 1:
            nr_of_sent_logs = self.connection.send_logs(self.send_logs)
            if nr_of_sent_logs > 0:
                # successfull sent, clear sent logs
                del self.send_logs[0:nr_of_sent_logs]

    def store_logs_job(self):
        """Is called on a time interval set in the configuration.
        """
        self.keep_logfile_in_max_limits()
        try:
            if len(self.file_logs) > 1:
                stream = open(self.abs_path_log, 'a')
                for msg in self.file_logs:
                    stream.write('{0}\n'.format(msg))
                stream.close()
                self.file_logs = []
        except Exception as e:
            self.logger.error('Unable to write log: {0}'.format(e))

    def keep_logfile_in_max_limits(self):
        """Organises the logfiles.
        If a logfile is to big, it is stored under an other name and a
        new logfile is created.
        If there are too many logfiles, the oldest one is removed.
        The total max log size is set in the configuration. The individual
        log file size is set in global variable SINGLE_LOG_FILE_SIZE .
        """
        total_size, highest_log_number = self.examine_logfolder()

        # remove logs until logs are under max local log size
        try:
            while total_size > self.max_log_size:
                os.remove(self.abs_path_log + '.' + str(highest_log_number))
                highest_log_number -= 1
                total_size, highest_log_number = self.examine_logfolder()
        except:
            self.logger.error('Unable to remove log file {0}'.format(
                              self.abs_path_log + '.' +
                              str(highest_log_number)))

        # rename logs
        try:
            if os.path.isfile(self.abs_path_log):
                size = os.path.getsize(os.path.abspath(self.abs_path_log))
                if size > SINGLE_LOG_FILE_SIZE:
                    log_nr = highest_log_number
                    while log_nr >= 0:
                        os.rename(self.abs_path_log + '.' + str(log_nr),
                                  self.abs_path_log + '.' + str(log_nr + 1))
                        log_nr -= 1
                    os.rename(self.abs_path_log, self.abs_path_log + '.0')
        except:
            self.logger.error(
                'Unable to rename log file {0}'.format(
                    self.abs_path_log))

    def examine_logfolder(self):
        total_size = 0
        highest_log_nr = -1

        for dirpath, dirnames, filenames in os.walk(self.abs_path_log_folder):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
                base_name = os.path.basename(self.abs_path_log)
                if base_name in f:
                    try:
                        nr = int(f.split('.')[-1])
                        if highest_log_nr < nr:
                            highest_log_nr = nr
                    except ValueError:
                        # nr is not a number
                        pass
        return (total_size, highest_log_nr)

    def set_led_call(self, led_call):
        self.led_call = led_call


class JobInfoFilter(logging.Filter):

    """Filter for the apscheduler lib logs"""

    def filter(self, record):
        return not record.levelno <= logging.WARNING


class ModbusClientFilter(logging.Filter):

    """Filter for the modbus lib logs"""

    def filter(self, record):
        if 'Could not configure port' not in str(record.msg):
            return record
