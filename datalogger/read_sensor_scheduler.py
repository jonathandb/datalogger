from datetime import datetime, date
from modbus_slave_reader import ModbusSlaveReader
import configuration
import logging


class ReadSensorScheduler:

    """
    This class sets up the timers that read the sensor data
    """

    def __init__(self, scheduler, packet_manager):
        self.logger = logging.getLogger(__name__)
        self.scheduler = scheduler
        self.packet_manager = packet_manager

        self.update_configuration()

    def update_configuration(self):
        try:
            self.timers = configuration.timers
            try:
                self.scheduler.unschedule_func(self.check_modbus_connection)
                self.scheduler.unschedule_func(self.read_sensor)
            except:
                pass

            if not self.create_modbus_reader('/dev/ttyS0'):
                # start job to check connection
                self.scheduler.add_interval_job(self.check_modbus_connection,
                                                seconds=10)
            else:
                self.create_timers()

        except:
            self.logger.warning(
                'Failed to update configuration of %s' %
                __name__)
            raise

    def create_modbus_reader(self, serial_port):
        self.modbus_slave_reader = ModbusSlaveReader(serial_port)
        return self.modbus_slave_reader.check_connection()

    def add_timer(self, timer):
        if len(timer.slaves) > 0:
            now = datetime.now()
            first_shot = datetime.combine(date.today(), timer.start_time)

            if first_shot <= now:
                while first_shot <= now:
                    first_shot += timer.time_interval

            else:
                while first_shot > now:
                    first_shot -= timer.time_interval

            self.scheduler.add_interval_job(
                self.read_sensor,
                seconds=timer.time_interval.total_seconds(),
                start_date=first_shot,
                args=[timer])

    def create_timers(self):
        # remove possible previous added timers
        try:
            self.scheduler.unschedule_func(self.read_sensor)
        except:
            pass

        # start timers
        for timer in self.timers:
            self.add_timer(timer)

    def check_modbus_connection(self):
        if self.modbus_slave_reader.check_connection():
            # stop this job
            self.scheduler.unschedule_func(self.check_modbus_connection)

            self.create_timers()

    def read_sensor(self, timer):
        values = []
        for slave in timer.slaves:
            value = self.modbus_slave_reader.read_register_value(
                slave.address,
                slave.register)
            values.append(value)

        self.packet_manager.store_packet_in_memory(timer.type, values)
        try:
            self.led_call.flash()
        except:
            pass

    def set_led_call(self, led_call):
        self.led_call = led_call
