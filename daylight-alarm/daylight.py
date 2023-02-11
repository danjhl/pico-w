import machine
import utime

pin = machine.Pin('LED', machine.Pin.OUT)

# Set current time
start =  (2021, 1, 11, 6, 15, 5, 0, 0)
machine.RTC().datetime(start)

# Set alarm in 10 seconds
alarm = (2021, 1, 11, 15, 5, 10, 0, 11)
alarm_s = utime.mktime(alarm)

now = utime.time()
diff = alarm_s - now

if diff < 0:
    print("Alarm was set in the past not activating light")
else:
    utime.sleep_ms(diff * 1000)
    pin.toggle()
    utime.sleep_ms(10_000)
    pin.toggle()