import logging
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from log_handlers_and_filters import ModbusClientFilter
from pymodbus.other_message import ReportSlaveIdRequest


class ModbusSlaveReader:

    """
    This class uses the pymodbus library to communicate with modbus slaves
    via serial connection.
    """

    def __init__(self, serial_socket):
        self.logger = logging.getLogger(__name__)

        self.client = ModbusClient(method='rtu', port=serial_socket, timeout=1)

        modbus_client_filter = ModbusClientFilter()
        logging.getLogger("pymodbus.client.sync").addFilter(
            modbus_client_filter)

    def read_register_value(self, slave, register):
        value = self.client.read_holding_registers(register, 1, unit=slave)
        self.logger.debug('value read from modbus slave: ' + value)
        return value

    def check_connection(self):
        """Before a timer is made in the ReadSensorScheduler to read the data
        from the modbus slaves, the connection with the modbus client is
        checked.
        """
        try:
            self.client.connect()
        except:
            self.logger.warning(
                'Unable to connect to modbus network, check serial port')
            raise
            return False

        try:
            rq = ReportSlaveIdRequest()
            rr = self.client.execute(rq)
            assert(rr is None)
            self.logger.warning('Unable to see modbus master on network')
            return True
        except:
            self.logger.warning('Unable to see modbus master on network')
            return False
