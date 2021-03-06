from datetime import datetime, date
import configuration
import logging
import math


class ReadSensorScheduler:

    """
    This class is used to debug the datalogger without the need of a modbus
    network. Instead of using ModbusSlaveReader it returns random data when
    it is expected to read data.
    """

    def __init__(self, scheduler, packet_manager):
        self.logger = logging.getLogger(__name__)
        self.scheduler = scheduler
        self.packet_manager = packet_manager
        self.update_configuration()
        self.x = 0

    def update_configuration(self):
        try:
            self.timers = configuration.timers
            self.check_mcu_connection()

        except:
            self.logger.warning(
                'Failed to update configuration of %s' %
                __name__)

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

    def check_mcu_connection(self):
        try:
            self.scheduler.unschedule_func(self.read_sensor)
        except:
            pass

        # start timers
        for timer in self.timers:
            self.add_timer(timer)

    def read_sensor(self, timer):
        values = []

        for slave in timer.slaves:
            y = math.sin(self.x)*10
            if slave.address == 1 and slave.register == 1:
                values.append(y)
            # elif slave.address == 1 and slave.register == 2:
            #    values.append(-y)
            else:
                values.append((math.pow(self.x, 3) % 20) - 10)
        self.x += 0.1
        self.logger.debug("read random sensor")
        self.packet_manager.store_packet_in_memory(timer.type, values)
        try:
            self.led_call.flash()
        except:
            pass

    def set_led_call(self, led_call):
        self.led_call = led_call
