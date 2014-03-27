import configuration
import time
import requests
import logging
import json
from jsonschema import validate

class ConnectionManager:
    def __init__(self):
        self.json_header = {'content-type': 'application/json'}
        self.logger = logging.getLogger(__name__)

        connection_filter = ConnectionFilter()
        logging.getLogger('requests.packages.urllib3.connectionpool').addFilter(connection_filter)
        
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
            self.update_led()
            return False
        self.logger.info("Connected to the internet.")
        self.connected = True
        self.update_led()
        return True

    def check_server_connection(self):
        try:
            if requests.get(self.server_url+"request/config/checksum").status_code == 200:
                self.connected = True
        except Exception as e:
            self.logger.warning("No connection to the server")
            self.connected = False
            return False
        self.logger.info("Connected to the server.")
        self.update_led()
        return True 

    def get_checksum(self):
        try:
            checksum_req = requests.get(self.server_url+"request/config/checksum")
            if checksum_req.status_code != 200:
                raise requests.ConnectionError()
            return checksum_req.text
        except Exception as e:
            self.logger.warning('Failed to get configuration checksum from server, is server application running?')
            raise
        return 0

    def get_configuration(self):
        try:
            config_req = requests.get(self.server_url+"request/config")
            if config_req.status_code == 200:
                return config_req.json()
            else:
                raise requests.ConnectionError()

        except Exception as e:
            self.logger.warning("Failed to load configuration from server: %s" % e)
            raise

    def send_packets(self, packets):
        nr_of_sent_packets = 0
        try:
            nr_of_sent_packets = len(packets)
            post = requests.post(self.server_url+"request/packets",data=json.dumps(packets), headers=self.json_header)
            if self.validate_response(post):
                self.log_response(post)
                if not post.json()['status'] == 'success':
                    nr_of_sent_packets = 0
            else:
                self.logger.warning('Failed to interpret response of server, http code= %s', post.status_code)
                nr_of_sent_packets = 0
            self.connected = True 
        except Exception as e:
            self.logger.warning('Failed to send packets, server message: %s', e)
            nr_of_sent_packets = 0
            self.connected = False
            self.update_led()
        self.update_led()
        self.logger.info('%s packages are sent, current nr of packets is %s. ',
                        nr_of_sent_packets, len(packets))
        return nr_of_sent_packets

    def validate_response(self, post):
        json_schema = {
            "type" : "object",
            "properties" : {
                "status" : {"type" : "string"},
                "msg" : {"type" : "string"},
            },
        }

        try:
            validate(json_schema, post.json())
        except:
            return False
        return True

    def log_response(self, post):
        if post.json()['status'] == 'error':
            self.logger.warning('Failed to send data, code %s, server message: %s', 
                                post.status_code, 
                                post.json()['msg'])
        elif post.json()['status'] == 'success':
            self.logger.info('Sent packets to server, code %s, server message: %s', 
                             post.status_code, 
                             post.json()['msg'])

    def send_logs(self, logs):
        nr_of_sent_logs = 0
        try:
            nr_of_sent_logs= len(logs)
            post = requests.post(self.server_url+'request/logs',data=json.dumps(logs), headers=self.json_header)
            
            if self.validate_response(post):
                self.log_response(post)
                if not post.json()['status'] == 'success':
                    nr_of_sent_logs = 0
            else:
                self.logger.warning('Failed to interpret response of server, http code= %s', post.status_code)
            nr_of_sent_logs = 0
            self.connected = True 
        except Exception as e:
            self.logger.warning('Failed to send logs to server:', e)
            nr_of_sent_logs = 0
            self.connected = False
        self.update_led()
        return nr_of_sent_logs

    def update_led(self):
        try:
            if self.connected:
                self.led_call.on()
            else:
                self.led_call.off()
        except:
            pass

    def set_led_call(self, led_call):
        self.led_call = led_call

class ConnectionFilter(logging.Filter):
    def filter(self, record):
        return False 
