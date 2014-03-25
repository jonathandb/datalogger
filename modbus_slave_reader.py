import time
import logging
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.other_message import *
from log_handlers_and_filters import ModbusClientFilter

class ModbusSlaveReader:
    def __init__(self, serial_socket):
        self.logger = logging.getLogger(__name__)

        self.client = ModbusClient(method='rtu', port=serial_socket, timeout=1)

        modbus_client_filter = ModbusClientFilter()
        logging.getLogger("pymodbus.client.sync").addFilter(modbus_client_filter)

   
    def read_register_value(self, slave, register):
        value = self.client.read_holding_registers(register, 1, unit=slave)
        self.logger.debug('16bit value read from mcu: ' + char)
        return value

    def check_connection(self):
        try:
            self.client.connect()
        except:
            self.logger.warning('Unable to connect to modbus network, check serial port')
            raise
            return False

        try:
            rq = ReportSlaveIdRequest()
            rr = self.client.execute(rq)
            assert(rr == None)
            self.logger.warning('Unable to see modbus master on network')
            return True 
        except:
            self.logger.warning('Unable to see modbus master on network')
            return False
