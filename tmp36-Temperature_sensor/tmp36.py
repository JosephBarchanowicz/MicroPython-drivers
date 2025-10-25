from machine import ADC
from time import sleep

# 1. Set up the ADC on the desired pin
# GPIO 26 is a common choice for an analog input
adcpin = 26
tmp36 = ADC(adcpin)

# Define the reference voltage and a scaling factor for conversion
# 3.3V is the Pico's reference voltage
# 65535 is the maximum value from read_u16()
conversion_factor = 3.3 / 65535

def read_temperature():
    """Reads the TMP36 sensor and returns the temperature in Celsius."""
    # 2. Read the raw 16-bit value from the ADC
    raw_adc_value = tmp36.read_u16()

    # 3. Convert the raw ADC value to a voltage
    voltage = raw_adc_value * conversion_factor

    # 4. Convert the voltage to Celsius using the TMP36 formula
    # Formula: (voltage_in_V * 100) - 50 = degC
    temperature_C = (voltage * 100) - 50
    return round(temperature_C, 1)

