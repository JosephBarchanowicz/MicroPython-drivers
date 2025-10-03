import machine, time
from machine import Pin


class hcsr04:
    
    def __init__(self, t_pin, e_pin, echo_timeout=500*2*30):
        
        self.echo_timeout_us = echo_timeout
        self.trigger = Pin(t_pin, mode=Pin.OUT, pull=None)
        self.trigger.low()
        self.echo = Pin(e_pin, mode=Pin.IN, pull=None)

    def _send_pulse(self):
        
        self.trigger.low()
        time.sleep_us(5)
        self.trigger.high()
        time.sleep_us(10)
        self.trigger.low()
        try:
            pulse_time = machine.time_pulse_us(self.echo, 1, self.echo_timeout_us)
            return pulse_time
        except OSError as ex:
            if ex.args[0] == 110: 
                raise OSError('Out of range')
            raise ex

    def distance_mm(self):
        pulse_time = self._send_pulse() 
        mm = pulse_time * 100 // 582
        return mm

    def distance_cm(self):
        pulse_time = self._send_pulse()
        cm = (pulse_time / 2) / 29.1
        return cm
