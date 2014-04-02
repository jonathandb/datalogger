from datetime import datetime, date
from modbus_slave_reader import ModbusSlaveReader
import configuration
import logging


class MCUReadSensorScheduler:

    """
    This class sets up the timers that read the sensor data from the
    microcontroller
    """

    def __init__(self, scheduler, packet_manager):
        self.logger = logging.getLogger(__name__)
        self.scheduler = scheduler
        self.packet_manager = packet_manager

        self.update_configuration()

    def update_configuration(self):
        try:
            self.timers = configuration.timers
            self.i2c_slave_address = configuration.get_mcu_i2c_slave_address()
            self.i2c_bus_address = configuration.get_i2c_bus_address()

            try:
                self.scheduler.unschedule_func(self.check_mcu_connection)
                self.scheduler.unschedule_func(self.read_sensor)
            except:
                pass

            if not self.create_modbus_reader(self.i2c_bus_address,
                                             self.i2c_slave_address):
                # start job to check connection
                self.scheduler.add_interval_job(self.check_mcu_connection,
                                                seconds=10)
            else:
                self.create_timers()

        except:
            self.logger.warning(
                'Failed to update configuration of {0}'.format(__name__))

    def create_modbus_reader(self, i2c_bus_address, i2c_slave_address):
        self.modbus_slave_reader = ModbusSlaveReader(
            i2c_bus_address,
            i2c_slave_address)
        return self.modbus_slave_reader.check_mcu_connection()

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

    def check_mcu_connection(self):
        if self.modbus_slave_reader.check_mcu_connection():
            # stop this job
            self.scheduler.unschedule_func(self.check_mcu_connection)

            self.create_timers()

    def read_sensor(self, timer):
        values = []
        for slave in timer.slaves:
            self.modbus_slave_reader.request_modbus_value(
                slave.address,
                slave.register)
            values.append(self.modbus_slave_reader.read_value())

        self.packet_manager.store_packet(timer.type, values)
