
from machine import UART, Pin
import uos
import time

print("uos.uname() information")
print("\tsysname: \t" + uos.uname()[0])
print("\tnodename: \t" + uos.uname()[1])
print("\trelease: \t" + uos.uname()[2])
print("\tversion: \t" + uos.uname()[3])
print("\tmachine: \t" + uos.uname()[4])


uart0 = UART(0, baudrate=115200, tx=Pin(16), rx=Pin(17))

wifi_ssid = ("ND-guest")

uart0.write('AT+CIPMUX=1'+'\r\n')


while True:
    rxData = ""
    while uart0.any() > 0:
        rxData += str(uart0.read(1))
    rxData = rxData.replace("b'", "")
    
    if (len(rxData)):
        print(rxData, end="")

#while True:
#    rxData = bytes()
#    while uart0.any() > 0:
#        rxData += uart0.read(1)
#      
#    if (len(rxData)):
#        print(rxData.decode('utf-8'), end="")