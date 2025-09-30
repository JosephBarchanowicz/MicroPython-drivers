# Import the necessary modules from MicroPython
from machine import Pin, PWM
    
class MotorDriver:
    def __init__(self, enable_a, input1_a, input2_a, enable_b, input1_b, input2_b):
        self.enable_a = enable_a
        self.input1_a = input1_a
        self.input2_a = input2_a
        self.enable_b = enable_b
        self.input1_b = input1_b
        self.input2_b = input2_b
        
        self.in1 = Pin(input1_a, Pin.OUT)
        self.in2 = Pin(input2_a, Pin.OUT)
        self.ena = PWM(Pin(enable_a))
        self.ena.freq(1000)
        
        self.in3 = Pin(input1_b, Pin.OUT)
        self.in4 = Pin(input2_b, Pin.OUT)
        self.enb = PWM(Pin(enable_b))
        self.enb.freq(1000)
        
    def motor_forward(self, speed):
        print("Moving Forward")
        self.in1.high()
        self.in2.low()
        self.ena.duty_u16(speed)
        self.in3.high()
        self.in4.low()
        self.enb.duty_u16(speed)
     
    def motor_backward(self, speed):
        print("Moving Backward")
        self.in1.low()
        self.in2.high()
        self.ena.duty_u16(speed)
        self.in3.low()
        self.in4.high()
        self.enb.duty_u16(speed)
        
    def motor_fwda_revb(self, speed):
        print("Moving Motor A Forward Motor B Reverse")
        self.in1.high()
        self.in2.low()
        self.ena.duty_u16(speed)
        self.in3.low()
        self.in4.high()
        self.enb.duty_u16(speed)
        
    def motor_reva_fwdb(self, speed):
        print("Moving Motor A Reverse Motor B Forward")
        self.in1.low()
        self.in2.high()
        self.ena.duty_u16(speed)
        self.in3.high()
        self.in4.low()
        self.enb.duty_u16(speed)
        
    def motor_stop(self):
        print("Motor Stopped")
        self.in1.low()
        self.in2.low()
        self.ena.duty_u16(0)
        self.in3.low()
        self.in4.low()
        self.enb.duty_u16(0)

        
        
        
        