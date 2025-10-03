# HC‑SR04 Ultrasonic Distance Sensor — Raspberry Pi Pico (MicroPython)

Measure distances with an HC‑SR04 ultrasonic sensor using a Raspberry Pi Pico and MicroPython. This README covers hardware, wiring, a safe **voltage divider** for the 5V Echo line, and a tested MicroPython example.

---

## Features

* MicroPython driver-style example (single file)
* Robust timing with `machine.time_pulse_us`
* Works with **HC‑SR04** (5V) on **Pico (3.3V GPIO)**
* Notes on speed‑of‑sound compensation and simple fault handling

---

## Parts & Tools

* Raspberry Pi Pico or Pico W (3.3V logic)
* HC‑SR04 ultrasonic module (Trig, Echo, Vcc, GND)
* Breadboard + jumper wires
* **Two resistors** for a voltage divider on *Echo* (example: **R1=10kΩ**, **R2=20kΩ**)

> **Why the divider?** The HC‑SR04 *Echo* pin outputs **~5V**. Pico GPIO are **3.3V‑only**. The divider drops Echo to a safe level.

---

## Wiring Overview

**HC‑SR04 → Pico**

| HC‑SR04 Pin | Connects To                       | Notes                          |
| ----------- | --------------------------------- | ------------------------------ |
| Vcc         | Pico **VBUS/5V** (or external 5V) | Do **not** power from Pico 3V3 |
| GND         | Pico **GND**                      | Common ground required         |
| Trig        | Pico **GPIO X** (output)          | 3.3V is fine for HC‑SR04 Trig  |
| Echo        | Pico **GPIO Y** **via divider**   | Must level‑shift to ~3.3V      |

> Choose any free Pico GPIO for X (Trig) and Y (Echo); the example defaults are noted in code below.

---

## Voltage Divider for Echo (5V → ~3.3V)

Use a simple two‑resistor divider:

```
5V (Echo) ── R1 ──┬──> Pico Echo (GPIO Y)
                  |
                 R2
                  |
                 GND
```

The output at the Pico pin is:

```
Vout = Vin × R2 / (R1 + R2)
```

Good choices (Vin ≈ 5.0V):

* **R1 = 1kΩ, R2 = 2kΩ → Vout ≈ 3.33V** (safe, low current)
* R1 = 4.7kΩ, R2 = 10kΩ → Vout ≈ 3.40V
* R1 = 2kΩ,  R2 = 3.3kΩ → Vout ≈ 3.12V

Keep total resistance ≥ ~10kΩ to limit current; avoid too high (≫100kΩ) to reduce edge slow‑down. 10k/20k is a nice balance.

> **Alternative:** Use a proper 1‑channel logic‑level shifter or a small NPN/MOSFET level‑shifter if you prefer.

---

## MicroPython Example (single file)

Create `hcsr04_pico.py` and copy the following. Adjust pins if needed.

```python
# hcsr04_pico.py
# Raspberry Pi Pico + HC‑SR04 — MicroPython example
# Wiring: Trig -> GPIO 3 (example), Echo (via divider) -> GPIO 2
# Power: HC‑SR04 Vcc -> 5V (VBUS), GND common to Pico

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

from time import sleep

# Initialize the HC-SR04 sensor with trigger on GPIO 17 and echo on GPIO 16
sensor = hcsr04(17, 16, 30000)

while True:
    try:
        distance_mm = sensor.distance_mm()
        print(f'Distance: {distance_mm} mm')
    except OSError as e:
        print('Error:', e)
    sleep(1) 
```

### Pin Selection Tips

* Use any available **GPIO**; avoid SWD pins if you actively debug.
* Keep **Echo** wiring short; keep the divider close to the Pico pin to reduce ringing.

---

## Calibration & Environment Notes

* **Temperature affects sound speed.** For higher accuracy, apply a temperature correction (optional):

  * `speed (m/s) ≈ 331.3 + 0.606 × T°C`
  * Update the `58.0` constant accordingly, or compute from first principles.
* The HC‑SR04 minimum range is typically ~2 cm; maximum practical range ~3–4 m.
* Soft materials (cloth, foam) and angled surfaces reflect poorly—expect unstable readings.

---

## Troubleshooting

* **Always 0 or timeout:** Check common ground, Trig wiring, and that Echo is level‑shifted.
* **Noisy/erratic values:** Shorten wires, ensure solid 5V supply, add 100nF decoupling near sensor.
* **Interference:** Avoid nearby ultrasounds (other HC‑SR04s); add a small delay between pings (≥60 ms).

---

### Quick Start

1. Wire the sensor (include the **Echo divider**!).
2. Copy `hcsr04_pico.py` to the Pico (e.g., with Thonny).
3. Run the script and watch the serial console for `Distance: ... cm`.

Happy measuring! 📏🔊
