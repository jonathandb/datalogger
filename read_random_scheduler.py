from apscheduler.scheduler import Scheduler
from datetime import timedelta, time, datetime, date
import configuration
import random

class ReadSensorScheduler:
    def __init__(self, scheduler, packet_manager):
        self.scheduler = scheduler
        self.packet_manager = packet_manager
        self.update_configuration()
        
    def update_configuration(self):
        try:
            self.timers = configuration.timers 
            self.check_mcu_connection()

        except:
            self.logger.warning('Failed to update configuration of %s' % __name__)

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
            job = self.scheduler.add_interval_job(self.read_sensor,
                                                  seconds=timer.time_interval.total_seconds(), 
                                                  start_date=first_shot, 
                                                  args=[timer])

    def check_mcu_connection(self):
        try:
            self.scheduler.unschedule_func(self.read_sensor)
        except:
            pass

        #start timers
        for timer in self.timers:
            self.add_timer(timer)


    def read_sensor(self, timer):
        values = []
        for slave in timer.slaves:
            values.append(random.randint(1, 10))
        print("read random sensor")
        self.packet_manager.store_packet_in_memory(timer.type, values) 
