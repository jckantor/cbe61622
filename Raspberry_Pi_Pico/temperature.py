import machine
import time
 
sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)
 
while True:
    raw_reading = sensor_temp.read_u16()
    volt_reading = raw_reading * conversion_factor 
    temperature = 27 - (volt_reading - 0.706)/0.001721
    print(raw_reading, volt_reading, temperature)
    print(machine.ADC.CORE_TEMP)
    time.sleep(2)