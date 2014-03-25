import requests
import json
from jsonschema import validate
from datetime import timedelta, time, datetime
import configparser
import configuration
import logging
import os

class ModbusSlave(object):
    __slots__ = ['type','address','register']

class Timer(object):
    __slots__ = ['type', 'slaves' , 'start_time', 'time_interval']


class ConfigurationManager:
    def __init__(self, config_location):
        self.logger = logging.getLogger()
        self.config_location = config_location

        self.load_local_configuration()
    
    def load_local_configuration(self):
    	if configuration.local == None:
            try:
                if not os.path.exists(self.config_location):
                    self.logger.error('Configuration file doesn\' exist!')

                configuration.local = configparser.ConfigParser()
                configuration.local.read(self.config_location)
                configuration.timers = []
                configuration.modbus_slaves = []

                for json_modbus_slave in json.loads(configuration.local['sensorConfiguration']['modbusSlaves']):
                    s = ModbusSlave()
                    s.type = json_modbus_slave[0]
                    s.address = json_modbus_slave[1]
                    s.register = json_modbus_slave[2]
                    configuration.modbus_slaves.append(s)
                    
                for json_timer in json.loads(configuration.local['sensorConfiguration']['timers']):
                    t = Timer()
                    t.type = json_timer[0]
                    t.slaves = []
                    for slave in configuration.modbus_slaves:
                        if slave.type == t.type:
                            t.slaves.append(slave)
                    t.start_time = datetime.utcfromtimestamp(json_timer[1]).time()
                    t.time_interval = timedelta(seconds=json_timer[2])
                    configuration.timers.append(t)
            except KeyError as k:
                self.logger.warning('Local configuration incomplete, key  %s not found ' % k)
                
    def is_configuration_online_different(self, online_checksum):
        if configuration.get_checksum() == online_checksum:
            return False
        else:
            return True

    def validate_json_configuration(self, json_configuration):
        configuration_schema = {
         "type" : "object",
         "properties": {
             "timers": {
                 "type": "array",
                 "items": {"type": "array",
                           "items": {"type":"number", "minItems":3, "maxItems":3}
                          }
             },
             "modbus_slaves": {
                 "type": "array",
                 "items": {"type": "array",
                           "items": {"type":"number", "minItems":3, "maxItems":3}
                 }
             }
         }
        }
        try:
            validate(json_configuration, configuration_schema)
        except Exception as e:
            self.logger.warning("not valid json: \n\r%s" % e)

    def save_online_configuration_local(self, checksum, online_configuration):
        #init sections
        try:
            configuration.local.add_section('sensorConfiguration')
            configuration.local.add_section('server')
            configuration.local.add_section('logging')
            configuration.local.add_section('i2c')
        except:
            pass

        configuration.local['sensorConfiguration']['checksum'] = str(checksum)
        
        self.try_save_configuration_parameter(online_configuration,
                                      'sensorConfiguration','timers')
        self.try_save_configuration_parameter(online_configuration,
                                      'sensorConfiguration','modbusSlaves')
        self.try_save_configuration_parameter(online_configuration,
                                      'server','url')
        self.try_save_configuration_parameter(online_configuration,
                                      'server','timeout')
        self.try_save_configuration_parameter(online_configuration,
                                      'server','timeIntervalToSendPackets')
        self.try_save_configuration_parameter(online_configuration,
                                      'server','minimumPacketsToSend')
        self.try_save_configuration_parameter(online_configuration,
                                      'sensorConfiguration','sendLogsToServer')
        self.try_save_configuration_parameter(online_configuration,
                                      'logging','storeLogsLocal')
        self.try_save_configuration_parameter(online_configuration,
                                      'logging','logLevelToSendToServer')
        self.try_save_configuration_parameter(online_configuration,
                                      'logging','logLevelToStoreLocal')
        self.try_save_configuration_parameter(online_configuration,
                                      'logging','timeIntervalToStoreLocal')
        self.try_save_configuration_parameter(online_configuration,
                                      'logging','timeIntervalToSendLog')
        self.try_save_configuration_parameter(online_configuration,
                                      'logging','sendLogsToServer')       
        self.try_save_configuration_parameter(online_configuration,
                                      'logging','storeLogsLocal')
        self.try_save_configuration_parameter(online_configuration,
                                      'logging','timeIntervalToCheckOnlineConfig')       
        self.try_save_configuration_parameter(online_configuration,
                                      'logging','maxLocalLogSize')
        self.try_save_configuration_parameter(online_configuration,
                                      'i2c','slaveAddress')
        self.try_save_configuration_parameter(online_configuration,
                                      'i2c','busAddress')
        try:
            with open(self.config_location, 'w') as configfile:
                configuration.local.write(configfile)
            self.logger.info("New Configuration loaded and saved")
        except:
            self.logger.error('Problem storing configuration file')
        
        self.load_local_configuration()

    def try_save_configuration_parameter(self, online_configuration, section, key):
        try:
            configuration.local[section][key] = str(online_configuration[key])
        except KeyError:
            self.logger.warning('Parameter %s does not exist in online configuration' % key)


