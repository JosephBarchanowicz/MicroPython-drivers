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
        
        