import machine
import utime

# RP Pico has a real time clock that is synchronized by Thonny.
# There is no battery backup for the clock, so it must be reset
# on each power up.

# create an instance of the real time clock
rtc = machine.RTC()

# directly access the real time clock
now = rtc.datetime()
print(f"rtc machine time = {now}")

# using utime module
# note this returns local time every time.

print(f"local time = {utime.gmtime()}")
print(f"gm time = {utime.localtime()}")
