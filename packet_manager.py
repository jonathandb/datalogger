from apscheduler.scheduler import Scheduler
from datetime import timedelta, time, datetime, date
import configuration
from connection_manager import ConnectionManager
from configuration_manager import ConfigurationManager
import time
import logging
import json


class PacketManager():
    def __init__(self, scheduler):
        self.scheduler = scheduler
        self.packets = []
        self.logger = logging.getLogger(__name__)
        self.update_configuration()
       
    def update_configuration(self):
        try:
            self.checksum = configuration.get_checksum()
            self.packet_send_interval = configuration.get_time_interval_to_send_packets()
            self.minimum_packets_to_send = configuration.get_minimum_packets_to_send()
        except:
            self.logger.warning('Failed to update configuration of %s' % __name__)   
    
    def initiate_send_packets(self, connection):
        self.connection = connection
        self.update_configuration()
        
        try:
            self.scheduler.unschedule_func(self.send_packets_job)
        except:
            pass
       
        try:
            #start job to send packets
            self.scheduler.add_interval_job(self.send_packets_job,
                                            seconds=self.packet_send_interval)
        except:
            self.logger.error("Failed to start send packets job, incomplete configuration")

    def send_packets_job(self):
        if self.minimum_packets_to_send < len(self.packets):
            #try to send packets
            nr_of_packets = len(self.packets)
            if self.connection.send_packets(self.packets):
                #success, clear sent packets
                self.logger.info("%s packets sent", nr_of_packets)
                self.packets = []
        else:
            #not enough packets to send, initiate job with small interval to keep checking
            #number of packets
            try:
                self.scheduler.unschedule_func(self.check_packets_to_send)
            except:
                pass

            self.scheduler.add_interval_job(self.check_packets_to_send,
                                            seconds=1)

    def check_packets_to_send(self):
         if self.minimum_packets_to_send < len(self.packets):
            #try to send packets
            if self.connection.send_packets(self.packets):
                #success, clear sent packets
                self.packets = []
                #stop this timer
                try:
                    self.scheduler.unschedule_func(self.check_packets_to_send)
                except:
                    pass

    def store_packet_in_memory(self, type, values):
        #type, timestamp, values
        timestamp = time.mktime(datetime.now().timetuple())
        packet = {'checksum': self.checksum, 'type': type, 'timeDate': timestamp, 'sensorData': values}
        self.packets.append(packet)

    def remove_all_packets_from_memory(self):
        self.packets = []
