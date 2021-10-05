import machine
import utime
 
temperature_sensor = machine.ADC(4)
conversion_factor = 3.3 / (65535)
 
while True:
    raw_reading = temperature_sensor.read_u16()
    volt_reading = raw_reading * conversion_factor 
    temperature = 27 - (volt_reading - 0.706)/0.001721
    print(raw_reading, volt_reading, temperature)
    utime.sleep(2)