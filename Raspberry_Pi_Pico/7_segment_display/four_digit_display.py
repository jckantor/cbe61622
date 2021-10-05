import tm1637
import machine
import utime


disp = tm1637.TM1637(clk=machine.Pin(3), dio=machine.Pin(2))
adc = machine.ADC(4)

def display_mv(timer):
    global adc, disp
    mv = 0
    N = 50
    for k in range(N):
        mv += 3300*adc.read_u16()/65535/N
    disp.number(int(mv))

machine.Timer(freq=2, mode=machine.Timer.PERIODIC, callback=display_mv)
