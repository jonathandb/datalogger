import json
from jsonschema import validate
from datetime import timedelta, datetime
import configparser
import configuration
import logging
import os


class ModbusSlave(object):
    __slots__ = ['type', 'address', 'register']


class Timer(object):
    __slots__ = ['type', 'slaves', 'start_time', 'time_interval']


class ConfigurationManager:

    def __init__(self, config_location):
        self.logger = logging.getLogger(__name__)
        self.config_location = config_location

        self.load_local_configuration()

    def load_local_configuration(self):
        """Loads the locally stored configuration
        Loads the json and put its parameters, modbus slaves
        and timers in the configuration module
        """
        try:
            if not os.path.exists(self.config_location):
                self.logger.error('Configuration file doesn\' exist!')

            configuration.local = configparser.ConfigParser()
            configuration.local.read(self.config_location)
            configuration.timers = []
            configuration.modbus_slaves = []

            slaves = json.loads(
                configuration.local['sensorConfiguration']['modbusSlaves'])
            for slave in slaves:
                s = ModbusSlave()
                s.type = slave[0]
                s.address = slave[1]
                s.register = slave[2]
                configuration.modbus_slaves.append(s)

            timers = json.loads(
                configuration.local['sensorConfiguration']['timers'])
            for timer in timers:
                t = Timer()
                t.type = timer[0]
                t.slaves = []
                for slave in configuration.modbus_slaves:
                    if slave.type == t.type:
                        t.slaves.append(slave)
                t.start_time = datetime.utcfromtimestamp(timer[1]).time()
                t.time_interval = timedelta(seconds=timer[2])
                configuration.timers.append(t)
        except KeyError as k:
            self.logger.warning(
                'Local configuration incomplete, key  %s not found ' %
                k)

    def is_online_configuration_different(self, online_checksum):
        if configuration.get_checksum() == online_checksum:
            return False
        else:
            return True

    def validate_json_configuration(self, json_configuration):
        configuration_schema = {
            "type": "object", "properties": {
                "timers": {
                    "type": "array", "items": {
                        "type": "array", "items": {
                            "type": "number", "minItems": 3, "maxItems": 3}
                    }
                },
                "modbus_slaves": {
                    "type": "array", "items": {
                        "type": "array", "items": {
                            "type": "number", "minItems": 3, "maxItems": 3}
                    }
                }
            }
        }
        try:
            validate(json_configuration, configuration_schema)
        except Exception as e:
            self.logger.warning("not valid json: \n\r%s" % e)

    def save_configuration_local(self, checksum, new_configuration):
        """Saves the new configuration locally. """
        # init sections
        try:
            configuration.local.add_section('sensorConfiguration')
            configuration.local.add_section('server')
            configuration.local.add_section('logging')
            configuration.local.add_section('i2c')
        except:
            pass

        configuration.local['sensorConfiguration']['checksum'] = str(checksum)

        self.try_save_configuration_parameter(
            new_configuration,
            'sensorConfiguration',
            'timers')
        self.try_save_configuration_parameter(
            new_configuration,
            'sensorConfiguration',
            'modbusSlaves')
        self.try_save_configuration_parameter(
            new_configuration,
            'server',
            'url')
        self.try_save_configuration_parameter(
            new_configuration,
            'server',
            'timeout')
        self.try_save_configuration_parameter(
            new_configuration,
            'server',
            'timeIntervalToSendPackets')
        self.try_save_configuration_parameter(
            new_configuration,
            'server',
            'minimumPacketsToSend')
        self.try_save_configuration_parameter(
            new_configuration,
            'sensorConfiguration',
            'sendLogsToServer')
        self.try_save_configuration_parameter(
            new_configuration,
            'logging',
            'storeLogsLocal')
        self.try_save_configuration_parameter(
            new_configuration,
            'logging',
            'logLevelToSendToServer')
        self.try_save_configuration_parameter(
            new_configuration,
            'logging',
            'logLevelToStoreLocal')
        self.try_save_configuration_parameter(
            new_configuration,
            'logging',
            'timeIntervalToStoreLocal')
        self.try_save_configuration_parameter(
            new_configuration,
            'logging',
            'timeIntervalToSendLog')
        self.try_save_configuration_parameter(
            new_configuration,
            'logging',
            'sendLogsToServer')
        self.try_save_configuration_parameter(
            new_configuration,
            'logging',
            'storeLogsLocal')
        self.try_save_configuration_parameter(
            new_configuration,
            'logging',
            'timeIntervalToCheckOnlineConfig')
        self.try_save_configuration_parameter(
            new_configuration,

            'logging',
            'maxLocalLogSize')
        self.try_save_configuration_parameter(
            new_configuration,
            'i2c',
            'slaveAddress')
        self.try_save_configuration_parameter(
            new_configuration,
            'i2c',
            'busAddress')
        try:
            config_dirpath = os.path.dirname(
                os.path.abspath(
                    self.config_location))
            if not os.path.isdir(config_dirpath):
                try:
                    os.makedirs(config_dirpath)
                    self.logger.info(
                        'Made configuration folder {0}'.format(config_dirpath))
                except:
                    self.logger.error('Problem making configuration folder')
                    raise

            with open(self.config_location, 'w') as configfile:
                configuration.local.write(configfile)
            self.logger.info("New Configuration saved")
        except:
            self.logger.error('Problem storing configuration file')
            raise
        self.load_local_configuration()

    def try_save_configuration_parameter(
            self,
            online_configuration,
            section,
            key):
        try:
            configuration.local[section][key] = str(online_configuration[key])
        except KeyError:
            self.logger.warning(
                'Parameter %s does not exist in online configuration' %
                key)
