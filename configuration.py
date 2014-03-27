
local = None
timers = None
modbusSlaves = None

def get_server_path():
    return get_configuration_parameter('server','url')

def get_web_connection_timeout():
    return int(get_configuration_parameter('server','timeout'))

def get_time_interval_to_send_packets():
    return int(get_configuration_parameter('server','timeIntervalToSendPackets'))

def get_minimum_packets_to_send():
    return int(get_configuration_parameter('server','minimumPacketsToSend'))

def get_mcu_i2c_slave_address():
    return get_configuration_parameter('i2c','slaveAddress')

def get_i2c_bus_address():
    return get_configuration_parameter('i2c','busAddress')

def get_checksum():
    return get_configuration_parameter('sensorConfiguration','checksum')

def get_time_interval_to_store_local():
    return int(get_configuration_parameter('logging','timeIntervalToStoreLocal'))

def get_time_interval_to_send_log():
    return int(get_configuration_parameter('logging','timeIntervalToSendLog'))

def is_send_logs_to_server():
    return get_configuration_parameter('logging','sendLogsToServer')

def is_store_logs_local():
    return get_configuration_parameter('logging','storeLogsLocal')

def get_max_local_log_size():
    return int(get_configuration_parameter('logging','maxLocalLogSize'))

def get_time_interval_to_check_online_config():
    return int(get_configuration_parameter('logging','timeIntervalToCheckOnlineConfig'))

def get_log_level_to_send_to_server():
    return get_configuration_parameter('logging','logLevelToSendToServer')

def get_log_level_to_store_local():
    return get_configuration_parameter('logging','timeIntervalToStoreLocal')

def get_configuration_parameter(section, key):
    try:
        return local[section][key] 
    except KeyError:
        import logging
        logger = logging.getLogger(__name__)
        logger.error('Parameter {0} does not exist in configuration'.format(key))

        if section == 'server' and key == 'url':
            logger.warning('using default url http://200.2.191.227:5000')
            return 'http://200.2.191.227:5000/'
        if section == 'server' and key == 'timeIntervalToCheckOnlineConfig':
            logger.warning('using default timeIntervalToCheckOnlineConfig 100 ')
            return '100' 
        if section == 'server' and key == 'timeIntervalToSendPackets':
            logger.warning('using default timeIntervalToSendPackets 10 ')
            return '10'
        if section == 'server' and key == 'minimumPacketsToSend':
            logger.warning('using default minimumPacketsToSend 10 ')
            return '10'
        if section =='logging' and key == 'timeIntervalToStoreLocal':
            logger.warning('using default timeIntervalToStoreLocal 300')
            return '300'
    except:
        import logging
        logger = logging.getLogger(__name__)
        logger.error("Can't get configuration parameters, configuration not loaded")
