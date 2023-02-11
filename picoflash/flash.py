from machine import Pin
import utime

pin = Pin('LED', Pin.OUT)

while True:
    pin.toggle()
    utime.sleep_ms(1000)