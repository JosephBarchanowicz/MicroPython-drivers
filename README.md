# Raspberry Pi Pico Motor Control with MicroPython

This project demonstrates how to control **two TT-style DC motors** using an **L298N motor driver** and a **Raspberry Pi Pico**, programmed in **MicroPython**.  

It’s a simple foundation for robotics projects such as rovers, line-followers, or other autonomous systems.

---

## Hardware Used
- Raspberry Pi Pico (RP2040 microcontroller)
- 2x TT Gear Motors
- L298N Motor Driver Module
- External power source for motors (recommended: 6–9V battery pack)
- Jumper wires and breadboard (optional)

---

## Wiring Diagram
- Pico GP pins → L298N `IN1–IN4` for motor control
- Pico GND → L298N GND
- External power → L298N `+12V` (or +V), GND shared with Pico
- Motors connected to `OUT1/OUT2` and `OUT3/OUT4` on the L298N
- ENA/ENB jumpers left on, or connected to PWM-capable pins for speed control

---

## Features
- Forward and backward motor control
- Individual motor direction control
- Easy extension for PWM speed control
- Modular MicroPython code

---

## Example MicroPython Code

```python
from motor_driver import MotorDriver
from time import sleep
    
    
if __name__ == "__main__":
    motor1 = MotorDriver(12, 10, 11, 13, 14, 15)
    try:
        while True:
            motor1.motor_forward(32768)
            sleep(2)
            
            motor1.motor_stop()
            sleep(2)
            
            motor1.motor_backward(32768)
            sleep(2)
            
            motor1.motor_stop()
            sleep(2)
            
            motor1.motor_fwda_revb(32768)
            sleep(2)
            
            motor1.motor_stop()
            sleep(2)
            
            motor1.motor_reva_fwdb(32768)
            sleep(2)
            
            motor1.motor_stop()
            sleep(2)
            
    except KeyboardInterrupt:
        motor1.motor_stop()
        print("Program Stopped")
