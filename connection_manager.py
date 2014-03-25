from apscheduler.scheduler import Scheduler
import configuration
from configuration_manager import ConfigurationManager
import time
import requests
import logging
import json

class ConnectionManager:
    def __init__(self, scheduler):
        self.scheduler = scheduler
        self.json_header = {'content-type': 'application/json'}
        self.logger = logging.getLogger(__name__)
        self.connected = False
        self.update_configuration()

    def update_configuration(self):
        try:
            self.server_url = configuration.get_server_path()
        except:
            self.logger.warning('Failed to update configuration of %s' % __name__)

    def is_connected(self):
        return self.connected

    def check_internet_connection(self):
        self.logger.info("Trying to connect to internet..")
        try:
            requests.get("http://www.google.com")
        except Exception as e:
            self.logger.warning("No connection to the internet")
            self.connected = False
            return False
        self.logger.info("Connected to the internet.")
        return True

    def check_server_connection(self):
        try:
            if requests.get(self.server_url+"request/config/checksum").status_code == 200:
                self.connected = True
                return True
        except Exception as e:
            self.logger.warning("No connection to the server")
            self.connected = False
            return False
        self.logger.info("Connected to the server.")
        return False

    def get_checksum(self):
        try:
            checksum = requests.get(self.server_url+"request/config/checksum").text
            return checksum
        except Exception as e:
            self.logger.warning("Failed to get configuration checksum from server")
        return 0

    def get_configuration(self):
        try:
            return requests.get(self.server_url+"request/config").json()
        except Exception as e:
            self.logger.warning("Failed to load configuration from server")
            raise e
    def send_packets(self, packets):
        try:
            r = requests.post(self.server_url+"request/packets",data=json.dumps(packets), headers=self.json_header)
        except Exception as e:
            self.logger.warning("Failed to send packets to server")
            self.connected = False
            return False
        self.connected = True
        return True

    def send_logs(self, logs):
        try:
            r = requests.post(self.server_url,data=json.dumps(logs), headers=self.json_header)
        except Exception as e:
            self.logger.warning("Failed to send logs to server")
            self.connected = False
            raise e
            return False
        self.connected = True
        return True
