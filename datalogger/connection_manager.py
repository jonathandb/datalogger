import configuration
import requests
import logging
import json
from jsonschema import validate


CHECKSUM_URL_SUFFIX = 'request/config/checksum'


class ConnectionManager:

    """This class provides a connection to the server and is able to:
        - Check connection
        - Sent packets
        - Sent logs
        - Give validation of the response of the requests
    """

    def __init__(self):
        self.json_header = {'content-type': 'application/json'}
        self.logger = logging.getLogger(__name__)

        connection_filter = ConnectionFilter()
        requests_logger_name = 'requests.packages.urllib3.connectionpool'
        logging.getLogger(requests_logger_name).addFilter(
            connection_filter)

        self.connected = False
        self.update_configuration()

    def update_configuration(self):
        try:
            self.server_url = configuration.get_server_path()
        except:
            self.logger.warning(
                'Failed to update configuration of {0}'.format(__name__))

    def is_connected(self):
        return self.connected

    def check_internet_connection(self):
        self.logger.info('Trying to connect to internet..')
        try:
            requests.get("http://www.google.com")
        except Exception:
            self.logger.warning('No connection to the internet')
            self.connected = False
            self.update_led()
            return False
        self.logger.info('Connected to the internet.')
        self.update_led()
        return True

    def check_server_connection(self):
        try:
            req = requests.get(self.server_url+CHECKSUM_URL_SUFFIX)
            if req.status_code == 200:
                self.connected = True
            else:
                raise
        except Exception:
            self.logger.warning('No connection to the server')
            self.connected = False
            return False
        self.logger.info('Connected to the server.')
        self.update_led()
        return True

    def get_configuration_checksum(self):
        if self.connected:
            try:
                checksum_req = requests.get(
                    self.server_url + CHECKSUM_URL_SUFFIX)
                if checksum_req.status_code != 200:
                    raise requests.ConnectionError()
                return checksum_req.text
            except Exception:
                warning = 'Failed to get configuration checksum from server,'\
                    'is server application running?'
                self.logger.warning(warning)
                raise
        return 0

    def get_configuration(self):
        if self.connected:
            try:
                config_req = requests.get(self.server_url+"request/config")
                if config_req.status_code == 200:
                    return config_req.json()
                else:
                    raise requests.ConnectionError()

            except Exception as e:
                self.logger.warning(
                    'Failed to load configuration from server: {0}'.format(e))
                raise

    def send_packets(self, packets):
        nr_of_sent_packets = 0
        if self.connected:
            try:
                nr_of_sent_packets = len(packets)
                self.logger.info(
                    '{0} packets are ready to be sent'.format(
                        nr_of_sent_packets))
                post = requests.post(
                    self.server_url +
                    "request/packets",
                    data=json.dumps(packets),
                    headers=self.json_header)
                if self.validate_response(post):
                    self.log_response(post)
                    if not post.json()['status'] == 'success':
                        nr_of_sent_packets = 0
                else:
                    warning = 'Failed to interpret response of server,'\
                        'http code= {0}'.format(post.status_code)
                    self.logger.warning(warning)
                    nr_of_sent_packets = 0
                self.connected = True
            except Exception as e:
                self.logger.warning(
                    'Failed to send packets, server message: {0}'.format(e))
                nr_of_sent_packets = 0
                self.connected = False
                self.update_led()
            self.update_led()
            self.logger.info(
                '{0} packages are sent, current nr of packets is {1}.'.format(
                    nr_of_sent_packets,
                    len(packets)))
        else:
            self.logger.info(
                'Postponing sending packets, no connection to server')
        return nr_of_sent_packets

    def validate_response(self, post):
        json_schema = {
            "type": "object",
            "properties": {
                "status": {"type": "string"},
                "msg": {"type": "string"},
            },
        }

        try:
            validate(json_schema, post.json())
        except:
            return False
        return True

    def log_response(self, post):
        if post.json()['status'] == 'error':
            self.logger.warning(
                'Failed to send data, code {0}, server message: {1}'.format(
                    post.status_code,
                    post.json()['msg']))
        elif post.json()['status'] == 'success':
            self.logger.info(
                'Sent data to server, code {0}, server message: {1}'.format(
                    post.status_code,
                    post.json()['msg']))

    def send_logs(self, logs):
        nr_of_sent_logs = 0
        if self.connected:
            try:
                nr_of_sent_logs = len(logs)
                post = requests.post(
                    self.server_url +
                    'request/logs',
                    data=json.dumps(logs),
                    headers=self.json_header)

                if self.validate_response(post):
                    self.log_response(post)
                    if not post.json()['status'] == 'success':
                        nr_of_sent_logs = 0
                else:
                    warning = 'Failed to interpret response of server,'\
                        'http code= {0}'.format(
                            post.status_code)
                    self.logger.warning(warning)

                nr_of_sent_logs = 0
                self.connected = True
            except Exception as e:
                self.logger.warning(
                    'Failed to send logs to server: {0}'.format(e))
                nr_of_sent_logs = 0
                self.connected = False
            self.update_led()
        else:
            self.logger.info(
                'Postponing sending logs, no connection to server')
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
