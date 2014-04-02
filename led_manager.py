from apscheduler.scheduler import Scheduler
import logging
from datetime import datetime, timedelta
from time import sleep
import os
from enum import IntEnum, Enum

FLASH_TIME = 100

class PinName(IntEnum):
    """
    Contains all the led pins with their function

    Add other led pins here
    """
    powered = 1
    logging = 2
    connected = 3
    readingsensor = 4

class LedState(Enum):
    on = 1
    off = 2
    flash = 3

class Led(object):
    def __init__(self,pin_name, ledstate):
        self.pin_name = pin_name
        self.state = ledstate
        self.enabled = False

    def set_state(self, ledstate):
        self.state = ledstate

    def get_pin(self):
        return int(self.pin_name)

    def set_pindir(self, pindir):
        self.enabled = True
        self.pindir = pindir

    def get_pindir(self):
        return pindir

class LedManager():
    """
    Manages the gpio pins.
    """
    def __init__(self, scheduler):
        self.logger = logging.getLogger(__name__)
        self.scheduler = scheduler
        self.pindirs = []
        self.leds = []

        for pin in PinName:
            self.leds.append(Led(pin, LedState.off))

    def update_led(self, pin_name, ledstate):
        """
        If the pin has an other state, it will be updated.
        """
        for led in self.leds:
            if led.pin_name == pin_name:
                if led.state != ledstate:
                    led.set_state(ledstate)
                    if not led.enabled:
                        self.enable_output(led.get_pin())

                    if led.state == LedState.on:
                        self.turn_on(led.get_pin())
                    elif led.state == LedState.off:
                        self.turn_off(led.get_pin())
                    elif led.state == LedState.flash:
                        self.flash(led.get_pin(), FLASH_TIME)
                return
        raise Exception('Led doesn\'t exist')

    def enable_output(self, pin_nr):
        """Tries to activate the gpio pin.
        If the activation is successfull, the pin is set as output.
        """
        if self.activate(pin_nr):
            self.set_as_output(pin_nr)

    def activate(self, pin_nr):
        activated = False
        try:
            f= open ('/sys/class/gpio/export','w')
            f.write(str(pin_nr))
            f.close()
            activated = True
        except IOError as e:
            if 'Device or resource busy' in e:
                self.logger.debug('GPIO pin {0} already activated'.format(pin_nr))
            else:
                self.logger.debug('Failed to activate GPIO pin {0}'.format(pin_nr))

        for dirpath, dirnames, filename in os.walk('/sys/class/gpio/'):
            for d in dirnames:
                if 'gpio' + str(pin_nr) in d:
                    self.pindirs[pin_nr] = d
        return activated
    def set_as_output(self, pin_nr):
        try:
            path = '/sys/class/gpio/' + self.pindirs[pin_nr] +  '/direction'
            f= open (path,'w')
            f.write('out')
            f.close()
        except:
            self.logger.debug('Failed to set GPIO pin {0} as output'.format(pin_nr))

    def turn_on(self, pin_nr):
        """Sets gpio pin on"""
        try:
            path = '/sys/class/gpio/' + self.pindirs[pin_nr] + '/value'
            f= open (path,'w')
            f.write('1')
            f.close()
        except:
            self.logger.debug('Failed to change value GPIO pin {0}'.format(pin_nr))

    def turn_off(self, pin_nr):
        """Sets gpio pin off"""
        try:
            path = '/sys/class/gpio/' + self.pindirs[pin_nr] + '/value'
            f= open (path,'w')
            f.write('0')
            f.close()
        except:
            self.logger.debug('Failed to change value GPIO pin {0}'.format(pin_nr))

    def flash(self, pin_nr, msecs):
        """Sets gpio pin on for certain msecs.

        :param pin_nr: gpio pin
        :param msecs: time in milliseconds the pin will be on
        """
        self.turn_on(pin_nr)
        time_to_turn_off = datetime.now() + timedelta(microseconds=msecs*1000)
        try:
            self.scheduler.add_date_job(self.turn_off,
                                              time_to_turn_off,[pin_nr] )
        except:
            self.turn_off(msecs)

class LedCall:
    """
    Instances of this class are given to classes which have events that controls
    the leds.
    """
    def __init__(self, led_manager, led_pin):
        self.led_manager = led_manager
        self.led_pin = led_pin

    def on(self):
        self.led_manager.update_led(self.led_pin, LedState.on)

    def off(self):
        self.led_manager.update_led(self.led_pin, LedState.off)

    def flash(self):
        self.led_manager.update_led(self.led_pin, LedState.flash)
